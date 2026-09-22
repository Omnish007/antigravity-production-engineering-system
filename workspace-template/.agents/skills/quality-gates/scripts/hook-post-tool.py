#!/usr/bin/env python3
"""hook-post-tool.py

Antigravity PostToolUse Lifecycle Hook:
- Captures tool execution metadata across commands and file mutation tools.
- P0-07: Writes to canonical per-task event stream (.agents/state/events/TASK-xxx.jsonl)
  when task ID is known, or runtime telemetry (.agents/state/events/telemetry.jsonl).
  Does NOT append directly to the derived aggregate events.jsonl.
- P0-20: Redacts sensitive credentials, tokens, and secrets from commands, errors, stderr, and paths.
- P0-21: Preserves TOOL_EXECUTION strictly as runtime telemetry.
- Returns empty JSON object {} as required by Antigravity PostToolUse contract.
"""

from datetime import datetime, timezone
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

REDACTION_PATTERNS = [
    (re.compile(r"Bearer\s+[A-Za-z0-9_\-\.]{8,}", re.IGNORECASE), "Bearer [REDACTED]"),
    (re.compile(r"(?i)(api[_-]?key|apikey|token|password|passwd|secret|private[_-]?key)\s*(=|:|\s+)\s*([^\s&'\"]+)", re.IGNORECASE), r"\1\2[REDACTED]"),
    (re.compile(r"://([^:\s]+):([^@\s]+)@"), r"://\1:[REDACTED]@"),
    (re.compile(r"-----BEGIN (?:[A-Z0-9_-]+ )?PRIVATE KEY-----[\s\S]+?-----END (?:[A-Z0-9_-]+ )?PRIVATE KEY-----"), "[REDACTED_PRIVATE_KEY]"),
]


def redact_string(val: str) -> Tuple[str, bool]:
    """Redact sensitive patterns from arbitrary string (P0-20)."""
    redacted = val
    was_redacted = False
    for pattern, replacement in REDACTION_PATTERNS:
        new_redacted = pattern.sub(replacement, redacted)
        if new_redacted != redacted:
            was_redacted = True
            redacted = new_redacted
    return redacted, was_redacted


def get_current_iso_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _get_next_sequence(event_file: Path) -> int:
    """Determine the next sequence number in an event file."""
    if not event_file.is_file():
        return 1
    count = 0
    try:
        with open(event_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    count += 1
    except Exception:
        pass
    return count + 1


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            print(json.dumps({}))
            return

        payload = json.loads(raw_input)
    except Exception:
        # Return {} even on parse failure to not break post-tool completion (fail open for telemetry)
        print(json.dumps({}))
        return

    # Extract execution details
    step_idx = payload.get("stepIdx")
    tool_call = payload.get("toolCall", {})
    tool_name = tool_call.get("name") if isinstance(tool_call, dict) else payload.get("toolName")
    tool_args = tool_call.get("args") if isinstance(tool_call, dict) else {}
    error = payload.get("error")
    workspace_paths = payload.get("workspacePaths", [])

    ws_info = resolve_workspace(payload={"workspacePaths": workspace_paths})
    if not ws_info.is_governed and not ws_info.state_root.is_dir():
        # Non-governed workspace without state dir: no-op
        print(json.dumps({}))
        return

    task_id = payload.get("taskId") or (tool_args.get("taskId") if isinstance(tool_args, dict) else None)
    if not task_id and isinstance(tool_args, dict):
        # Look for TASK-xxx in target path or command
        cmd_str = str(tool_args.get("CommandLine") or "")
        m = re.search(r"TASK-[0-9]{3,}", cmd_str)
        if m:
            task_id = m.group(0)

    events_dir = ws_info.state_root / "events"
    events_dir.mkdir(parents=True, exist_ok=True)

    # P0-07: Write to canonical per-task event stream if taskId known, else telemetry stream
    if task_id:
        target_event_file = events_dir / f"{task_id}.jsonl"
    else:
        target_event_file = events_dir / "telemetry.jsonl"

    seq = _get_next_sequence(target_event_file)
    event_id = f"EVT-{seq:06d}"

    was_redacted_any = False

    # Redact error (P0-20)
    clean_error = None
    if error:
        clean_error, r_err = redact_string(str(error))
        if r_err:
            was_redacted_any = True

    event_entry: Dict[str, Any] = {
        "eventId": event_id,
        "sequence": seq,
        "timestamp": get_current_iso_timestamp(),
        "source": "antigravity-hook",
        "stepIdx": step_idx if isinstance(step_idx, int) else None,
        "tool": tool_name if isinstance(tool_name, str) else None,
        "event": "TOOL_EXECUTION",
        "hasError": bool(error),
        "commandRedacted": False,
    }

    if task_id:
        event_entry["taskId"] = str(task_id)

    if clean_error:
        event_entry["error"] = clean_error

    if isinstance(tool_args, dict):
        # 1. Command execution auditing & redaction (P0-20)
        cmd = tool_args.get("CommandLine") or tool_args.get("command") or tool_args.get("cmd")
        if cmd:
            clean_cmd, was_redacted = redact_string(str(cmd))
            event_entry["command"] = clean_cmd
            if was_redacted:
                was_redacted_any = True

        # 2. Mutation tools auditing (write_to_file, replace_file_content, etc.)
        target_file = (
            tool_args.get("TargetFile")
            or tool_args.get("target_file")
            or tool_args.get("path")
            or tool_args.get("filePath")
        )
        if target_file:
            clean_path, was_path_redacted = redact_string(str(target_file))
            if was_path_redacted:
                was_redacted_any = True
            event_entry["filesMutated"] = [clean_path]

    event_entry["commandRedacted"] = was_redacted_any

    # Append to target canonical or telemetry event stream
    try:
        with open(target_event_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(event_entry) + "\n")
            f.flush()
    except Exception:
        pass

    # PostToolUse contract expects an empty JSON object
    print(json.dumps({}))


if __name__ == "__main__":
    main()
