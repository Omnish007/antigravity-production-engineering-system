#!/usr/bin/env python3
"""
generate-manifest.py

Automated manifest generator and parity checker to prevent manifest drift:
1. Scans repository for all tracked files (ignoring git, caches, and archives).
2. Compares disk state against FILE_MANIFEST.md.
3. In --check mode: returns exit code 1 if any drift is detected.
4. In --generate mode: updates FILE_MANIFEST.md with accurate file listings.
"""

import os
import re
import sys
from typing import Dict, List, Set, Tuple

IGNORE_DIRS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "node_modules"}
IGNORE_EXTS = {".pyc", ".pyo", ".zip", ".tar.gz", ".DS_Store"}

DEFAULT_SECTIONS = [
    "## Package-level",
    "## Workspace bridge",
    "## Developer Preferences",
    "## Technology Catalog & Profiles",
    "## Rules",
    "## Skills",
    "## Orchestration",
    "## State",
    "## Templates",
    "## CI/CD",
    "## Requirements",
    "## Project Memory",
]

KNOWN_PURPOSES = {
    "VERSION.md": "Freezes the system specification at version 4.0.0.",
    "CHANGELOG.md": "Documents release history, migrations, and freeze specifications across all versions.",
    "RESEARCH_BASIS.md": "Documents researched official sources, release lines, and architectural baselines.",
    "VALIDATION.md": "Documents comprehensive validation matrix, test results, and adversarial security assessments.",
    "workspace-template/.agents/rules/rule-activation.yaml": "Declarative matrix defining rule activation triggers, stable IDs, and domain mappings.",
    "workspace-template/.agents/rules/RULE_ACTIVATION.md": "Authoritative catalog of all project rules, activation criteria, and precedence levels.",
    "workspace-template/.agents/orchestration/policy-registry.yaml": "Authoritative machine-readable registry of policy domains, canonical owners, and schemas.",
    "workspace-template/.agents/orchestration/lane-policy.yaml": "Authoritative machine-readable execution lane policy governing Fast, Standard, and High-Assurance ceremonies.",
    "workspace-template/.agents/orchestration/antigravity-tool-registry.json": "Authoritative versioned registry of Antigravity platform tools, access modes, and risk levels.",
    "workspace-template/.agents/orchestration/verification-policy.yaml": "Declarative matrix defining mandatory verification gates and evidence requirements per task risk and type.",
    "workspace-template/.agents/skills/governance-enforcement/SKILL.md": "Resolves, records, validates, and enforces task-scoped governance requirements and quality gates.",
    "workspace-template/.agents/orchestration/governance-enforcement-policy.md": "Defines the canonical governance resolution, recording, validation, and completion gate enforcement policy.",
    "workspace-template/.agents/skills/quality-gates/scripts/validate-governance.py": "Automated semantic validator verifying task-scoped governance state, quality gates, evidence, and completion invariants.",
    "workspace-template/.agents/skills/quality-gates/scripts/completion_gate.py": "Authoritative stop condition and completion gate evaluator for governed tasks.",
    "workspace-template/.agents/skills/quality-gates/scripts/validate-agents.py": "Validates agent definitions, frontmatter, tool validity, and least-privilege role boundaries.",
    "workspace-template/.agents/skills/quality-gates/scripts/validate-skills.py": "Validates Antigravity Skills mechanically using PyYAML, checking required sections and naming.",
    "workspace-template/.agents/skills/quality-gates/scripts/validate-control-plane.py": "Verifies control-plane integrity, CODEOWNERS coverage, and cryptographic hashes.",
    "workspace-template/.agents/skills/quality-gates/scripts/lint-policy-consistency.py": "Lints documentation and policies for semantic consistency and prevents obsolete concepts.",
    "workspace-template/.agents/skills/quality-gates/scripts/validate-technology-profiles.py": "Validates technology profile frontmatter, required metadata, and document structure.",
    "workspace-template/.agents/skills/quality-gates/scripts/reconcile-state.py": "Reconciles and detects drift between canonical per-task state and derived aggregates.",
    "workspace-template/.agents/skills/quality-gates/scripts/recover-task.py": "Diagnoses and remediates interrupted tasks using git working tree and event history.",
    "workspace-template/.agents/skills/quality-gates/scripts/lint-state-instructions.py": "Lints agent instructions to ensure writes target canonical per-task state.",
    "workspace-template/.agents/skills/quality-gates/scripts/validate-policy-registry.py": "Validates policy registry integrity, canonical owners, and supporting artifacts.",
    "workspace-template/.agents/skills/quality-gates/scripts/lint-documentation.py": "Lints documentation for tag closures, broken relative links, and heading hierarchy.",
    "workspace-template/.agents/validation/core/__init__.py": "Python package initializer for core governance and verification engine.",
    "workspace-template/.agents/validation/core/workspace_resolver.py": "Deterministic workspace and governance root resolver enforcing explicit sentinels.",
    "workspace-template/.agents/validation/core/verification_policy.py": "Executable verification policy engine implementing canonical gate registry and taxonomy.",
    "workspace-template/.agents/validation/core/governance_core.py": "Authoritative governance evaluation engine enforcing task-scoped stop conditions and completion invariants.",
    "workspace-template/.agents/state/task-record.schema.json": "Strict canonical schema for per-task state records.",
    "workspace-template/.agents/state/governance-record.schema.json": "Strict canonical schema for per-task governance records.",
    "workspace-template/.agents/state/blocker-record.schema.json": "Strict canonical schema for blocker records.",
    "workspace-template/.agents/state/event.schema.json": "Strict canonical schema for task lifecycle and recovery events.",
    "workspace-template/.agents/state/governance.json": "Stores task-scoped governance requirements, quality gate evidence, and completion status.",
    "workspace-template/.agents/state/governance.schema.json": "JSON Schema defining task-scoped governance state and completion gate structures.",
    "workspace-template/.agents/CONTROL_PLANE_MANIFEST.json": "Authoritative SHA-256 integrity manifest for protected control-plane files.",
    "workspace-template/.agents/agents/coordinator.md": "Central engineering coordinator responsible for task decomposition, context routing, subagent delegation, result synthesis, and final governance enforcement.",
}


def get_disk_files(root_dir: str) -> Set[str]:
    disk_files = set()
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Filter out ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]
        for f in filenames:
            ext = os.path.splitext(f)[1]
            if ext in IGNORE_EXTS or f == ".DS_Store":
                continue
            full_path = os.path.join(dirpath, f)
            rel_path = os.path.relpath(full_path, root_dir)
            disk_files.add(rel_path)
    return disk_files


def parse_manifest_sections(manifest_path: str) -> Tuple[List[str], Dict[str, str], Dict[str, str]]:
    """
    Parses manifest returning:
    - section_order: List of section names in order of appearance
    - file_to_section: Map of file path -> section name
    - file_to_purpose: Map of file path -> purpose description
    """
    if not os.path.exists(manifest_path):
        return DEFAULT_SECTIONS, {}, {}

    with open(manifest_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    section_order = []
    file_to_section = {}
    file_to_purpose = {}

    current_section = None
    row_pattern = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|")

    for line in lines:
        line_str = line.strip()
        if line_str.startswith("## "):
            current_section = line_str
            if current_section not in section_order:
                section_order.append(current_section)
        elif current_section:
            match = row_pattern.match(line_str)
            if match:
                path = match.group(1).strip()
                purpose = match.group(2).strip()
                file_to_section[path] = current_section
                file_to_purpose[path] = purpose

    for sec in DEFAULT_SECTIONS:
        if sec not in section_order:
            section_order.append(sec)

    return section_order, file_to_section, file_to_purpose


def categorize_file(path: str) -> str:
    if path.startswith("workspace-template/.agents/agents/"):
        return "## Orchestration"
    if path.startswith("workspace-template/.agents/skills/quality-gates/scripts/"):
        return "## Orchestration"
    if path.startswith("workspace-template/.agents/preferences/"):
        return "## Developer Preferences"
    if path.startswith("workspace-template/.agents/technology/"):
        return "## Technology Catalog & Profiles"
    if path.startswith("workspace-template/.agents/rules/"):
        return "## Rules"
    if path.startswith("workspace-template/.agents/skills/"):
        return "## Skills"
    if path.startswith("workspace-template/.agents/orchestration/"):
        return "## Orchestration"
    if path.startswith("workspace-template/.agents/state/"):
        return "## State"
    if path.startswith("workspace-template/.agents/templates/"):
        return "## Templates"
    if path.startswith("workspace-template/.github/"):
        return "## CI/CD"
    if path.startswith("workspace-template/docs/requirements/"):
        return "## Requirements"
    if path.startswith("workspace-template/docs/"):
        return "## Project Memory"
    if path == "workspace-template/AGENTS.md":
        return "## Workspace bridge"
    return "## Package-level"


def parse_manifest(manifest_path: str) -> Dict[str, str]:
    if not os.path.exists(manifest_path):
        return {}
    with open(manifest_path, "r", encoding="utf-8") as f:
        content = f.read()

    row_pattern = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|", re.MULTILINE)
    manifest_entries = {}
    for match in row_pattern.finditer(content):
        path = match.group(1).strip()
        purpose = match.group(2).strip()
        manifest_entries[path] = purpose
    return manifest_entries


def check_parity(root_dir: str, manifest_path: str) -> bool:
    disk_files = get_disk_files(root_dir)
    manifest_entries = parse_manifest(manifest_path)
    manifest_files = set(manifest_entries.keys())

    missing_on_disk = manifest_files - disk_files
    untracked_on_manifest = disk_files - manifest_files

    has_error = False

    if missing_on_disk:
        has_error = True
        print(f"Error: {len(missing_on_disk)} files listed in manifest do NOT exist on disk:")
        for f in sorted(missing_on_disk):
            print(f"  - [MISSING ON DISK] {f}")

    if untracked_on_manifest:
        has_error = True
        print(f"Error: {len(untracked_on_manifest)} files on disk are NOT listed in manifest:")
        for f in sorted(untracked_on_manifest):
            print(f"  - [UNTRACKED IN MANIFEST] {f}")

    if not has_error:
        print(f"SUCCESS: FILE_MANIFEST.md has 100% parity with disk ({len(disk_files)} files tracked).")
        return True
    return False


def generate_manifest(root_dir: str, manifest_path: str) -> bool:
    disk_files = get_disk_files(root_dir)
    section_order, file_to_section, file_to_purpose = parse_manifest_sections(manifest_path)

    # Group disk files into sections
    section_to_files: Dict[str, List[Tuple[str, str]]] = {sec: [] for sec in section_order}

    for path in sorted(disk_files):
        sec = file_to_section.get(path) or categorize_file(path)
        if sec not in section_to_files:
            section_to_files[sec] = []
            section_order.append(sec)

        purpose = file_to_purpose.get(path)
        if not purpose:
            purpose = KNOWN_PURPOSES.get(path, f"Defines {os.path.basename(path)} specification and implementation.")
        section_to_files[sec].append((path, purpose))

    # Generate markdown content
    lines = [
        "# File Manifest",
        "",
        "Every file listed below is included in this package. Each has one primary responsibility. Update this manifest when the structure changes.",
        "",
    ]

    for sec in section_order:
        files = section_to_files.get(sec, [])
        if not files:
            continue
        lines.append(sec)
        lines.append("")
        lines.append("| Path | Purpose |")
        lines.append("|---|---|")
        for p, purp in files:
            lines.append(f"| `{p}` | {purp} |")
        lines.append("")

    new_content = "\n".join(lines).rstrip() + "\n"

    with open(manifest_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"SUCCESS: Generated {manifest_path} with {len(disk_files)} files across {len(section_order)} sections.")
    return check_parity(root_dir, manifest_path)


def find_package_root(override: str = None) -> str:
    """Discovers the package root directory containing FILE_MANIFEST.md (P1-63)."""
    if override:
        return os.path.abspath(override)
    # 1. Search up from script directory
    cur = os.path.dirname(os.path.abspath(__file__))
    while cur and cur != os.path.dirname(cur):
        if os.path.isfile(os.path.join(cur, "FILE_MANIFEST.md")):
            return cur
        cur = os.path.dirname(cur)
    # 2. Search up from current working directory
    cur = os.getcwd()
    while cur and cur != os.path.dirname(cur):
        if os.path.isfile(os.path.join(cur, "FILE_MANIFEST.md")):
            return cur
        cur = os.path.dirname(cur)
    # 3. Default fallback to cwd
    return os.getcwd()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Root-aware file manifest generator and parity checker (P1-63)")
    parser.add_argument("--root", default=None, help="Root directory of framework package")
    parser.add_argument("--check", action="store_true", help="Check manifest parity without modifying")
    parser.add_argument("--generate", action="store_true", help="Regenerate FILE_MANIFEST.md")
    args = parser.parse_args()

    root_dir = find_package_root(args.root)
    manifest_path = os.path.join(root_dir, "FILE_MANIFEST.md")

    if args.generate:
        success = generate_manifest(root_dir, manifest_path)
        sys.exit(0 if success else 1)
    else:
        # Default or --check
        success = check_parity(root_dir, manifest_path)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
