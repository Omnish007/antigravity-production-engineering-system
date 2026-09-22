#!/usr/bin/env python3
"""aggregate-state.py

Authoritative State Aggregator:
- Generates aggregate derived views (tasks.json, governance.json, events.jsonl, blockers.json)
  purely FROM SCRATCH from canonical per-task records (P0-06).
- Never merges stale existing aggregate records (P0-06).
- Atomic file writes using tempfile, fsync, and atomic os.replace (P1-03).
- Uses workspace_resolver.py deterministically without hardcoded template paths (P0-31, P0-32).
"""

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Dict, List, Optional

# Add core validation package to sys.path
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from workspace_resolver import resolve_workspace
except ImportError:
    from .workspace_resolver import resolve_workspace


def atomic_write_json(target_path: Path, data: Any):
    """Write JSON data atomically via tempfile + fsync + os.replace (P1-03)."""
    target_path = Path(target_path).resolve()
    target_dir = target_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", dir=str(target_dir), delete=False, encoding="utf-8") as tf:
        temp_name = tf.name
        json.dump(data, tf, indent=2)
        tf.write("\n")
        tf.flush()
        os.fsync(tf.fileno())

    os.replace(temp_name, str(target_path))


def atomic_write_jsonl(target_path: Path, items: List[Dict[str, Any]]):
    """Write JSONL lines atomically via tempfile + fsync + os.replace (P1-03, P1-04)."""
    target_path = Path(target_path).resolve()
    target_dir = target_path.parent
    target_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", dir=str(target_dir), delete=False, encoding="utf-8") as tf:
        temp_name = tf.name
        for item in items:
            tf.write(json.dumps(item) + "\n")
        tf.flush()
        os.fsync(tf.fileno())

    os.replace(temp_name, str(target_path))


def aggregate_tasks(state_dir: Path, errors: List[str]):
    """Rebuild tasks.json from scratch reading only canonical tasks/*.json (P0-06)."""
    tasks_dir = state_dir / "tasks"
    tasks_file = state_dir / "tasks.json"

    tasks_list: List[Dict[str, Any]] = []
    if tasks_dir.is_dir():
        for fname in sorted(os.listdir(tasks_dir)):
            if fname.endswith(".json"):
                fpath = tasks_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        t = json.load(f)
                        if isinstance(t, dict) and t.get("id"):
                            tasks_list.append(t)
                except Exception as e:
                    errors.append(f"Failed to parse canonical per-task file '{fpath.name}': {e}")

    # Build fresh aggregate view (preserving phases if defined, otherwise empty)
    fresh_aggregate: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "tasks": tasks_list,
        "phases": [],
    }

    # If existing tasks.json had phases defined, carry over phases structure only
    if tasks_file.is_file():
        try:
            with open(tasks_file, "r", encoding="utf-8") as f:
                old = json.load(f)
                if isinstance(old, dict) and "phases" in old:
                    fresh_aggregate["phases"] = old["phases"]
        except Exception:
            pass

    atomic_write_json(tasks_file, fresh_aggregate)
    print(f"Generated aggregate {tasks_file} from {len(tasks_list)} canonical per-task records")


def aggregate_governance(state_dir: Path, errors: List[str]):
    """Rebuild governance.json from scratch reading only canonical governance/*.json (P0-06)."""
    gov_dir = state_dir / "governance"
    gov_file = state_dir / "governance.json"

    records_list: List[Dict[str, Any]] = []
    if gov_dir.is_dir():
        for fname in sorted(os.listdir(gov_dir)):
            if fname.endswith(".json"):
                fpath = gov_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        rec = json.load(f)
                        if isinstance(rec, dict) and rec.get("taskId"):
                            records_list.append(rec)
                except Exception as e:
                    errors.append(f"Failed to parse canonical per-task governance file '{fpath.name}': {e}")

    fresh_aggregate: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "records": records_list,
    }
    atomic_write_json(gov_file, fresh_aggregate)
    print(f"Generated aggregate {gov_file} from {len(records_list)} canonical per-task records")


def aggregate_events(state_dir: Path, errors: List[str]):
    """Rebuild events.jsonl from scratch reading only canonical events/*.jsonl (P0-06, P0-07)."""
    events_dir = state_dir / "events"
    events_file = state_dir / "events.jsonl"

    all_events: List[Dict[str, Any]] = []
    if events_dir.is_dir():
        for fname in sorted(os.listdir(events_dir)):
            if fname.endswith(".jsonl") or fname.endswith(".json"):
                fpath = events_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        for line in f:
                            l = line.strip()
                            if l:
                                ev = json.loads(l)
                                if isinstance(ev, dict):
                                    all_events.append(ev)
                except Exception as e:
                    errors.append(f"Failed to parse canonical per-task events file '{fpath.name}': {e}")

    # Sort events by sequence if available, or timestamp
    def _sort_key(ev: Dict[str, Any]):
        seq = ev.get("sequence")
        ts = ev.get("timestamp") or ""
        return (seq if isinstance(seq, int) else 999999, ts)

    all_events.sort(key=_sort_key)
    atomic_write_jsonl(events_file, all_events)
    print(f"Aggregated {len(all_events)} events into {events_file}")


def aggregate_blockers(state_dir: Path, errors: List[str]):
    """Rebuild blockers.json from scratch reading only canonical blockers/*.json (P0-06, P0-35)."""
    blockers_dir = state_dir / "blockers"
    blockers_file = state_dir / "blockers.json"

    active_map: Dict[str, Dict[str, Any]] = {}
    resolved_map: Dict[str, Dict[str, Any]] = {}

    if blockers_dir.is_dir():
        for fname in sorted(os.listdir(blockers_dir)):
            if fname.endswith(".json"):
                fpath = blockers_dir / fname
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        b_data = json.load(f)
                        items = b_data if isinstance(b_data, list) else [b_data]
                        for b in items:
                            if isinstance(b, dict) and b.get("id"):
                                if b.get("status") == "resolved":
                                    resolved_map[b["id"]] = b
                                    active_map.pop(b["id"], None)
                                else:
                                    active_map[b["id"]] = b
                except Exception as e:
                    errors.append(f"Failed to parse canonical per-blocker file '{fpath.name}': {e}")

    fresh_aggregate: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "active": list(active_map.values()),
        "resolved": list(resolved_map.values()),
    }
    atomic_write_json(blockers_file, fresh_aggregate)
    print(f"Generated aggregate {blockers_file} from {len(fresh_aggregate['active'])} active and {len(fresh_aggregate['resolved'])} resolved canonical records")


def split_state(state_dir: Path):
    """Extract records from aggregate files into canonical per-task files."""
    tasks_file = state_dir / "tasks.json"
    gov_file = state_dir / "governance.json"
    events_file = state_dir / "events.jsonl"
    blockers_file = state_dir / "blockers.json"

    tasks_dir = state_dir / "tasks"
    gov_dir = state_dir / "governance"
    events_dir = state_dir / "events"
    blockers_dir = state_dir / "blockers"

    tasks_dir.mkdir(parents=True, exist_ok=True)
    gov_dir.mkdir(parents=True, exist_ok=True)
    events_dir.mkdir(parents=True, exist_ok=True)
    blockers_dir.mkdir(parents=True, exist_ok=True)

    if tasks_file.is_file():
        with open(tasks_file, "r", encoding="utf-8") as f:
            t_data = json.load(f)
            for t in t_data.get("tasks", []):
                t_id = t.get("id")
                if t_id:
                    atomic_write_json(tasks_dir / f"{t_id}.json", t)

    if gov_file.is_file():
        with open(gov_file, "r", encoding="utf-8") as f:
            g_data = json.load(f)
            for r in g_data.get("records", []):
                t_id = r.get("taskId")
                if t_id:
                    atomic_write_json(gov_dir / f"{t_id}.json", r)

    if events_file.is_file():
        events_by_task: Dict[str, List[Dict[str, Any]]] = {}
        with open(events_file, "r", encoding="utf-8") as f:
            for line in f:
                l = line.strip()
                if l:
                    ev = json.loads(l)
                    t_id = ev.get("taskId") or "__global__"
                    events_by_task.setdefault(t_id, []).append(ev)
        for t_id, evs in events_by_task.items():
            atomic_write_jsonl(events_dir / f"{t_id}.jsonl", evs)

    if blockers_file.is_file():
        with open(blockers_file, "r", encoding="utf-8") as f:
            b_data = json.load(f)
            for b in b_data.get("active", []) + b_data.get("resolved", []):
                b_id = b.get("id")
                if b_id:
                    atomic_write_json(blockers_dir / f"{b_id}.json", b)

    print(f"Split state into per-task files under {state_dir}")


def main():
    parser = argparse.ArgumentParser(description="Deterministic state aggregator and synchronizer")
    parser.add_argument("--state-dir", default=None, help="Path to .agents/state directory")
    parser.add_argument("--split", action="store_true", help="Split aggregate files into per-task files")
    args = parser.parse_args()

    if args.state_dir:
        state_dir = Path(args.state_dir).resolve()
    else:
        info = resolve_workspace()
        state_dir = info.state_root

    if not state_dir.is_dir():
        print(f"Error: State directory '{state_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.split:
        split_state(state_dir)
def rebuild_all_aggregates(state_dir: Path) -> bool:
    """Rebuild all aggregate state files purely from scratch from canonical files."""
    errors: List[str] = []
    aggregate_tasks(state_dir, errors)
    aggregate_governance(state_dir, errors)
    aggregate_events(state_dir, errors)
    aggregate_blockers(state_dir, errors)
    if errors:
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Deterministic state aggregator and synchronizer")
    parser.add_argument("--state-dir", default=None, help="Path to .agents/state directory")
    parser.add_argument("--split", action="store_true", help="Split aggregate files into per-task files")
    args = parser.parse_args()

    if args.state_dir:
        state_dir = Path(args.state_dir).resolve()
    else:
        info = resolve_workspace()
        state_dir = info.state_root

    if not state_dir.is_dir():
        print(f"Error: State directory '{state_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.split:
        split_state(state_dir)
    else:
        ok = rebuild_all_aggregates(state_dir)
        if not ok:
            sys.exit(1)


if __name__ == "__main__":
    main()
