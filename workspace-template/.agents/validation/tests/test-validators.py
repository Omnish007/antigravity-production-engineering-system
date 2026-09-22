#!/usr/bin/env python3
"""
test-validators.py

Automated test suite verifying the governance validator and task DAG validator
against known-good (valid) and known-bad (invalid) fixtures.

Target Invariants:
1. All valid fixtures in fixtures/valid/*.json must PASS validation cleanly (0 errors).
2. All invalid fixtures in fixtures/invalid/*.json must FAIL validation and report
   the specific expected error substrings.
"""

import json
import os
import shutil
import sys
import tempfile
from typing import Any, Dict, List, Tuple

# Add scripts directory to sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", "..", ".."))
SCRIPTS_DIR = os.path.join(REPO_ROOT, "workspace-template", ".agents", "skills", "quality-gates", "scripts")
sys.path.insert(0, SCRIPTS_DIR)

try:
    import importlib.util
    # Load validate-governance.py
    gov_spec = importlib.util.spec_from_file_location("validate_governance", os.path.join(SCRIPTS_DIR, "validate-governance.py"))
    gov_mod = importlib.util.module_from_spec(gov_spec)
    gov_spec.loader.exec_module(gov_mod)

    # Load validate-task-dag.py
    dag_spec = importlib.util.spec_from_file_location("validate_task_dag", os.path.join(SCRIPTS_DIR, "validate-task-dag.py"))
    dag_mod = importlib.util.module_from_spec(dag_spec)
    dag_spec.loader.exec_module(dag_mod)
except Exception as e:
    print(f"FATAL: Failed to import validator modules from {SCRIPTS_DIR}: {e}", file=sys.stderr)
    sys.exit(1)


def setup_temp_workspace(fixture: Dict[str, Any]) -> str:
    """Create a temporary workspace populated with fixture state and symlinks to real rules/skills/docs."""
    temp_dir = tempfile.mkdtemp(prefix="agy_val_test_")
    agents_dir = os.path.join(temp_dir, ".agents")
    state_dir = os.path.join(agents_dir, "state")
    os.makedirs(state_dir, exist_ok=True)

    # Symlink rules, skills, technology, orchestration from workspace-template
    src_agents = os.path.join(REPO_ROOT, "workspace-template", ".agents")
    for d in ["rules", "skills", "technology", "orchestration", "templates"]:
        src = os.path.join(src_agents, d)
        if os.path.exists(src):
            os.symlink(src, os.path.join(agents_dir, d))

    # Symlink docs
    src_docs = os.path.join(REPO_ROOT, "workspace-template", "docs")
    if os.path.exists(src_docs):
        os.symlink(src_docs, os.path.join(temp_dir, "docs"))

    # Copy schema files to state directory
    src_state = os.path.join(src_agents, "state")
    if os.path.isdir(src_state):
        for f in os.listdir(src_state):
            if f.endswith(".schema.json"):
                shutil.copy2(os.path.join(src_state, f), os.path.join(state_dir, f))

    # Write fixture state files
    gov_path = os.path.join(state_dir, "governance.json")
    with open(gov_path, "w", encoding="utf-8") as f:
        json.dump(fixture.get("governance", {"schemaVersion": "1.0.0", "records": []}), f, indent=2)

    tasks_path = os.path.join(state_dir, "tasks.json")
    with open(tasks_path, "w", encoding="utf-8") as f:
        json.dump(fixture.get("tasks", {"schemaVersion": "1.0.0", "tasks": []}), f, indent=2)

    events_path = os.path.join(state_dir, "events.jsonl")
    with open(events_path, "w", encoding="utf-8") as f:
        for ev in fixture.get("events", []):
            f.write(json.dumps(ev) + "\n")

    blockers_path = os.path.join(state_dir, "blockers.json")
    with open(blockers_path, "w", encoding="utf-8") as f:
        json.dump(fixture.get("blockers", {"schemaVersion": "1.0.0", "active": [], "resolved": []}), f, indent=2)

    return temp_dir


def test_valid_fixtures() -> Tuple[int, int]:
    valid_dir = os.path.join(REPO_ROOT, "workspace-template", ".agents", "validation", "fixtures", "valid")
    if not os.path.isdir(valid_dir):
        print(f"Error: valid fixtures directory not found: {valid_dir}")
        return 0, 1

    fixtures = sorted([f for f in os.listdir(valid_dir) if f.endswith(".json")])
    passed = 0
    failed = 0

    print(f"\n--- Running Positive Fixture Tests ({len(fixtures)} fixtures) ---")
    for fname in fixtures:
        fpath = os.path.join(valid_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            fixture = json.load(f)

        temp_ws = setup_temp_workspace(fixture)
        try:
            gov_path = os.path.join(temp_ws, ".agents", "state", "governance.json")
            gov_data = fixture.get("governance", {})
            tasks_data = fixture.get("tasks", {})

            # 1. Test Governance Validator
            errors, metrics = gov_mod.validate_governance_layers(gov_data, tasks_data, gov_path)
            # 2. Test Task DAG Validator
            dag_errors = dag_mod.validate_dag(tasks_data, os.path.join(temp_ws, ".agents", "state", "tasks.json"))

            all_errors = errors + dag_errors
            if all_errors:
                print(f"  [FAIL] {fname}: Expected PASS, got {len(all_errors)} errors:")
                for err in all_errors:
                    print(f"         - {err}")
                failed += 1
            else:
                print(f"  [PASS] {fname} ({metrics['records_count']} records, {metrics['gates_evaluated']} gates)")
                passed += 1
        finally:
            shutil.rmtree(temp_ws, ignore_errors=True)

    return passed, failed


def test_invalid_fixtures() -> Tuple[int, int]:
    invalid_dir = os.path.join(REPO_ROOT, "workspace-template", ".agents", "validation", "fixtures", "invalid")
    if not os.path.isdir(invalid_dir):
        print(f"Error: invalid fixtures directory not found: {invalid_dir}")
        return 0, 1

    fixtures = sorted([f for f in os.listdir(invalid_dir) if f.endswith(".json")])
    passed = 0
    failed = 0

    print(f"\n--- Running Negative Fixture Tests ({len(fixtures)} fixtures) ---")
    for fname in fixtures:
        fpath = os.path.join(invalid_dir, fname)
        with open(fpath, "r", encoding="utf-8") as f:
            fixture = json.load(f)

        expected_errors = fixture.get("expectedErrors", [])
        temp_ws = setup_temp_workspace(fixture)
        try:
            gov_path = os.path.join(temp_ws, ".agents", "state", "governance.json")
            gov_data = fixture.get("governance", {})
            tasks_data = fixture.get("tasks", {})

            errors, _ = gov_mod.validate_governance_layers(gov_data, tasks_data, gov_path)
            dag_errors = dag_mod.validate_dag(tasks_data, os.path.join(temp_ws, ".agents", "state", "tasks.json"))

            all_errors = errors + dag_errors
            if not all_errors:
                print(f"  [FAIL] {fname}: Expected errors, but validation PASSED!")
                failed += 1
                continue

            # Check that expected error substrings are present
            missing_expected = []
            for exp in expected_errors:
                if not any(exp.lower() in err.lower() for err in all_errors):
                    missing_expected.append(exp)

            if missing_expected:
                print(f"  [FAIL] {fname}: Missing expected error substring(s): {missing_expected}")
                print(f"         Actual errors:")
                for err in all_errors:
                    print(f"         - {err}")
                failed += 1
            else:
                print(f"  [PASS] {fname} (Correctly rejected with {len(all_errors)} error(s))")
                passed += 1
        finally:
            shutil.rmtree(temp_ws, ignore_errors=True)

    return passed, failed


def main():
    print("======================================================================")
    print("      ANTIGRAVITY GOVERNANCE & TASK DAG VALIDATOR TEST SUITE          ")
    print("======================================================================")

    v_passed, v_failed = test_valid_fixtures()
    iv_passed, iv_failed = test_invalid_fixtures()

    total_passed = v_passed + iv_passed
    total_failed = v_failed + iv_failed
    total_tests = total_passed + total_failed

    print("\n----------------------------------------------------------------------")
    print(f"TEST SUMMARY: {total_tests} executed | {total_passed} PASSED | {total_failed} FAILED")
    print("----------------------------------------------------------------------")

    if total_failed > 0:
        sys.exit(1)
    else:
        print("All validator test suite fixtures PASSED cleanly.\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
