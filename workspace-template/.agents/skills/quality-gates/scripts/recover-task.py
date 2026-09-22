#!/usr/bin/env python3
"""recover-task.py

Deterministic Task Recovery & Remediation Tool:
- P0-10: Emits strictly schematized recovery events (TASK_RECOVERED_RESET, TASK_RESUMED, TASK_RECOVERED_FAILED)
  conforming to events.schema.json without arbitrary payload properties.
- P0-11: Mutates ONLY canonical per-task state (.agents/state/tasks/TASK-xxx.json) and
  canonical per-task events (.agents/state/events/TASK-xxx.jsonl), then triggers scratch aggregation.
- P0-12: Fails closed on Git errors (never interprets git failure as clean tree).
- P0-13: Enforces strict recovery transition matrix (COMPLETED/CANCELLED can never be auto-resumed).
- P0-31, P0-32: Standardized deterministic workspace resolution via workspace_resolver.py.
"""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, List, Optional, Tuple

# Add core validation package to sys.path
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from workspace_resolver import resolve_workspace
except ImportError:
    from .workspace_resolver import resolve_workspace

import importlib.util
_agg_spec = importlib.util.spec_from_file_location("aggregate_state", str(_script_dir / "aggregate-state.py"))
_agg_mod = importlib.util.module_from_spec(_agg_spec)
_agg_spec.loader.exec_module(_agg_mod)
aggregate_tasks = _agg_mod.aggregate_tasks
aggregate_events = _agg_mod.aggregate_events

# P0-13: Transition Matrix
VALID_RECOVERY_TRANSITIONS = {
    "IN_PROGRESS": {"resume", "reset", "fail", "block"},
    "TESTING": {"resume", "reset", "fail", "block"},
    "VERIFYING": {"resume", "reset", "fail", "block"},
    "REVIEWING": {"resume", "reset", "fail", "block"},
    "BLOCKED": {"resume", "reset", "fail", "block"},
    "FAILED": {"reset"},  # Failed tasks can be explicitly reset
    "COMPLETED": set(),   # NEVER auto-resume or reset completed tasks
    "CANCELLED": set(),   # NEVER auto-resume or reset cancelled tasks
}


def get_current_iso_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def check_git_status(cwd: Path) -> Tuple[Optional[List[str]], Optional[str]]:
    """Check working tree status. Returns (files, error_str).

    P0-12: Fails closed on Git errors (returns None for files, non-empty error).
    """
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
        if res.returncode != 0:
            return None, f"git status exited with code {res.returncode}: {res.stderr.strip()}"
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        return lines, None
    except Exception as e:
        return None, f"Failed to execute git status: {e}"


def load_canonical_task(state_dir: Path, task_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """P0-11: Read ONLY canonical task state."""
    task_file = state_dir / "tasks" / f"{task_id}.json"
    if not task_file.is_file():
        return None, f"Canonical task file '{task_file}' does not exist."
    try:
        with open(task_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data, None
        return None, f"Canonical task file '{task_file}' contains invalid data structure."
    except Exception as e:
        return None, f"Failed to parse canonical task file '{task_file}': {e}"


def save_canonical_task(state_dir: Path, task: Dict[str, Any]):
    """P0-11: Save ONLY canonical task state via atomic write."""
    task_id = task["id"]
    tasks_dir = state_dir / "tasks"
    tasks_dir.mkdir(parents=True, exist_ok=True)
    task_path = tasks_dir / f"{task_id}.json"

    import tempfile
    with tempfile.NamedTemporaryFile("w", dir=str(tasks_dir), delete=False, encoding="utf-8") as tf:
        temp_name = tf.name
        json.dump(task, tf, indent=2)
        tf.write("\n")
        tf.flush()
        os.fsync(tf.fileno())

    os.replace(temp_name, str(task_path))


def append_canonical_event(
    state_dir: Path,
    task_id: str,
    event_name: str,
    recovery_action: str,
    previous_status: str,
    details_str: str,
):
    """P0-10: Emit formal recovery event conforming strictly to events.schema.json."""
    events_dir = state_dir / "events"
    events_dir.mkdir(parents=True, exist_ok=True)
    ev_path = events_dir / f"{task_id}.jsonl"

    count = 0
    if ev_path.is_file():
        try:
            with open(ev_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        count += 1
        except Exception:
            pass

    seq = count + 1
    event_id = f"EVT-{seq:06d}"

    ev_record = {
        "eventId": event_id,
        "sequence": seq,
        "timestamp": get_current_iso_timestamp(),
        "source": "recover-task.py",
        "taskId": task_id,
        "event": event_name,
        "recoveryAction": recovery_action,
        "previousStatus": previous_status,
        "details": details_str,
    }

    with open(ev_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev_record) + "\n")
        f.flush()


def main():
    parser = argparse.ArgumentParser(description="Deterministic task recovery and interruption remediation tool")
    parser.add_argument("--task-id", help="Task ID to recover (e.g. TASK-101)")
    parser.add_argument("--state-dir", default=None, help="Path to .agents/state directory")
    parser.add_argument(
        "--action",
        choices=["auto", "reset", "resume", "fail", "block"],
        default="auto",
        help="Recovery action to take (default: auto)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Diagnose without making state changes")
    args = parser.parse_args()

    if args.state_dir:
        state_dir = Path(args.state_dir).resolve()
        project_root = state_dir.parent.parent
    else:
        info = resolve_workspace()
        state_dir = info.state_root
        project_root = info.project_root

    if not state_dir.is_dir():
        print(f"Error: State directory '{state_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    task_id = args.task_id
    if not task_id:
        # Search canonical tasks/ for active IN_PROGRESS task
        tasks_dir = state_dir / "tasks"
        if tasks_dir.is_dir():
            for fname in sorted(os.listdir(tasks_dir)):
                if fname.endswith(".json"):
                    try:
                        with open(tasks_dir / fname, "r", encoding="utf-8") as f:
                            t = json.load(f)
                            if t.get("status") in {"IN_PROGRESS", "TESTING", "VERIFYING"}:
                                task_id = t.get("id")
                                break
                    except Exception:
                        pass

    if not task_id:
        print("No active or specified task to recover. All tasks are idle, complete, or clean.")
        sys.exit(0)

    task, err = load_canonical_task(state_dir, task_id)
    if not task:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)

    status = task.get("status", "UNKNOWN")

    # Check Git working tree (P0-12)
    git_files, git_err = check_git_status(project_root)

    print(f"=== Task Recovery Diagnosis for {task_id} ===")
    print(f"Current Status: {status}")
    if git_err:
        print(f"Git Status: ERROR ({git_err})")
    else:
        print(f"Working Tree Changes: {len(git_files)} modified/untracked files")
        for f in git_files[:5]:
            print(f"  {f}")

    # P0-13: Transition Matrix Check
    allowed_actions = VALID_RECOVERY_TRANSITIONS.get(status, set())
    if not allowed_actions:
        print(
            f"Error: Task '{task_id}' is in terminal/immutable state '{status}'. "
            f"Recovery transitions from '{status}' are strictly forbidden.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Determine recovery action
    action = args.action
    if action == "auto":
        # P0-12: If git status failed, fail closed! Do NOT auto-reset.
        if git_err:
            print(
                f"Error: Cannot determine automatic recovery action because git status failed ({git_err}). "
                f"Failing closed to prevent accidental data loss. Please specify explicit --action after repairing Git state.",
                file=sys.stderr,
            )
            sys.exit(1)

        if status in {"IN_PROGRESS", "TESTING", "VERIFYING", "REVIEWING"}:
            if git_files:
                action = "resume"
            else:
                action = "reset"
        elif status == "BLOCKED":
            action = "block"
        elif status == "FAILED":
            action = "reset"
        else:
            action = "resume"

    if action not in allowed_actions:
        print(
            f"Error: Action '{action}' is not permitted for task in status '{status}'. "
            f"Allowed actions: {sorted(list(allowed_actions))}",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Recommended Action: {action.upper()}")

    if args.dry_run:
        print("[DRY-RUN] No changes made.")
        sys.exit(0)

    # Apply recovery action
    previous_status = status
    if action == "reset":
        task["status"] = "READY"
        task["updatedAt"] = get_current_iso_timestamp()
        save_canonical_task(state_dir, task)
        append_canonical_event(
            state_dir,
            task_id,
            "TASK_RECOVERED_RESET",
            recovery_action="reset",
            previous_status=previous_status,
            details_str="Interrupted task reset to READY due to clean working tree or explicit reset instruction.",
        )
        print(f"Task {task_id} successfully reset to READY.")
    elif action == "resume":
        task["status"] = "IN_PROGRESS"
        task["updatedAt"] = get_current_iso_timestamp()
        save_canonical_task(state_dir, task)
        append_canonical_event(
            state_dir,
            task_id,
            "TASK_RESUMED",
            recovery_action="resume",
            previous_status=previous_status,
            details_str=f"Interrupted task resumed in IN_PROGRESS with {len(git_files) if git_files else 0} uncommitted changes.",
        )
        print(f"Task {task_id} marked IN_PROGRESS to resume execution.")
    elif action == "fail":
        task["status"] = "FAILED"
        task["updatedAt"] = get_current_iso_timestamp()
        save_canonical_task(state_dir, task)
        append_canonical_event(
            state_dir,
            task_id,
            "TASK_RECOVERED_FAILED",
            recovery_action="fail",
            previous_status=previous_status,
            details_str="Task manually or policy-marked FAILED during recovery.",
        )
        print(f"Task {task_id} marked FAILED.")
    elif action == "block":
        task["status"] = "BLOCKED"
        task["updatedAt"] = get_current_iso_timestamp()
        save_canonical_task(state_dir, task)
        append_canonical_event(
            state_dir,
            task_id,
            "TASK_BLOCKED",
            recovery_action="block",
            previous_status=previous_status,
            details_str="Task marked BLOCKED pending resolution of active blockers.",
        )
        print(f"Task {task_id} marked BLOCKED.")

    # P0-11: Trigger scratch aggregate update from canonical records
    agg_errors: List[str] = []
    aggregate_tasks(state_dir, agg_errors)
    aggregate_events(state_dir, agg_errors)
    if agg_errors:
        print(f"Warning: Aggregate sync reported errors: {agg_errors}", file=sys.stderr)


if __name__ == "__main__":
    main()
