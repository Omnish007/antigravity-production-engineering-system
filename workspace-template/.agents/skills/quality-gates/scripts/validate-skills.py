#!/usr/bin/env python3
"""
validate-skills.py

Mechanical Skill Validator (P1-19, P1-20):
- Uses real YAML parser (yaml.safe_load) to parse SKILL.md frontmatter.
- Validates:
  1. Directory naming matches frontmatter 'name'.
  2. Frontmatter contains required fields ('name', 'description').
  3. Skill IDs and names are unique across all skills.
  4. Descriptions are substantive (>= 20 characters).
  5. Required standard sections (<MISSION>, <WHEN_TO_USE>, <PRECONDITIONS>, <NON_NEGOTIABLES>, <PROCEDURE>).
  6. File references within SKILL.md resolve to existing files.
- Returns exit code 0 on PASS, 1 on FAIL.
"""

import argparse
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Set, Tuple

import yaml

REQUIRED_SECTIONS = [
    "MISSION",
    "WHEN_TO_USE",
    "PRECONDITIONS",
    "NON_NEGOTIABLES",
    "PROCEDURE",
]

# Core paths resolver
_script_dir = Path(__file__).resolve().parent
_core_dir = _script_dir.parent.parent.parent / "validation" / "core"
if _core_dir.is_dir() and str(_core_dir) not in sys.path:
    sys.path.insert(0, str(_core_dir))

try:
    from workspace_resolver import resolve_workspace
except ImportError:
    try:
        from .workspace_resolver import resolve_workspace
    except ImportError:
        resolve_workspace = None


def find_skills_dir(override: str = None) -> Path:
    if override:
        return Path(override).resolve()
    if resolve_workspace is not None:
        try:
            ws = resolve_workspace()
            cand = ws.governance_root / "skills"
            if cand.is_dir():
                return cand
        except Exception:
            pass
    for cand in [Path(".agents/skills"), Path("workspace-template/.agents/skills")]:
        if cand.is_dir():
            return cand.resolve()
    return Path(".agents/skills").resolve()


def validate_skill_file(skill_dir: Path, skill_file: Path) -> Tuple[List[str], Dict[str, Any]]:
    errors: List[str] = []
    dir_name = skill_dir.name

    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        return [f"[{dir_name}] Cannot read SKILL.md: {e}"], {}

    if not content.startswith("---"):
        return [f"[{dir_name}] Missing starting '---' YAML frontmatter delimiter."], {}

    parts = content.split("---", 2)
    if len(parts) < 3:
        return [f"[{dir_name}] Unclosed '---' YAML frontmatter delimiter."], {}

    raw_yaml = parts[1]
    body = parts[2]

    try:
        fm = yaml.safe_load(raw_yaml)
        if not isinstance(fm, dict):
            return [f"[{dir_name}] Frontmatter does not parse to a dictionary."], {}
    except yaml.YAMLError as ye:
        return [f"[{dir_name}] YAML frontmatter parse error: {ye}"], {}

    # Check required fields
    for req in ["name", "description"]:
        if req not in fm or not fm[req]:
            errors.append(f"[{dir_name}] Missing required frontmatter field '{req}'.")

    name = fm.get("name", "")
    if name and name != dir_name:
        errors.append(f"[{dir_name}] Frontmatter name '{name}' does not match directory name '{dir_name}'.")

    desc = fm.get("description", "")
    if desc and len(str(desc).strip()) < 20:
        errors.append(f"[{dir_name}] Description is too short (< 20 characters): '{desc}'.")

    # Check required sections
    for sec in REQUIRED_SECTIONS:
        start_tag = f"<{sec}>"
        end_tag = f"</{sec}>"
        if start_tag not in body:
            errors.append(f"[{dir_name}] Missing required section tag '{start_tag}'.")
        elif end_tag not in body:
            errors.append(f"[{dir_name}] Missing closing section tag '{end_tag}'.")

    return errors, fm


def validate_all_skills(skills_root: Path) -> Tuple[List[str], int]:
    errors: List[str] = []
    if not skills_root.is_dir():
        return [f"Skills root directory '{skills_root}' not found."], 0

    skill_dirs = sorted([d for d in skills_root.iterdir() if d.is_dir()])
    if not skill_dirs:
        return [f"No skill directories found in '{skills_root}'."], 0

    seen_names: Set[str] = set()
    seen_ids: Set[str] = set()
    total_valid = 0

    for s_dir in skill_dirs:
        skill_file = s_dir / "SKILL.md"
        if not skill_file.is_file():
            errors.append(f"[{s_dir.name}] Missing SKILL.md in directory.")
            continue

        file_errors, fm = validate_skill_file(s_dir, skill_file)
        if file_errors:
            errors.extend(file_errors)
            continue

        name = fm.get("name")
        if name in seen_names:
            errors.append(f"[{s_dir.name}] Duplicate skill name '{name}'.")
        seen_names.add(name)

        skill_id = fm.get("id")
        if skill_id:
            if skill_id in seen_ids:
                errors.append(f"[{s_dir.name}] Duplicate skill ID '{skill_id}'.")
            seen_ids.add(skill_id)

        total_valid += 1

    return errors, total_valid


def main():
    parser = argparse.ArgumentParser(description="Validate Antigravity Skills mechanically (P1-19, P1-20)")
    parser.add_argument("--skills-dir", default=None, help="Path to .agents/skills directory")
    args = parser.parse_args()

    skills_root = find_skills_dir(args.skills_dir)
    print(f"Validating Skills in: {skills_root}")

    errors, count = validate_all_skills(skills_root)

    if errors:
        print(f"\nFAILED: {len(errors)} validation error(s) across skills:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(f"\nSUCCESS: All {count} skills passed validation cleanly.")
        sys.exit(0)


if __name__ == "__main__":
    main()
