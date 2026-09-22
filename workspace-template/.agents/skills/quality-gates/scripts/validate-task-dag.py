#!/usr/bin/env python3
"""
validate-task-dag.py

Validates the semantic integrity of the task Directed Acyclic Graph (DAG) in tasks.json:
1. Valid JSON syntax and basic schema conformance.
2. Unique task IDs across the entire task set.
3. Valid task ID format (TASK-NNN).
4. Valid statuses (PENDING, READY, IN_PROGRESS, VERIFYING, COMPLETED, FAILED, BLOCKED, CANCELLED).
5. Dependency resolution: all dependencies reference existing task IDs.
6. Cycle detection: no circular dependency loops exist in the DAG.
7. Phase consistency: all taskIds in phases reference valid tasks.
8. Status progression logic: tasks cannot be READY/IN_PROGRESS if dependencies are incomplete.
"""

import json
import os
import re
import sys
from typing import Dict, List, Set, Any

VALID_STATUSES = {
    "DRAFT",
    "CLASSIFIED",
    "CONTEXT_READY",
    "PLANNED",
    "PENDING",
    "READY",
    "IN_PROGRESS",
    "TESTING",
    "VERIFYING",
    "REVIEWING",
    "MEMORY_SYNC",
    "STATE_SYNC",
    "GOVERNANCE_CHECK",
    "COMPLETED",
    "FAILED",
    "BLOCKED",
    "CANCELLED",
}

VALID_TYPES = {
    "simple",
    "bug",
    "bugfix",
    "feature",
    "complex-feature",
    "refactor",
    "architecture",
    "security",
    "database",
    "migration",
    "performance",
    "testing",
    "test",
    "deployment",
    "documentation",
    "docs",
    "requirements",
    "investigation",
    "unknown/mixed",
    "infrastructure",
}

VALID_RISKS = {"low", "medium", "high", "critical"}
VALID_PRIORITIES = {"P0", "P1", "P2", "P3"}
TASK_ID_PATTERN = re.compile(r"^TASK-[0-9]{3,}$")


def validate_dag(data: Dict[str, Any], filepath: str) -> List[str]:
    errors: List[str] = []

    if not isinstance(data, dict):
        return [f"Root of {filepath} must be a JSON object."]

    tasks = data.get("tasks", [])
    phases = data.get("phases", [])

    if not isinstance(tasks, list):
        errors.append(f"'tasks' field must be an array in {filepath}")
        return errors

    if not isinstance(phases, list):
        errors.append(f"'phases' field must be an array in {filepath}")

    # If tasks array is empty (template state), DAG is valid trivially
    if len(tasks) == 0:
        return errors

    task_map: Dict[str, Dict[str, Any]] = {}
    duplicate_ids: Set[str] = set()

    for idx, task in enumerate(tasks):
        if not isinstance(task, dict):
            errors.append(f"Task at index {idx} must be an object.")
            continue

        task_id = task.get("id")
        if not task_id or not isinstance(task_id, str):
            errors.append(f"Task at index {idx} missing valid 'id' string.")
            continue

        if not TASK_ID_PATTERN.match(task_id):
            errors.append(
                f"Task '{task_id}' has invalid ID format (must match ^TASK-[0-9]{{3,}}$)."
            )

        if task_id in task_map:
            duplicate_ids.add(task_id)
        else:
            task_map[task_id] = task

        # Check status
        status = task.get("status")
        if status not in VALID_STATUSES:
            errors.append(f"Task '{task_id}' has invalid status: '{status}'.")

        # Check type
        task_type = task.get("type")
        if task_type and task_type not in VALID_TYPES:
            errors.append(f"Task '{task_id}' has invalid type: '{task_type}'.")

        # Check dependencies is list
        deps = task.get("dependencies", [])
        if not isinstance(deps, list):
            errors.append(f"Task '{task_id}' dependencies must be a list of IDs.")

        # Check acceptance criteria
        ac = task.get("acceptanceCriteria", [])
        if not isinstance(ac, list) or len(ac) == 0:
            errors.append(
                f"Task '{task_id}' must have at least one acceptance criterion in 'acceptanceCriteria'."
            )

    if duplicate_ids:
        for dup in sorted(duplicate_ids):
            errors.append(f"Duplicate task ID found: '{dup}'.")

    # Dependency existence check
    for task_id, task in task_map.items():
        deps = task.get("dependencies", [])
        if isinstance(deps, list):
            for dep in deps:
                if dep not in task_map:
                    errors.append(
                        f"Task '{task_id}' depends on non-existent task '{dep}'."
                    )
                elif dep == task_id:
                    errors.append(f"Task '{task_id}' cannot depend on itself.")

    # Cycle detection via DFS
    visited: Dict[str, int] = {}  # 0 = unvisited, 1 = visiting, 2 = visited

    def detect_cycle(node: str, path: List[str]) -> bool:
        visited[node] = 1
        path.append(node)
        task = task_map.get(node)
        if task:
            deps = task.get("dependencies", [])
            for dep in deps:
                if dep in task_map:
                    if visited.get(dep, 0) == 1:
                        cycle_path = " -> ".join(path[path.index(dep) :] + [dep])
                        errors.append(f"Dependency cycle detected: {cycle_path}")
                        return True
                    elif visited.get(dep, 0) == 0:
                        if detect_cycle(dep, path):
                            return True
        path.pop()
        visited[node] = 2
        return False

    for task_id in task_map:
        if visited.get(task_id, 0) == 0:
            detect_cycle(task_id, [])

    # Status progression consistency check
    for task_id, task in task_map.items():
        status = task.get("status")
        deps = task.get("dependencies", [])
        if status in {"READY", "IN_PROGRESS", "VERIFYING", "COMPLETED"}:
            for dep in deps:
                dep_task = task_map.get(dep)
                if dep_task:
                    dep_status = dep_task.get("status")
                    if status in {"READY", "IN_PROGRESS"} and dep_status != "COMPLETED":
                        errors.append(
                            f"Task '{task_id}' is '{status}' but dependency '{dep}' is '{dep_status}' (must be COMPLETED)."
                        )
                    elif status == "COMPLETED" and dep_status not in {"COMPLETED"}:
                        errors.append(
                            f"Task '{task_id}' is COMPLETED but dependency '{dep}' is '{dep_status}'."
                        )

    # Cross-reference governance.json if available
    gov_file = os.path.join(os.path.dirname(filepath), "governance.json")
    if os.path.isfile(gov_file):
        try:
            with open(gov_file, "r", encoding="utf-8") as gf:
                gov_data = json.load(gf)
                gov_records = {
                    r.get("taskId"): r
                    for r in gov_data.get("records", [])
                    if isinstance(r, dict) and "taskId" in r
                }
                for task_id, task in task_map.items():
                    if task.get("status") == "COMPLETED":
                        rec = gov_records.get(task_id)
                        if not rec:
                            errors.append(
                                f"Task '{task_id}' is COMPLETED in tasks.json but has no record in governance.json."
                            )
                        elif rec.get("governanceStatus") != "complete":
                            errors.append(
                                f"Task '{task_id}' is COMPLETED in tasks.json but governanceStatus is '{rec.get('governanceStatus')}' in governance.json."
                            )
        except Exception:
            pass

    # Phase validation
    for idx, phase in enumerate(phases):
        if not isinstance(phase, dict):
            errors.append(f"Phase at index {idx} must be an object.")
            continue
        phase_id = phase.get("id", f"phase-{idx}")
        phase_task_ids = phase.get("taskIds", [])
        if isinstance(phase_task_ids, list):
            for pid in phase_task_ids:
                if pid not in task_map:
                    errors.append(
                        f"Phase '{phase_id}' references non-existent task '{pid}'."
                    )

    return errors


def main():
    if len(sys.argv) < 2:
        target = os.path.join(os.getcwd(), ".agents", "state", "tasks.json")
        if not os.path.exists(target):
            target = os.path.join(
                os.getcwd(), "workspace-template", ".agents", "state", "tasks.json"
            )
    else:
        target = sys.argv[1]

    if not os.path.exists(target):
        print(f"Error: File not found: {target}")
        sys.exit(1)

    try:
        with open(target, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON Parse Error in {target}: {e}")
        sys.exit(1)

    # Merge per-task tasks if tasks directory exists (per-task is canonical source of truth)
    tasks_dir = os.path.join(os.path.dirname(target), "tasks")
    if os.path.isdir(tasks_dir):
        per_task_tasks = {}
        for fname in sorted(os.listdir(tasks_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(tasks_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        t = json.load(f)
                        if isinstance(t, dict) and t.get("id"):
                            per_task_tasks[t["id"]] = t
                except Exception as e:
                    print(f"JSON Parse Error in per-task file {fpath}: {e}")
                    sys.exit(1)
        # Per-task tasks override aggregate tasks
        tasks_map = {t.get("id"): t for t in data.get("tasks", []) if isinstance(t, dict) and t.get("id")}
        tasks_map.update(per_task_tasks)
        data["tasks"] = list(tasks_map.values())

    errors = validate_dag(data, target)

    if errors:
        print(f"Task DAG Validation FAILED for {target} ({len(errors)} errors):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        task_count = len(data.get("tasks", []))
        print(f"Task DAG Validation PASSED for {target} ({task_count} tasks verified).")
        sys.exit(0)


if __name__ == "__main__":
    main()
