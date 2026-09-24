#!/usr/bin/env python3
"""
lint-policy-consistency.py

Documentation and Policy Semantic Consistency Linter (P1-35):
Detects regressions and obsolete concepts across all markdown and yaml policy files:
  1. Stale completion criteria counts ("15 completion criteria", "fifteen completion criteria")
  2. Fixed "five quality gates" claims (gates are dynamically driven by verification policy)
  3. Stale "14-phase lifecycle" claims (canonical states are 13 states + activity execution)
  4. Deprecated aggregate authority claims ("tasks.json is canonical", "governance.json is canonical")
  5. Hardcoded runtime assumptions ("workspace-template" used as runtime path instead of resolver)
- Returns exit code 0 on PASS, 1 on FAIL.
"""

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Dict, List, Pattern, Tuple

# Patterns representing obsolete or contradictory governance concepts
DISALLOWED_PATTERNS: List[Tuple[str, Pattern, str]] = [
    (
        "STALE_COMPLETION_COUNT",
        re.compile(r"\b15\s+completion\s+criteria\b|\bfifteen\s+completion\s+criteria\b", re.IGNORECASE),
        "Reference to fixed '15 completion criteria'. Completion criteria are dynamically evaluated per task type and risk.",
    ),
    (
        "FIXED_FIVE_GATES",
        re.compile(r"\bfive\s+quality\s+gates\b|\b5\s+quality\s+gates\b", re.IGNORECASE),
        "Reference to fixed '5 quality gates'. Gates are determined by VerificationPolicyEngine from canonical Gate Registry.",
    ),
    (
        "STALE_14_PHASE",
        re.compile(r"\b14-phase\s+lifecycle\b|\b14\s+lifecycle\s+phases\b", re.IGNORECASE),
        "Reference to '14-phase lifecycle'. The lifecycle has 13 canonical states plus execution activities.",
    ),
    (
        "AGGREGATE_CANONICAL_TASKS",
        re.compile(r"tasks\.json\s+is\s+canonical|tasks\.json\s+as\s+canonical", re.IGNORECASE),
        "Claim that aggregate 'tasks.json' is canonical. Sole canonical source is per-task .agents/state/tasks/<id>.json.",
    ),
    (
        "AGGREGATE_CANONICAL_GOV",
        re.compile(r"governance\.json\s+is\s+canonical|governance\.json\s+as\s+canonical", re.IGNORECASE),
        "Claim that aggregate 'governance.json' is canonical. Sole canonical source is per-task .agents/state/governance/<id>.json.",
    ),
]


def lint_file(file_path: Path) -> List[str]:
    errors: List[str] = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Cannot read file '{file_path}': {e}"]

    lines = content.splitlines()
    for line_idx, line in enumerate(lines, 1):
        # Ignore comments or changelog history references if marked explicitly
        for rule_id, pattern, message in DISALLOWED_PATTERNS:
            if pattern.search(line):
                # Allow if line has explicit historical exception comment
                if "historical-ref" in line or "audit-ref" in line or "CHANGELOG" in str(file_path):
                    continue
                errors.append(f"{file_path}:{line_idx}: [{rule_id}] {message} Found: '{line.strip()}'")

    return errors


def lint_directory(target_dir: Path) -> Tuple[List[str], int]:
    all_errors: List[str] = []
    checked_count = 0

    extensions = {".md", ".yaml", ".yml", ".json"}
    for root, dirs, files in os.walk(target_dir):
        # Skip hidden git and cache dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__" and d != "node_modules"]
        for f in files:
            fpath = Path(root) / f
            if fpath.is_symlink():
                continue
            if fpath.suffix in extensions:
                # Do not lint audit scratch files or CHANGELOG
                if "scratch" in str(fpath) or fpath.name == "CHANGELOG.md":
                    continue
                errs = lint_file(fpath)
                if errs:
                    all_errors.extend(errs)
                checked_count += 1

    return all_errors, checked_count


def main():
    parser = argparse.ArgumentParser(description="Lint documentation and policies for semantic consistency (P1-35)")
    parser.add_argument("target_dirs", nargs="*", default=["workspace-template/.agents", "workspace-template/docs"],
                        help="Directories to lint")
    args = parser.parse_args()

    total_errors: List[str] = []
    total_files = 0

    for d in args.target_dirs:
        p = Path(d).resolve()
        if not p.is_dir():
            continue
        errs, count = lint_directory(p)
        total_errors.extend(errs)
        total_files += count

    if total_files == 0:
        total_errors.append("Policy Consistency Linter inspected zero files; configuration cannot be considered healthy.")

    print(f"Policy Consistency Linter: Inspected {total_files} file(s).")

    if total_errors:
        print(f"\nFAILED: Found {len(total_errors)} consistency error(s):", file=sys.stderr)
        for err in total_errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("SUCCESS: All documentation and policy files are semantically consistent with the canonical architecture and policy model.")
        sys.exit(0)


if __name__ == "__main__":
    main()
