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


def test_hooks_are_not_duplicated() -> None:
    hooks = json.loads((ROOT / ".agents" / "hooks.json").read_text())
    assert len(hooks["pretool-guard"]["PreToolUse"]) == 1
    assert len(hooks["posttool-audit"]["PostToolUse"]) == 1
    assert len(hooks["session-bootstrap"]["PreInvocation"]) == 1


def test_rule_activation_uses_native_triggers() -> None:
    rules_dir = ROOT / ".agents" / "rules"
    supported = {"always_on", "model_decision", "glob", "manual"}
    for path in sorted(rules_dir.glob("*.md")):
        if path.name == "RULE_ACTIVATION.md":
            continue
        content = path.read_text()
        assert content.startswith("---\n"), path
        end = content.find("\n---\n", 4)
        assert end != -1, path
        frontmatter = content[:end + 5]
        trigger_line = next((line for line in frontmatter.splitlines() if line.startswith("trigger:")), "")
        trigger = trigger_line.split(":", 1)[1].strip()
        assert trigger in supported, path
        if trigger == "model_decision":
            assert "description:" in frontmatter, path
        if trigger == "glob":
            assert "globs:" in frontmatter, path


def test_policy_linter_works_from_workspace_root() -> None:
    script = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "lint-policy-consistency.py"
    proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "inspected" in proc.stdout.lower()


def test_bootstrap_injects_context_and_records_inquiry_session(tmp_path: Path) -> None:
    script = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "bootstrap-session.py"
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text(json.dumps({"role": "user", "content": "What is the architecture of this project?"}) + "\n")
    conversation_id = f"test-conversation-{tmp_path.name}"
    payload = {"conversationId": conversation_id, "workspacePaths": [str(ROOT)], "transcriptPath": str(transcript)}
    try:
        proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, input=json.dumps(payload), text=True, capture_output=True)
        assert proc.returncode == 0, proc.stderr
        result = json.loads(proc.stdout)
        assert "injectSteps" in result
        assert all("toolCall" in step or "ephemeralMessage" in step for step in result["injectSteps"])
        session = json.loads((ROOT / ".agents" / "state" / "runtime" / "session.json").read_text())
        assert session["mode"] == "inquiry"
        assert session["conversationId"] == conversation_id

        proc2 = subprocess.run([sys.executable, str(script)], cwd=ROOT, input=json.dumps(payload), text=True, capture_output=True)
        assert proc2.returncode == 0, proc2.stderr
        second = json.loads(proc2.stdout)
        assert len(second["injectSteps"]) == 1
        assert "already completed" in second["injectSteps"][0]["ephemeralMessage"]
    finally:
        for candidate in [
            ROOT / ".agents" / "state" / "runtime" / "session.json",
            ROOT / ".agents" / "state" / "runtime" / "context-plan.md",
            ROOT / ".agents" / "state" / "runtime" / "sessions" / f"{conversation_id}.json",
            ROOT / ".agents" / "state" / "runtime" / "context-plans" / f"{conversation_id}.md",
        ]:
            candidate.unlink(missing_ok=True)


def test_bootstrap_preloads_task_specific_rules_and_skills(tmp_path: Path) -> None:
    script = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "bootstrap-session.py"
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text(
        json.dumps({
            "role": "user",
            "content": "Fix the authentication bug in the Next.js frontend and add a regression test."
        }) + "\n"
    )
    conversation_id = f"test-governed-context-{tmp_path.name}"
    payload = {
        "conversationId": conversation_id,
        "workspacePaths": [str(ROOT)],
        "transcriptPath": str(transcript),
    }
    proc = subprocess.run(
        [sys.executable, str(script)],
        cwd=ROOT,
        input=json.dumps(payload),
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 0, proc.stderr
    result = json.loads(proc.stdout)
    paths = []
    for step in result["injectSteps"]:
        call = step.get("toolCall", {})
        args = call.get("args", {})
        if call.get("name") == "view_file":
            paths.append(args.get("AbsolutePath", ""))
    joined = "\n".join(paths)
    assert ".agents/rules/07-security.md" in joined
    assert ".agents/skills/bug-fix/SKILL.md" in joined
    assert ".agents/skills/frontend/SKILL.md" in joined
    assert ".agents/skills/verification/SKILL.md" in joined
    assert ".agents/state/stack.json" in joined
    assert ".agents/orchestration/stack.json" not in joined

    task_files = list((ROOT / ".agents" / "state" / "tasks").glob("TASK-*.json"))
    assert task_files
    newest = max(task_files, key=lambda p: p.stat().st_mtime)
    task = json.loads(newest.read_text())
    assert task["bootstrapProvisional"] is True
    governance_file = ROOT / ".agents" / "state" / "governance" / f"{task['id']}.json"
    assert governance_file.is_file()
    governance = json.loads(governance_file.read_text())
    assert governance["taskId"] == task["id"]
    assert governance["governanceStatus"] == "pending"

    # Keep framework tests hermetic: runtime/task state must never leak between pytest runs.
    for candidate in [
        task_files[0],
        governance_file,
        ROOT / ".agents" / "state" / "runtime" / "session.json",
        ROOT / ".agents" / "state" / "runtime" / "context-plan.md",
        ROOT / ".agents" / "state" / "runtime" / "sessions" / f"{conversation_id}.json",
        ROOT / ".agents" / "state" / "runtime" / "context-plans" / f"{conversation_id}.md",
    ]:
        candidate.unlink(missing_ok=True)


def test_runtime_contract_validator_passes() -> None:
    script = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "validate-runtime-contract.py"
    proc = subprocess.run([sys.executable, str(script)], cwd=ROOT, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "RUNTIME CONTRACT: PASS" in proc.stdout


def test_planning_and_memory_skills_do_not_require_in_progress() -> None:
    for name in ("planning", "project-memory", "requirements-discovery"):
        text = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text()
        pre = text.split("<PRECONDITIONS>", 1)[1].split("</PRECONDITIONS>", 1)[0]
        assert "must be `IN_PROGRESS`" not in pre
