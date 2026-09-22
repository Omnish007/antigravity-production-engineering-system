#!/usr/bin/env python3
"""
lint-state-instructions.py

Lints agent instructions, rules, skills, and orchestration policies to ensure they
direct agents to write to canonical per-task state (.agents/state/tasks/TASK-xxx.json, etc.)
rather than directly mutating derived aggregate files (tasks.json, governance.json, etc.).

Usage:
  python3 lint-state-instructions.py [--path TARGET_DIR] [--check] [--fix]
"""

import argparse
import os
import re
import sys
from typing import List, Tuple

# Patterns that indicate instructions directing writes to monolithic aggregates
VIOLATION_PATTERNS = [
    (
        re.compile(r"(?:update|write to|record in)\s+`?\.agents/state/tasks\.json`?", re.IGNORECASE),
        "Update canonical task state in `.agents/state/tasks/<task-id>.json` (or sync via `aggregate-state.py`)",
    ),
    (
        re.compile(r"(?:update|write to|record in)\s+`?\.agents/state/governance\.json`?", re.IGNORECASE),
        "Update canonical governance record in `.agents/state/governance/<task-id>.json`",
    ),
    (
        re.compile(r"(?:update|write to|record in)\s+`?\.agents/state/blockers\.json`?", re.IGNORECASE),
        "Record blocker in canonical file `.agents/state/blockers/<blocker-id>.json`",
    ),
    (
        re.compile(r"(?:update|write to|append to)\s+`?\.agents/state/events\.jsonl`?", re.IGNORECASE),
        "Append event to canonical per-task file `.agents/state/events/<task-id>.jsonl`",
    ),
    (
        re.compile(r"\bwrite to `?tasks\.json`?", re.IGNORECASE),
        "write to canonical task file `.agents/state/tasks/<task-id>.json`",
    ),
    (
        re.compile(r"\bwrite to `?governance\.json`?", re.IGNORECASE),
        "write to canonical governance file `.agents/state/governance/<task-id>.json`",
    ),
    (
        re.compile(r"\bappend(?:ed)? to `?events\.jsonl`?", re.IGNORECASE),
        "appended to canonical per-task event file `.agents/state/events/<task-id>.jsonl`",
    ),
]


def lint_file(file_path: str, fix: bool = False) -> Tuple[List[str], bool]:
    violations: List[str] = []
    modified = False

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read {file_path}: {e}"], False

    new_content = content
    lines = content.splitlines()

    for idx, line in enumerate(lines, 1):
        # Exclude scripts and schema files and test files from being flagged as instruction violations
        if file_path.endswith((".py", ".json", ".pyc")):
            continue

        for pattern, replacement in VIOLATION_PATTERNS:
            if pattern.search(line):
                violations.append(f"{file_path}:{idx}: Direct aggregate write instruction detected: '{line.strip()}'")
                if fix:
                    line_replaced = pattern.sub(replacement, line)
                    lines[idx - 1] = line_replaced
                    modified = True

    if fix and modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

    return violations, modified


def main():
    parser = argparse.ArgumentParser(description="Lint instructions for canonical per-task state compliance")
    parser.add_argument("--path", default=None, help="Directory to scan")
    parser.add_argument("--check", action="store_true", help="Exit with code 1 if violations are found")
    parser.add_argument("--fix", action="store_true", help="Automatically replace violations with canonical instructions")
    args = parser.parse_args()

    target_dir = args.path
    if not target_dir:
        candidate = os.path.join(".agents")
        if not os.path.isdir(candidate):
            candidate = os.path.join("workspace-template", ".agents")
        target_dir = candidate

    if not os.path.isdir(target_dir):
        print(f"Error: Target directory '{target_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    all_violations: List[str] = []
    files_fixed = 0

    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.endswith(".md"):
                fpath = os.path.join(root, f)
                violations, modified = lint_file(fpath, fix=args.fix)
                all_violations.extend(violations)
                if modified:
                    files_fixed += 1

    if all_violations:
        print(f"Found {len(all_violations)} instruction lint violation(s):")
        for v in all_violations:
            print(f"  {v}")
        if args.fix:
            print(f"Fixed violations across {files_fixed} file(s).")
        if args.check and not args.fix:
            sys.exit(1)
    else:
        print("All instructions adhere to canonical per-task state guidelines.")
        sys.exit(0)


if __name__ == "__main__":
    main()
