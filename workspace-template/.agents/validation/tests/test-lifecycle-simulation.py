#!/usr/bin/env python3
"""Lifecycle and tool-safety regression tests for the framework itself."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HOOK = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "hook-pre-tool.py"


def hook(payload: dict) -> dict:
    proc = subprocess.run([sys.executable, str(HOOK)], cwd=ROOT, input=json.dumps(payload), text=True, capture_output=True)
    assert proc.returncode == 0
    return json.loads(proc.stdout)


def test_unknown_tool_fails_closed() -> None:
    result = hook({"toolCall": {"name": "unknown_future_tool", "args": {}}, "workspacePaths": [str(ROOT)]})
    assert result["decision"] == "force_ask"


def test_safe_known_tool_allowed() -> None:
    result = hook({"toolCall": {"name": "view_file", "args": {"AbsolutePath": str(ROOT / "AGENTS.md")}}, "workspacePaths": [str(ROOT)]})
    assert result["decision"] == "allow"


def test_secret_file_requires_confirmation() -> None:
    result = hook({"toolCall": {"name": "write_to_file", "args": {"TargetFile": str(ROOT / ".env")}}, "workspacePaths": [str(ROOT)]})
    assert result["decision"] == "force_ask"


def test_catastrophic_command_denied() -> None:
    result = hook({"toolCall": {"name": "run_command", "args": {"CommandLine": "rm -rf /"}}, "workspacePaths": [str(ROOT)]})
    assert result["decision"] == "deny"


def test_registered_tools_have_required_metadata() -> None:
    registry = json.loads((ROOT / ".agents" / "orchestration" / "antigravity-tool-registry.json").read_text())
    required = {"capability", "access", "risk", "supportedAgentTypes"}
    for name, entry in registry.get("tools", {}).items():
        assert required.issubset(entry), f"Tool {name!r} is missing required adapter metadata."


def test_verification_rejects_missing_evidence() -> None:
    sys.path.insert(0, str(ROOT / ".agents"))
    from validation.core.verification_policy import VerificationPolicyEngine

    engine = VerificationPolicyEngine()
    required = engine.get_required_gates("feature", "medium")
    assert {"lint", "typecheck", "test", "build"}.issubset(required)

    passed_without_evidence = [
        {"name": gate, "status": "passed"}
        for gate in required
    ]
    ok, _, error = engine.evaluate_gates("feature", "medium", passed_without_evidence)
    assert ok is False
    assert error and "evidence" in error.lower()


def test_verification_rejects_nonzero_passed_command() -> None:
    sys.path.insert(0, str(ROOT / ".agents"))
    from validation.core.verification_policy import VerificationPolicyEngine

    engine = VerificationPolicyEngine()
    recorded = [
        {
            "name": "lint",
            "status": "passed",
            "evidenceRef": {
                "type": "local-command",
                "command": "npm run lint",
                "exitCode": 1,
                "capturedAt": "2026-01-01T00:00:00Z",
            },
        }
    ]
    ok, _, error = engine.evaluate_gates("simple", "low", recorded)
    assert ok is False
    assert error and "non-zero" in error


def test_verification_taxonomy_matches_schema() -> None:
    sys.path.insert(0, str(ROOT / ".agents"))
    from validation.core.verification_policy import CANONICAL_TASK_TYPES
    schema = json.loads((ROOT / ".agents" / "orchestration" / "verification-schema.json").read_text())
    expected = set(schema["properties"]["taskType"]["enum"])
    assert CANONICAL_TASK_TYPES == expected


if __name__ == "__main__":
    test_unknown_tool_fails_closed()
    test_safe_known_tool_allowed()
    test_secret_file_requires_confirmation()
    test_catastrophic_command_denied()
    test_registered_tools_have_required_metadata()
    test_verification_rejects_missing_evidence()
    test_verification_rejects_nonzero_passed_command()
    test_verification_taxonomy_matches_schema()
    print("Lifecycle/self-safety tests PASSED")
