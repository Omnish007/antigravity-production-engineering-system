#!/usr/bin/env python3
"""Self-tests for the shipped agent governance validators."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SCRIPTS = ROOT / ".agents" / "skills" / "quality-gates" / "scripts"


def run(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPTS / name), *args], cwd=ROOT, text=True, capture_output=True)


def test_static_validators() -> None:
    commands = [
        ("validate-agents.py",),
        ("validate-instruction-tags.py", str(ROOT)),
        ("validate-technology-profiles.py", "--profiles-dir", str(ROOT / ".agents" / "technology" / "profiles")),
        ("validate-policy-registry.py", "--registry-file", str(ROOT / ".agents" / "orchestration" / "policy-registry.yaml")),
        ("validate-control-plane.py", "--project-root", str(ROOT)),
        ("lint-state-instructions.py", "--check"),
        ("reconcile-state.py", "--check", "--state-dir", str(ROOT / ".agents" / "state")),
        ("generate-manifest.py", "--check", "--root", str(ROOT.parent)),
    ]
    for cmd in commands:
        proc = run(*cmd)
        assert proc.returncode == 0, (
            f"{cmd} failed:\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
        )


def test_state_taxonomy_is_canonical() -> None:
    schema = json.loads((ROOT / ".agents" / "state" / "tasks.schema.json").read_text())
    expected = ["simple", "bug", "feature", "complex-feature", "refactor", "architecture", "security", "database", "migration", "performance", "testing", "deployment", "documentation", "requirements", "investigation", "infrastructure"]
    actual = schema["properties"]["tasks"]["items"]["properties"]["type"]["enum"]
    assert actual == expected, (actual, expected)


if __name__ == "__main__":
    test_static_validators()
    test_state_taxonomy_is_canonical()
    print("Validator self-tests PASSED")


def test_architecture_checker_has_workspace_root() -> None:
    script = ROOT / ".agents" / "validation" / "check-architecture.py"
    proc = subprocess.run([sys.executable, str(script), "--json"], cwd=ROOT.parent, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["root"] == str(ROOT)
    assert payload["errors"] == 0


def test_agent_validator_autodetects_workspace_from_package_root() -> None:
    script = ROOT / ".agents" / "skills" / "quality-gates" / "scripts" / "validate-agents.py"
    proc = subprocess.run([sys.executable, str(script)], cwd=ROOT.parent, text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Checked 9 agent definition(s)" in proc.stdout
