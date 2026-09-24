#!/usr/bin/env python3
"""hook-pre-tool.py

Antigravity PreToolUse Lifecycle Hook:
- P0-14, P0-15: Protects framework control-plane (.agents/**, AGENTS.md, .github/workflows/**, CODEOWNERS).
- P0-17: Canonicalizes all file paths via realpath/abspath against traversal (../), symlinks, and alternate separators.
- P0-18: Inspects all mutation tools (run_command, write_to_file, replace_file_content, multi_replace_file_content).
- P0-19: Fails closed on malformed or empty inputs.
- Enforces runtime safety guardrails and least privilege.
"""

import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, Optional, Tuple

# Add core validation package to sys.path
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from workspace_resolver import resolve_workspace
except ImportError:
    from .workspace_resolver import resolve_workspace

# Catastrophic shell patterns that must be immediately DENIED
CATASTROPHIC_PATTERNS = [
    (r"\brm\s+-[a-zA-Z]*[rfRF][a-zA-Z]*\s+/(?:\s+|$|\*)", "Blocking attempt to delete filesystem root."),
    (r"\brm\s+-[a-zA-Z]*[rfRF][a-zA-Z]*\s+(?:~|\$HOME|\$\{HOME\})(?:\s+|$|\*)", "Blocking attempt to delete user home directory."),
    (r"\bmkfs(?:\.[a-z0-9]+)?\b", "Blocking disk formatting command."),
    (r"\bdd\s+if=.*\s+of=/dev/", "Blocking raw disk write operation via dd."),
    (r":\(\)\s*\{\s*:\|:&\s*\};:", "Blocking shell fork bomb."),
    (r">\s*/dev/(?:sd[a-z]|nvme[0-9]|hd[a-z])", "Blocking direct overwrite of block storage device."),
    (r"\bchmod\s+-[a-zA-Z]*[rR][a-zA-Z]*\s+(?:000|777)\s+/(?:\s+|$|\*)", "Blocking destructive root permission alteration."),
    (r"(?:curl|wget)\s+[^|]+\|\s*sudo\s+(?:ba)?sh", "Blocking unverified pipe of remote script to root shell."),
]

# High-risk shell patterns that require explicit user confirmation (FORCE_ASK)
HIGH_RISK_PATTERNS = [
    (r"\bgit\s+push\s+.*(?:--force|-f)\b", "Force-pushing to remote git repository requires explicit confirmation."),
    (r"\bgit\s+reset\s+--hard\s+origin/", "Hard reset to remote tracking branch requires explicit confirmation."),
    (r"\bDROP\s+(?:DATABASE|SCHEMA)\b", "Dropping an entire database or schema requires explicit confirmation."),
]

# Sensitive file path patterns:
# Hard DENY patterns (automated tools must never directly touch)
DENIED_PATH_PATTERNS = [
    (r"(?:^|/)\.git/(?!info/exclude)", "Direct modification of .git internals is prohibited; use git CLI commands."),
    (r"\.(?:pem|key|pfx|p12|pkcs12)$", "Direct authorship of private key or cryptographic certificate files is prohibited."),
]

# High-risk file path patterns that require user confirmation (FORCE_ASK)
# Covers control-plane (P0-14, P0-15), secrets, CI workflows, and prod infrastructure
HIGH_RISK_PATH_PATTERNS = [
    (r"(?:^|/)\.agents/.*", "Modifying framework governance control-plane (.agents/) requires explicit human confirmation."),
    (r"(?:^|/)AGENTS\.md$", "Modifying core agent operating instructions (AGENTS.md) requires explicit human confirmation."),
    (r"(?:^|/)CODEOWNERS$", "Modifying CODEOWNERS policy requires explicit human confirmation."),
    (r"(?:^|/)\.env(?:\.[a-zA-Z0-9_-]+)?$", "Modification of environment secret file (.env) requires explicit confirmation."),
    (r"(?:^|/)(?:credentials|secrets)(?:\.[a-zA-Z0-9_-]+)?$", "Modification of credentials or secrets file requires explicit confirmation."),
    (r"(?:^|/)\.github/workflows/.*\.ya?ml$", "Modifying CI/CD pipeline workflows requires explicit confirmation."),
    (r"(?:^|/)(?:infra|infrastructure|terraform)/prod(?:uction)?/.*", "Modifying production infrastructure definitions requires explicit confirmation."),
    (r"\.tfstate(?:\.backup)?$", "Modifying Terraform state files requires explicit confirmation."),
]


def canonicalize_path(raw_path: str, workspace_root: Optional[Path] = None) -> Tuple[str, str]:
    """P0-17: Normalize, resolve, realpath, and compute workspace-relative path.

    Returns:
        (canonical_abs_path, canonical_rel_path)
    """
    raw_clean = raw_path.strip().replace("\\", "/")
    p = Path(raw_clean)

    if not p.is_absolute():
        if workspace_root:
            p = workspace_root / p
        else:
            p = Path.cwd() / p

    try:
        resolved_abs = str(p.resolve())
    except Exception:
        resolved_abs = str(os.path.abspath(str(p)))

    # Compute relative to workspace_root if possible
    if workspace_root:
        try:
            rel = os.path.relpath(resolved_abs, str(workspace_root.resolve())).replace("\\", "/")
        except Exception:
            rel = raw_clean
    else:
        rel = raw_clean

    return resolved_abs.replace("\\", "/"), rel


def load_tool_registry(workspace_root: Path) -> Dict[str, Dict[str, Any]]:
    """Load the platform adapter registry; unknown tools are unsafe by default."""
    candidates = [
        workspace_root / ".agents" / "orchestration" / "antigravity-tool-registry.json",
        Path(__file__).resolve().parents[3] / "orchestration" / "antigravity-tool-registry.json",
    ]
    for candidate in candidates:
        try:
            if candidate.is_file():
                data = json.loads(candidate.read_text(encoding="utf-8"))
                tools = data.get("tools")
                if isinstance(tools, dict):
                    return tools
        except Exception:
            continue
    return {}


EXECUTION_MUTATION_STATUSES = {
    "IN_PROGRESS", "TESTING", "VERIFYING", "REVIEWING", "MEMORY_SYNC", "STATE_SYNC", "GOVERNANCE_CHECK"
}
STATE_WRITE_PREFIXES = (".agents/state/",)
REPO_MUTATION_COMMAND_PATTERNS = [
    r"\bsed\s+-[a-zA-Z]*i\b",
    r"\bperl\s+-[a-zA-Z]*i\b",
    r"(?:^|[;&|\s])(?:cat|printf|echo)\b[^;\n]*>\s*(?:\./|/|[A-Za-z0-9_.-]+/)",
    r"\b(?:python|python3)\b[^;\n]*\b(?:open\(|write_text\(|write_bytes\(|unlink\()",
    r"\bnode\b[^;\n]*\b(?:writeFile|writeFileSync|rmSync|unlink)\b",
    r"\bgit\s+(?:apply|checkout|restore|clean|mv|rm|commit|merge|rebase|cherry-pick)\b",
    r"\b(?:npm|pnpm|yarn)\s+(?:install|add|remove|uninstall|update|upgrade|pkg\s+set)\b",
    r"\b(?:composer|pip|poetry)\s+(?:install|update|add|remove)\b",
]

def _safe_conversation_id(conversation_id: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", conversation_id or "unknown")[:180] or "unknown"


def active_task_status(workspace_root: Path, conversation_id: str = "") -> Tuple[Optional[str], Optional[str]]:
    runtime_dir = workspace_root / ".agents" / "state" / "runtime"
    session_file = runtime_dir / "sessions" / f"{_safe_conversation_id(conversation_id)}.json" if conversation_id else runtime_dir / "session.json"
    if not session_file.is_file():
        return None, None
    try:
        session = json.loads(session_file.read_text(encoding="utf-8"))
        task_id = session.get("activeTaskId")
        if not task_id:
            return None, None
        task_file = workspace_root / ".agents" / "state" / "tasks" / f"{task_id}.json"
        if not task_file.is_file():
            return task_id, None
        task = json.loads(task_file.read_text(encoding="utf-8"))
        return task_id, task.get("status")
    except Exception:
        return None, None

def requires_execution_task(status: Optional[str]) -> bool:
    return status not in EXECUTION_MUTATION_STATUSES

def is_repo_mutation_command(command: str) -> bool:
    return any(re.search(pattern, command, re.IGNORECASE) for pattern in REPO_MUTATION_COMMAND_PATTERNS)


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            # P0-19: Malformed/empty input in governed mode fails closed
            print(json.dumps({
                "decision": "force_ask",
                "reason": "[GOVERNANCE GUARD] PreToolUse received empty invocation payload. Confirmation required."
            }))
            return

        payload = json.loads(raw_input)
    except Exception as e:
        # P0-19: Fail closed on unparseable input
        print(json.dumps({
            "decision": "deny",
            "reason": f"[SECURITY GUARDRAIL] PreToolUse hook failed to parse input JSON: {e}"
        }))
        return

    tool_call = payload.get("toolCall", {})
    if not isinstance(tool_call, dict):
        tool_call = {}
    tool_name = tool_call.get("name") or payload.get("toolName") or ""
    if not isinstance(tool_name, str) or not tool_name.strip():
        print(json.dumps({
            "decision": "force_ask",
            "reason": "[GOVERNANCE GUARD] PreToolUse received payload without a valid tool name. Confirmation required."
        }))
        return

    args = tool_call.get("args") or {}
    if not isinstance(args, dict):
        args = {}

    workspace_paths = payload.get("workspacePaths", [])
    ws_info = resolve_workspace(payload={"workspacePaths": workspace_paths})
    ws_root = ws_info.project_root
    tool_registry = load_tool_registry(ws_root)
    conversation_id = str(payload.get("conversationId") or "")
    active_task_id, task_status = active_task_status(ws_root, conversation_id)

    # New/unregistered tools must never inherit an implicit allow decision.
    if tool_name not in tool_registry:
        print(json.dumps({
            "decision": "force_ask",
            "reason": f"[GOVERNANCE GUARD] Tool {tool_name!r} is not registered in the platform adapter registry. Explicit confirmation is required."
        }))
        return

    registry_entry = tool_registry.get(tool_name)
    required_metadata = {"capability", "access", "risk", "supportedAgentTypes"}
    if not isinstance(registry_entry, dict) or not required_metadata.issubset(registry_entry):
        print(json.dumps({
            "decision": "deny",
            "reason": f"[GOVERNANCE GUARD] Tool {tool_name!r} has incomplete registry metadata. Control-plane repair is required before execution."
        }))
        return

    # 1. Inspect command execution calls
    if tool_name in {"run_command", "bash", "terminal", "execute_command"}:
        cmd = args.get("CommandLine") or args.get("command") or args.get("cmd") or ""
        if isinstance(cmd, str) and cmd.strip():
            # Check catastrophic patterns -> DENY
            for pattern, reason in CATASTROPHIC_PATTERNS:
                if re.search(pattern, cmd, re.IGNORECASE):
                    print(json.dumps({
                        "decision": "deny",
                        "reason": f"[SECURITY GUARDRAIL] Execution DENIED: {reason} Command: '{cmd.strip()}'"
                    }))
                    return

            # Repository-mutating shell commands require an execution-state task.
            # Read-only inspection/test commands remain available before implementation.
            if is_repo_mutation_command(cmd) and not ws_info.is_governed:
                pass
            elif is_repo_mutation_command(cmd) and requires_execution_task(task_status):
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"[GOVERNANCE GUARD] Repository-mutating command blocked: active task must be in an execution state before mutation (task={active_task_id or 'none'}, status={task_status or 'none'})."
                }))
                return

            # Check high-risk patterns -> FORCE_ASK
            for pattern, reason in HIGH_RISK_PATTERNS:
                if re.search(pattern, cmd, re.IGNORECASE):
                    print(json.dumps({
                        "decision": "force_ask",
                        "reason": f"[HIGH-RISK ACTION] {reason} Command: '{cmd.strip()}'"
                    }))
                    return

    # 2. Inspect file modification calls (P0-18)
    if tool_name in {"write_to_file", "replace_file_content", "multi_replace_file_content", "edit_file"}:
        target_file = (
            args.get("TargetFile")
            or args.get("target_file")
            or args.get("path")
            or args.get("filePath")
            or ""
        )
        if isinstance(target_file, str) and target_file.strip():
            # P0-17: Canonicalize path against traversal, symlinks, and relative offsets
            abs_path, rel_path = canonicalize_path(target_file, ws_root)
            paths_to_test = [target_file.strip().replace("\\", "/"), rel_path, abs_path]

            # Canonical state is writable during lifecycle bookkeeping.
            is_state_write = rel_path.startswith(STATE_WRITE_PREFIXES)

            # Hard DENY any path escaping the workspace boundary (P0-17)
            if rel_path.startswith("..") or (ws_root and not abs_path.startswith(str(ws_root.resolve()))):
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"[SECURITY GUARDRAIL] Path traversal outside workspace boundary is prohibited: '{target_file.strip()}'"
                }))
                return

            # Check hard-denied file paths -> DENY
            for pattern, reason in DENIED_PATH_PATTERNS:
                for p_str in paths_to_test:
                    if re.search(pattern, p_str, re.IGNORECASE):
                        print(json.dumps({
                            "decision": "deny",
                            "reason": f"[SECURITY GUARDRAIL] Modification DENIED: {reason} File: '{target_file.strip()}'"
                        }))
                        return

            # Check high-risk file paths -> FORCE_ASK (P0-14, P0-15).
            # Canonical state is deliberately handled by the lifecycle itself and
            # must remain machine-writable; other control-plane edits stay gated.
            if is_state_write:
                print(json.dumps({"decision": "allow"}))
                return
            for pattern, reason in HIGH_RISK_PATH_PATTERNS:
                for p_str in paths_to_test:
                    if re.search(pattern, p_str, re.IGNORECASE):
                        print(json.dumps({
                            "decision": "force_ask",
                            "reason": f"[HIGH-RISK PATH] {reason} File: '{target_file.strip()}'"
                        }))
                        return

            # All remaining governed application writes require a lifecycle task
            # that has passed classification/planning and entered execution.
            if ws_info.is_governed and requires_execution_task(task_status):
                print(json.dumps({
                    "decision": "deny",
                    "reason": f"[GOVERNANCE GUARD] Application mutation blocked: register/classify/plan the task and move it into an execution state before editing repository files (task={active_task_id or 'none'}, status={task_status or 'none'})."
                }))
                return

    # Default: ALLOW
    print(json.dumps({"decision": "allow"}))


if __name__ == "__main__":
    main()
