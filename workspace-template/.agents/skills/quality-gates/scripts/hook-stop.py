#!/usr/bin/env python3
"""hook-stop.py

Antigravity Stop Lifecycle Hook:
- Authoritative Stop Hook enforcing P0-01, P0-02, P0-03 invariants.
- Uses completion_gate.py (governance_core.py) as the single authoritative completion evaluator.
- Strictly task-scoped (P0-02).
- Enforces fullyIdle == True (P0-03).
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

# Ensure current script dir and core validation package are on sys.path
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
for d in [_script_dir, _core_dir]:
    if d.is_dir() and str(d) not in sys.path:
        sys.path.insert(0, str(d))

try:
    from completion_gate import evaluate_completion
except ImportError:
    from .completion_gate import evaluate_completion


def check_stop_conditions(
    state_dir: str = "",
    workspace_root: str = "",
    payload: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Wrapper function preserving invocation signature while delegating to authoritative completion gate."""
    if payload is None:
        # Default fullyIdle to True for direct Python API invocation when payload is omitted
        payload = {"fullyIdle": True}

    if not workspace_root and state_dir:
        workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(state_dir)))
    state_override = state_dir if state_dir else None
    return evaluate_completion(
        workspace_root=workspace_root,
        payload=payload,
        state_dir_override=state_override,
    )


def main():
    try:
        raw_input = sys.stdin.read()
        payload = json.loads(raw_input) if raw_input.strip() else {}
    except Exception:
        payload = {}

    result = evaluate_completion(payload=payload)
    print(json.dumps(result))
    sys.exit(0 if result.get("decision") == "allow" else 1)


if __name__ == "__main__":
    main()
