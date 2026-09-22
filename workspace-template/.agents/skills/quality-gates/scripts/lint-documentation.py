#!/usr/bin/env python3
"""
lint-documentation.py

Comprehensive markdown and documentation linter.
Validates:
- XML tag pairing and closure (<TAG> ... </TAG>)
- Broken relative markdown links ([label](relative/path))
- Heading hierarchy (H1 -> H2 -> H3)

Usage:
  python3 lint-documentation.py [--path DIR] [--check] [--strict-headings]
"""

import argparse
import os
import re
import sys
from typing import Dict, List

# Known XML tags used throughout rules, skills, and orchestration policies
KNOWN_TAGS = [
    "MISSION", "ROLE", "NON_NEGOTIABLES", "ACTION_SPACE_CONSTRAINTS",
    "READ", "WRITE", "EXECUTE", "DELETE", "NETWORK", "CREDENTIAL", "PRODUCTION",
    "ALLOWED", "PROHIBITED", "APPROVAL_REQUIRED", "TOOL_POLICY", "GENERAL",
    "INSPECTION", "DESTRUCTIVE_OPERATIONS", "SECRETS", "FAILURE", "PROCEDURE",
    "DECISION_RULES", "VERIFICATION_POLICY", "DELIVERABLES", "WHEN_TO_USE",
    "WHEN_NOT_TO_USE", "PRECONDITIONS", "ANTI_PATTERNS", "INSTRUCTION_HIERARCHY",
    "PRIORITIES", "CONTEXT_POLICY", "MEMORY_POLICY", "STATE_POLICY",
    "FAILURE_RECOVERY", "ESCALATION_POLICY", "AGENT_OPERATING_CONTRACT",
    "EVIDENCE_REQUIREMENTS", "SAFETY_CONSTRAINTS"
]


def check_tag_closures(file_path: str, content: str) -> List[str]:
    # Exclude instruction-tag-standard.md which serves as the tag dictionary
    if "instruction-tag-standard.md" in file_path:
        return []

    errors = []
    # Strip fenced code blocks
    sanitized = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    # Strip inline backtick code snippets
    sanitized = re.sub(r"`[^`\n]+`", "", sanitized)

    for tag in KNOWN_TAGS:
        open_tags = len(re.findall(rf"<{tag}>", sanitized))
        close_tags = len(re.findall(rf"</{tag}>", sanitized))
        if open_tags != close_tags:
            errors.append(f"Mismatched tag <{tag}>: {open_tags} opening vs {close_tags} closing tags")

    return errors


def check_relative_links(file_path: str, content: str) -> List[str]:
    errors = []
    base_dir = os.path.dirname(os.path.abspath(file_path))

    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    for match in link_pattern.finditer(content):
        target = match.group(2).strip()
        if (
            target.startswith("http://")
            or target.startswith("https://")
            or target.startswith("mailto:")
            or target.startswith("file://")
            or target.startswith("conversation://")
            or target.startswith("#")
        ):
            continue

        target_path = target.split("#")[0].strip()
        if not target_path:
            continue

        resolved = os.path.normpath(os.path.join(base_dir, target_path))
        if not os.path.exists(resolved):
            errors.append(f"Broken relative link '{target}' -> target '{resolved}' does not exist")

    return errors


def check_heading_hierarchy(content: str) -> List[str]:
    errors = []
    sanitized = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    heading_pattern = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)

    headings = heading_pattern.findall(sanitized)
    if not headings:
        return errors

    prev_level = 0
    for hashes, text in headings:
        level = len(hashes)
        # Disallow extreme skips like H1 directly to H4
        if prev_level > 0 and level > prev_level + 2:
            errors.append(f"Skipped heading level: H{prev_level} to H{level} ('{text}')")
        prev_level = level

    return errors


def lint_markdown(file_path: str, strict_headings: bool = False) -> List[str]:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Failed to read file: {e}"]

    errs = []
    errs.extend(check_tag_closures(file_path, content))
    errs.extend(check_relative_links(file_path, content))
    if strict_headings:
        errs.extend(check_heading_hierarchy(content))
    return errs


def main():
    parser = argparse.ArgumentParser(description="Lint documentation for tag closures, links, and headings")
    parser.add_argument("--path", default=None, help="Root directory to scan for markdown files")
    parser.add_argument("--check", action="store_true", help="Exit with code 1 if errors found")
    parser.add_argument("--strict-headings", action="store_true", help="Enforce strict heading hierarchy")
    args = parser.parse_args()

    scan_dir = args.path or "."
    if not os.path.isdir(scan_dir):
        print(f"Error: Directory '{scan_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    all_errors: Dict[str, List[str]] = {}
    total_files = 0

    for root, _, files in os.walk(scan_dir):
        if any(ignored in root for ignored in ["node_modules", ".git", "venv", ".venv"]):
            continue
        for f in files:
            if f.endswith(".md"):
                total_files += 1
                fpath = os.path.join(root, f)
                errs = lint_markdown(fpath, strict_headings=args.strict_headings)
                if errs:
                    all_errors[fpath] = errs

    print(f"Scanned {total_files} markdown file(s) across '{scan_dir}'.")
    if all_errors:
        print(f"Found issues in {len(all_errors)} file(s):", file=sys.stderr)
        for path, errs in all_errors.items():
            print(f"\n{path}:", file=sys.stderr)
            for e in errs:
                print(f"  - {e}", file=sys.stderr)
        if args.check:
            sys.exit(1)
    else:
        print("[SUCCESS] All documentation files passed linting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
