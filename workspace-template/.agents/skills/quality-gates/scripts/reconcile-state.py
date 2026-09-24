#!/usr/bin/env python3
"""
reconcile-state.py

Authoritative state reconciliation and drift detection tool (P1-05, P1-06).
Verifies and synchronizes canonical per-task state (.agents/state/tasks/*.json,
.agents/state/governance/*.json, .agents/state/events/*.jsonl, .agents/state/blockers/*.json)
with derived aggregate state files (tasks.json, governance.json, events.jsonl, blockers.json).

Uses:
  - Canonical record normalization + SHA-256 full content comparison
  - Exact field difference and ordering difference detection
  - Event stream parity checking
  - Atomic rebuild from scratch via aggregate-state.py on --fix
  - Workspace resolver integration

Modes:
  --check    Detect drift and report discrepancies (exit 0 if clean, exit 1 if drift)
  --fix      Reconcile and regenerate derived aggregates from canonical per-task state
"""

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

# Add core validation package to sys.path
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from workspace_resolver import resolve_workspace
except ImportError:
    try:
        from .workspace_resolver import resolve_workspace
    except ImportError:
        resolve_workspace = None


def canonical_json_hash(obj: Any) -> str:
    """Normalize object to sorted canonical JSON and return SHA-256 hex digest (P1-05)."""
    norm = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def find_field_differences(prefix: str, d1: Dict[str, Any], d2: Dict[str, Any]) -> List[str]:
    """Find specific key/value differences between two dictionaries."""
    diffs = []
    all_keys = sorted(set(d1.keys()) | set(d2.keys()))
    for k in all_keys:
        val1 = d1.get(k)
        val2 = d2.get(k)
        if k not in d1:
            diffs.append(f"{prefix}missing key in canonical: '{k}' (aggregate={val2!r})")
        elif k not in d2:
            diffs.append(f"{prefix}missing key in aggregate: '{k}' (canonical={val1!r})")
        elif canonical_json_hash(val1) != canonical_json_hash(val2):
            diffs.append(f"{prefix}field '{k}' mismatch: canonical={val1!r} vs aggregate={val2!r}")
    return diffs


def resolve_state_path(override: Optional[str] = None) -> Path:
    if override:
        return Path(override).resolve()
    if resolve_workspace is not None:
        try:
            ws = resolve_workspace()
            return ws.state_root
        except Exception:
            pass
    for cand in [Path(".agents/state"), Path("workspace-template/.agents/state")]:
        if cand.is_dir():
            return cand.resolve()
    return Path(".agents/state").resolve()


def check_tasks_drift(state_dir: Path) -> Tuple[List[str], Dict[str, Any]]:
    discrepancies: List[str] = []
    tasks_dir = state_dir / "tasks"
    tasks_file = state_dir / "tasks.json"

    canonical_tasks: Dict[str, Dict[str, Any]] = {}
    if tasks_dir.is_dir():
        for fpath in sorted(tasks_dir.glob("*.json")):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data.get("id"):
                        canonical_tasks[data["id"]] = data
            except Exception as e:
                discrepancies.append(f"Unreadable canonical task file '{fpath.name}': {e}")

    aggregate_tasks: Dict[str, Dict[str, Any]] = {}
    if tasks_file.is_file():
        try:
            with open(tasks_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
                for t in raw.get("tasks", []):
                    if isinstance(t, dict) and t.get("id"):
                        aggregate_tasks[t["id"]] = t
        except Exception as e:
            discrepancies.append(f"Unreadable aggregate tasks file 'tasks.json': {e}")
    elif canonical_tasks:
        discrepancies.append("Aggregate tasks file 'tasks.json' missing while canonical tasks exist")

    # Missing in aggregate
    for tid, ctask in canonical_tasks.items():
        if tid not in aggregate_tasks:
            discrepancies.append(f"Task '{tid}' exists in canonical state but is missing from tasks.json")
        else:
            atask = aggregate_tasks[tid]
            if canonical_json_hash(ctask) != canonical_json_hash(atask):
                diffs = find_field_differences(f"Task '{tid}' ", ctask, atask)
                discrepancies.extend(diffs)

    # Extra in aggregate
    for tid in aggregate_tasks:
        if tid not in canonical_tasks and tasks_dir.is_dir() and any(tasks_dir.glob("*.json")):
            discrepancies.append(f"Extra task '{tid}' exists in tasks.json with no canonical per-task file")

    return discrepancies, canonical_tasks


def check_governance_drift(state_dir: Path) -> Tuple[List[str], Dict[str, Any]]:
    discrepancies: List[str] = []
    gov_dir = state_dir / "governance"
    gov_file = state_dir / "governance.json"

    canonical_gov: Dict[str, Dict[str, Any]] = {}
    if gov_dir.is_dir():
        for fpath in sorted(gov_dir.glob("*.json")):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and data.get("taskId"):
                        canonical_gov[data["taskId"]] = data
            except Exception as e:
                discrepancies.append(f"Unreadable canonical governance file '{fpath.name}': {e}")

    aggregate_gov: Dict[str, Dict[str, Any]] = {}
    if gov_file.is_file():
        try:
            with open(gov_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
                for r in raw.get("records", []):
                    if isinstance(r, dict) and r.get("taskId"):
                        aggregate_gov[r["taskId"]] = r
        except Exception as e:
            discrepancies.append(f"Unreadable aggregate governance file 'governance.json': {e}")
    elif canonical_gov:
        discrepancies.append("Aggregate governance file 'governance.json' missing while canonical records exist")

    for tid, crec in canonical_gov.items():
        if tid not in aggregate_gov:
            discrepancies.append(f"Governance record '{tid}' exists in canonical state but missing from governance.json")
        else:
            arec = aggregate_gov[tid]
            if canonical_json_hash(crec) != canonical_json_hash(arec):
                diffs = find_field_differences(f"Governance record '{tid}' ", crec, arec)
                discrepancies.extend(diffs)

    for tid in aggregate_gov:
        if tid not in canonical_gov and gov_dir.is_dir() and any(gov_dir.glob("*.json")):
            discrepancies.append(f"Extra governance record '{tid}' in governance.json with no canonical record")

    return discrepancies, canonical_gov


def check_blockers_drift(state_dir: Path) -> Tuple[List[str], Dict[str, Any], Dict[str, Any]]:
    discrepancies: List[str] = []
    blockers_dir = state_dir / "blockers"
    blockers_file = state_dir / "blockers.json"

    canonical_active: Dict[str, Dict[str, Any]] = {}
    canonical_resolved: Dict[str, Dict[str, Any]] = {}

    if blockers_dir.is_dir():
        for fpath in sorted(blockers_dir.glob("*.json")):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    items = data if isinstance(data, list) else [data]
                    for b in items:
                        if isinstance(b, dict) and b.get("id"):
                            if b.get("status") == "resolved":
                                canonical_resolved[b["id"]] = b
                                canonical_active.pop(b["id"], None)
                            else:
                                canonical_active[b["id"]] = b
            except Exception as e:
                discrepancies.append(f"Unreadable canonical blocker file '{fpath.name}': {e}")

    aggregate_active: Dict[str, Dict[str, Any]] = {}
    aggregate_resolved: Dict[str, Dict[str, Any]] = {}
    if blockers_file.is_file():
        try:
            with open(blockers_file, "r", encoding="utf-8") as f:
                b_raw = json.load(f)
                for b in b_raw.get("active", []):
                    if isinstance(b, dict) and b.get("id"):
                        aggregate_active[b["id"]] = b
                for b in b_raw.get("resolved", []):
                    if isinstance(b, dict) and b.get("id"):
                        aggregate_resolved[b["id"]] = b
        except Exception as e:
            discrepancies.append(f"Unreadable aggregate blockers file 'blockers.json': {e}")

    for bid, cblk in canonical_active.items():
        if bid not in aggregate_active:
            discrepancies.append(f"Active blocker '{bid}' missing from aggregate blockers.json")
        else:
            ablk = aggregate_active[bid]
            if canonical_json_hash(cblk) != canonical_json_hash(ablk):
                diffs = find_field_differences(f"Active blocker '{bid}' ", cblk, ablk)
                discrepancies.extend(diffs)

    for bid, cblk in canonical_resolved.items():
        if bid not in aggregate_resolved:
            discrepancies.append(f"Resolved blocker '{bid}' missing from aggregate blockers.json")
        else:
            ablk = aggregate_resolved[bid]
            if canonical_json_hash(cblk) != canonical_json_hash(ablk):
                diffs = find_field_differences(f"Resolved blocker '{bid}' ", cblk, ablk)
                discrepancies.extend(diffs)

    for bid in aggregate_active:
        if bid not in canonical_active:
            discrepancies.append(f"Extra active blocker '{bid}' in blockers.json with no canonical record")

    for bid in aggregate_resolved:
        if bid not in canonical_resolved:
            discrepancies.append(f"Extra resolved blocker '{bid}' in blockers.json with no canonical record")

    return discrepancies, canonical_active, canonical_resolved


def check_events_drift(state_dir: Path) -> List[str]:
    discrepancies: List[str] = []
    events_dir = state_dir / "events"
    events_file = state_dir / "events.jsonl"

    canonical_events: List[Dict[str, Any]] = []
    if events_dir.is_dir():
        for fpath in sorted(events_dir.glob("*.jsonl")):
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    for line in f:
                        l = line.strip()
                        if l:
                            ev = json.loads(l)
                            if isinstance(ev, dict):
                                canonical_events.append(ev)
            except Exception as e:
                discrepancies.append(f"Unreadable canonical event file '{fpath.name}': {e}")

    # Canonical order: sorted by sequence if present, else timestamp
    def event_sort_key(ev: Dict[str, Any]):
        return (ev.get("sequence", 0), ev.get("timestamp", ""))

    canonical_events.sort(key=event_sort_key)

    aggregate_events: List[Dict[str, Any]] = []
    if events_file.is_file():
        try:
            with open(events_file, "r", encoding="utf-8") as f:
                for line in f:
                    l = line.strip()
                    if l:
                        ev = json.loads(l)
                        if isinstance(ev, dict):
                            aggregate_events.append(ev)
        except Exception as e:
            discrepancies.append(f"Unreadable aggregate events file 'events.jsonl': {e}")
    elif canonical_events:
        discrepancies.append("Aggregate events file 'events.jsonl' missing while canonical events exist")

    if len(canonical_events) != len(aggregate_events):
        discrepancies.append(
            f"Event count mismatch: canonical has {len(canonical_events)} events vs aggregate has {len(aggregate_events)}"
        )
    else:
        for idx, (cev, aev) in enumerate(zip(canonical_events, aggregate_events)):
            if canonical_json_hash(cev) != canonical_json_hash(aev):
                discrepancies.append(
                    f"Event index {idx} mismatch: canonical sequence={cev.get('sequence')}, event={cev.get('event')} "
                    f"vs aggregate sequence={aev.get('sequence')}, event={aev.get('event')}"
                )

    return discrepancies


def run_fix_aggregates(state_dir: Path) -> bool:
    """Rebuild all derived aggregates from canonical source using aggregate-state.py."""
    agg_script = _script_dir / "aggregate-state.py"
    if not agg_script.is_file():
        print(f"Error: Aggregator script '{agg_script}' not found.", file=sys.stderr)
        return False

    spec = importlib.util.spec_from_file_location("aggregate_state", str(agg_script))
    if not spec or not spec.loader:
        print("Error: Could not load aggregate-state module.", file=sys.stderr)
        return False

    agg_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(agg_mod)

    success = agg_mod.rebuild_all_aggregates(state_dir)
    return success


def main():
    parser = argparse.ArgumentParser(description="Reconcile and detect drift in state files (P1-05, P1-06)")
    parser.add_argument("--state-dir", default=None, help="Path to .agents/state directory")
    parser.add_argument("--check", action="store_true", help="Check for drift without modifying files")
    parser.add_argument("--fix", action="store_true", help="Reconcile derived aggregates from canonical state")
    args = parser.parse_args()

    state_dir = resolve_state_path(args.state_dir)
    if not state_dir.is_dir():
        print(f"Error: State directory '{state_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    task_disc, _ = check_tasks_drift(state_dir)
    gov_disc, _ = check_governance_drift(state_dir)
    blk_disc, _, _ = check_blockers_drift(state_dir)
    evt_disc = check_events_drift(state_dir)

    all_discrepancies = task_disc + gov_disc + blk_disc + evt_disc

    if args.check:
        if all_discrepancies:
            print(f"[DRIFT DETECTED] Found {len(all_discrepancies)} discrepancy(s) in state:")
            for d in all_discrepancies:
                print(f"  - {d}")
            sys.exit(1)
        else:
            print("[STATE CLEAN] Canonical per-task state and derived aggregates are in full parity.")
            sys.exit(0)
    else:
        # Rebuild mode (--fix or default)
        if all_discrepancies:
            print(f"Reconciling {len(all_discrepancies)} drift discrepancy(s)...")
            for d in all_discrepancies:
                print(f"  Drift: {d}")
        else:
            print("No drift detected. Regenerating clean aggregates from canonical source...")

        ok = run_fix_aggregates(state_dir)
        if ok:
            print(f"Reconciliation complete. Derived aggregates synchronized from canonical state in '{state_dir}'.")
            sys.exit(0)
        else:
            print("Reconciliation failed during aggregate rebuild.", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
