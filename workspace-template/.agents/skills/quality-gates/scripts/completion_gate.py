#!/usr/bin/env python3
"""completion_gate.py

Authoritative, shared completion gate evaluator for Antigravity.
Delegates to .agents.validation.core.governance_core for unified completion evaluation.
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure core validation package is on sys.path
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from governance_core import evaluate_governance_completion, CompletionResult
    from workspace_resolver import resolve_workspace, WorkspaceInfo
    from verification_policy import is_substantive_evidence
except ImportError:
    try:
        from ...validation.core.governance_core import evaluate_governance_completion, CompletionResult
        from ...validation.core.workspace_resolver import resolve_workspace, WorkspaceInfo
        from ...validation.core.verification_policy import is_substantive_evidence
    except Exception:
        # Fallback if invoked from another path
        _alt_core = Path.cwd() / "workspace-template" / ".agents" / "validation" / "core"
        if _alt_core.is_dir() and str(_alt_core) not in sys.path:
            sys.path.insert(0, str(_alt_core))
        from governance_core import evaluate_governance_completion, CompletionResult
        from workspace_resolver import resolve_workspace, WorkspaceInfo
        from verification_policy import is_substantive_evidence


def resolve_workspace_root(workspace_paths: Optional[List[str]] = None) -> str:
    payload = {"workspacePaths": workspace_paths} if workspace_paths else None
    info = resolve_workspace(payload=payload)
    return str(info.project_root)


def find_state_dir(workspace_root: str) -> str:
    info = resolve_workspace(start_path=workspace_root)
    if info.state_root.is_dir():
        return str(info.state_root)
    return ""


def is_governed_workspace(workspace_root: str) -> bool:
    info = resolve_workspace(start_path=workspace_root)
    return info.is_governed


def evaluate_completion(
    workspace_root: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
    task_id_filter: Optional[str] = None,
    state_dir_override: Optional[str] = None,
) -> Dict[str, Any]:
    """Authoritative evaluation of task completion, returning dict."""
    res = evaluate_governance_completion(
        workspace_root=workspace_root,
        payload=payload,
        task_id_filter=task_id_filter,
        state_dir_override=state_dir_override,
    )
    return res.to_dict()


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
