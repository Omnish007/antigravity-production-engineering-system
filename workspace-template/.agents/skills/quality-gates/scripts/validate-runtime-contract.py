#!/usr/bin/env python3
"""Validate the executable runtime contract of the Antigravity engineering system.

This validator checks the failure modes that are easy to miss when prose, rules,
skills, hooks, and CI evolve independently:
- native Antigravity hook/rule contracts;
- bootstrap paths and automatic context preload;
- lifecycle/precondition consistency in skills;
- control-plane discoverability;
- stale CI test references.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import List


ROOT = Path(__file__).resolve().parents[4]


def fail(errors: List[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: List[str] = []

    hooks_path = ROOT / ".agents" / "hooks.json"
    bootstrap_path = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "bootstrap-session.py"
    if not hooks_path.is_file():
        fail(errors, "Missing .agents/hooks.json")
    if not bootstrap_path.is_file():
        fail(errors, "Missing bootstrap-session.py")
    else:
        bootstrap = bootstrap_path.read_text(encoding="utf-8")
        required_bootstrap_paths = [
            '".agents/state/stack.json"',
            '".agents/orchestration/policy-registry.yaml"',
            '".agents/orchestration/task-lifecycle.md"',
            '".agents/orchestration/task-classifier.md"',
            '".agents/orchestration/context-router.md"',
            '"docs/INDEX.md"',
        ]
        for token in required_bootstrap_paths:
            if token not in bootstrap:
                fail(errors, f"Bootstrap is missing mandatory context reference: {token}")
        if ".agents/orchestration/stack.json" in bootstrap:
            fail(errors, "Bootstrap contains stale stack path .agents/orchestration/stack.json")
        if 'resolve_preinvocation_injection_mode' not in bootstrap:
            fail(errors, "Bootstrap is missing fail-closed PreInvocation capability gating")
        if 'PREINVOCATION_MODE_ENV' not in bootstrap:
            fail(errors, "Bootstrap is missing explicit PreInvocation mode controls")
        if 'supportedInjectedStepTypes' not in bootstrap or 'capabilities' not in bootstrap:
            fail(errors, "Bootstrap is missing host capability-signal handling")
        if '"ephemeralMessage"' not in bootstrap:
            fail(errors, "Bootstrap does not provide a host-compatible deferred-read message")
        if "candidate_rules(prompt)" not in bootstrap or "candidate_skills(prompt)" not in bootstrap:
            fail(errors, "Bootstrap does not route task-specific rule/skill candidates")
        if 'unknown-fails-closed' not in bootstrap:
            fail(errors, "Bootstrap does not fail closed when PreInvocation injection capability is unknown")
        for required_skill in (
            '".agents/skills/planning/SKILL.md"',
            '".agents/skills/verification/SKILL.md"',
            '".agents/skills/testing/SKILL.md"',
        ):
            if required_skill not in bootstrap:
                fail(errors, f"Bootstrap is missing baseline lifecycle skill: {required_skill}")

    if hooks_path.is_file():
        try:
            hooks = json.loads(hooks_path.read_text(encoding="utf-8"))
            expected = {
                "session-bootstrap": "PreInvocation",
                "pretool-guard": "PreToolUse",
                "posttool-audit": "PostToolUse",
                "stop-governance-guard": "Stop",
            }
            for name, event in expected.items():
                handlers = hooks.get(name, {}).get(event, [])
                if len(handlers) != 1:
                    fail(errors, f"Hook {name}/{event} must have exactly one handler; found {len(handlers)}")
        except Exception as exc:
            fail(errors, f"Cannot parse hooks.json: {exc}")

    rules_dir = ROOT / ".agents" / "rules"
    supported_triggers = {"always_on", "model_decision", "glob", "manual"}
    for rule in sorted(rules_dir.glob("*.md")):
        if rule.name == "RULE_ACTIVATION.md":
            continue
        text = rule.read_text(encoding="utf-8")
        if len(text) > 12000:
            fail(errors, f"Rule exceeds Antigravity 12,000-character limit: {rule.name}")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            fail(errors, f"Rule missing YAML frontmatter: {rule.name}")
            continue
        fm = text[4:text.find("\n---\n", 4)]
        trigger_match = re.search(r"^trigger:\s*([^\n]+)$", fm, re.M)
        if not trigger_match or trigger_match.group(1).strip() not in supported_triggers:
            fail(errors, f"Rule has invalid trigger: {rule.name}")
        if "ID: RULE-" not in text[:1400]:
            fail(errors, f"Rule missing control-plane ID tag: {rule.name}")

    skills_dir = ROOT / ".agents" / "skills"
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---\n") or "\n---\n" not in text[4:]:
            fail(errors, f"Skill missing YAML frontmatter: {skill_md.parent.name}")
            continue
        fm = text[4:text.find("\n---\n", 4)]
        if not re.search(r"^name:\s*\S+", fm, re.M):
            fail(errors, f"Skill missing name: {skill_md.parent.name}")
        if not re.search(r"^description:\s*.+", fm, re.M):
            fail(errors, f"Skill missing description: {skill_md.parent.name}")
        pre = re.search(r"<PRECONDITIONS>(.*?)</PRECONDITIONS>", text, re.S)
        if pre and re.search(r"must be `IN_PROGRESS`", pre.group(1), re.I):
            fail(errors, f"Skill lifecycle precondition is overly restrictive: {skill_md.parent.name}")

    workflow = ROOT / ".github" / "workflows" / "ai-validation.yml"
    if workflow.is_file():
        ci = workflow.read_text(encoding="utf-8")
        stale = ["test-validators.py", "test-lifecycle-simulation.py"]
        for ref in stale:
            if ref in ci:
                fail(errors, f"CI references stale test filename: {ref}")
        if "python3 -m pytest" not in ci:
            fail(errors, "CI framework-integrity job must execute the pytest suite directly")
        if "validate-runtime-contract.py" not in ci:
            fail(errors, "CI must execute validate-runtime-contract.py")

    task_lifecycle = ROOT / ".agents" / "orchestration" / "task-lifecycle.md"
    planning = ROOT / ".agents" / "skills" / "planning" / "SKILL.md"
    memory = ROOT / ".agents" / "skills" / "project-memory" / "SKILL.md"
    session_schema = ROOT / ".agents" / "state" / "runtime" / "session.schema.json"
    if not session_schema.is_file():
        fail(errors, "Missing runtime session schema")

    # Preserve the strongest legacy execution heuristics as regression invariants.
    legacy_required = {
        ROOT / ".agents" / "orchestration" / "decision-policy.md": ("Research First", "Ask the user"),
        ROOT / ".agents" / "orchestration" / "error-recovery-policy.md": ("doom loop", "root cause"),
        ROOT / ".agents" / "orchestration" / "context-budget-policy.md": ("finite, high-value resource", "Bulk-loading"),
        ROOT / ".agents" / "orchestration" / "parallel-work-policy.md": ("semantic conflicts", "preserve successful work"),
        ROOT / ".agents" / "rules" / "14-observability.md": ("exit codes", "lifecycle events"),
    }
    for path, markers in legacy_required.items():
        if not path.is_file():
            fail(errors, f"Missing legacy-hardening policy: {path.relative_to(ROOT)}")
            continue
        content = path.read_text(encoding="utf-8").lower()
        for marker in markers:
            if marker.lower() not in content:
                fail(errors, f"Legacy-hardening invariant missing '{marker}' from {path.relative_to(ROOT)}")
    if task_lifecycle.is_file() and planning.is_file() and memory.is_file():
        lifecycle = task_lifecycle.read_text(encoding="utf-8")
        if "PLANNED" not in lifecycle or "IN_PROGRESS" not in lifecycle:
            fail(errors, "Canonical task lifecycle is incomplete")
        for p in (planning, memory):
            text = p.read_text(encoding="utf-8")
            pre = re.search(r"<PRECONDITIONS>(.*?)</PRECONDITIONS>", text, re.S)
            if pre and "IN_PROGRESS" in pre.group(1) and "must be" in pre.group(1):
                fail(errors, f"Planning/memory skill still hard-codes IN_PROGRESS: {p.name}")

    if errors:
        print("RUNTIME CONTRACT: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("RUNTIME CONTRACT: PASS")
    print(f"Checked rules={len(list(rules_dir.glob('*.md')))}, skills={len(list(skills_dir.glob('*/SKILL.md')))}, hooks=4, bootstrap=1, CI=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
