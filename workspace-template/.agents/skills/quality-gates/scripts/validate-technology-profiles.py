#!/usr/bin/env python3
"""
validate-technology-profiles.py

Authoritative Technology Profile Validator (P1-36, P1-37, P1-38):
- Validates YAML frontmatter across all profiles in .agents/technology/profiles/ using PyYAML.
- Enforces required metadata:
    - name, category, baselineVersion, lastVerified, reviewAfter
    - preferredVersion, supportedVersions, legacyVersions, prohibitedVersions
    - sources (list of official URLs)
- Enforces freshness policy:
    - reviewAfter must be a valid future ISO date (YYYY-MM-DD).
    - Emits error if profile freshness date is expired.
- Enforces document structure (Scope, Detection Signals, Supported-Version Policy).
- Returns exit code 0 on PASS, 1 on FAIL.
"""

import argparse
from datetime import date, datetime
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Tuple

import yaml

REQUIRED_FIELDS = [
    "name",
    "category",
    "baselineVersion",
    "lastVerified",
    "reviewAfter",
    "preferredVersion",
    "supportedVersions",
    "legacyVersions",
    "prohibitedVersions",
    "sources",
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


def find_profiles_dir(override: str = None) -> Path:
    if override:
        return Path(override).resolve()
    if resolve_workspace is not None:
        try:
            ws = resolve_workspace()
            cand = ws.governance_root / "technology" / "profiles"
            if cand.is_dir():
                return cand
        except Exception:
            pass
    for cand in [Path(".agents/technology/profiles"), Path("workspace-template/.agents/technology/profiles")]:
        if cand.is_dir():
            return cand.resolve()
    return Path(".agents/technology/profiles").resolve()


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str, List[str]]:
    errors: List[str] = []
    if not content.startswith("---"):
        return {}, content, ["Missing starting '---' YAML frontmatter delimiter."]

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content, ["Unclosed '---' YAML frontmatter delimiter."]

    raw_yaml = parts[1]
    body = parts[2]

    try:
        metadata = yaml.safe_load(raw_yaml)
        if not isinstance(metadata, dict):
            return {}, body, ["YAML frontmatter did not parse into a dictionary."]
        return metadata, body, []
    except yaml.YAMLError as ye:
        return {}, body, [f"YAML parse error: {ye}"]


def validate_profile(file_path: Path, expected_category: str, check_date: date) -> List[str]:
    errors: List[str] = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Failed to read file: {e}"]

    metadata, body, parse_errs = parse_frontmatter(content)
    if parse_errs:
        return parse_errs

    # Required fields
    for req in REQUIRED_FIELDS:
        val = metadata.get(req)
        if val is None or val == "":
            errors.append(f"Missing required frontmatter field '{req}'")

    cat = metadata.get("category")
    if cat and cat != expected_category:
        errors.append(f"Frontmatter category '{cat}' does not match directory '{expected_category}'")

    # Validate lists
    for list_field in ["supportedVersions", "legacyVersions", "prohibitedVersions", "sources"]:
        val = metadata.get(list_field)
        if val is not None and not isinstance(val, list):
            errors.append(f"Field '{list_field}' must be a list (got {type(val).__name__})")

    # Freshness validation (P1-36, P1-38)
    review_after_str = metadata.get("reviewAfter")
    if review_after_str:
        try:
            review_after_date = datetime.strptime(str(review_after_str).strip(), "%Y-%m-%d").date()
            if review_after_date < check_date:
                errors.append(
                    f"Profile is expired: reviewAfter date ({review_after_date}) is in the past relative to reference date ({check_date})."
                )
        except ValueError:
            errors.append(f"Invalid ISO format for 'reviewAfter': '{review_after_str}'. Must be YYYY-MM-DD.")

    last_verified_str = metadata.get("lastVerified")
    if last_verified_str:
        try:
            datetime.strptime(str(last_verified_str).strip(), "%Y-%m-%d").date()
        except ValueError:
            errors.append(f"Invalid ISO format for 'lastVerified': '{last_verified_str}'. Must be YYYY-MM-DD.")

    # Check document structure in body
    if not re.search(r"^#\s+.+", body, re.MULTILINE):
        errors.append("Missing top-level H1 header ('# <Title>')")

    for req_section in ["1. Scope", "2. Detection Signals", "3. Supported-Version Policy"]:
        if f"## {req_section}" not in body:
            errors.append(f"Missing required section '## {req_section}'")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate technology profiles (P1-36, P1-37, P1-38)")
    parser.add_argument("--profiles-dir", default=None, help="Path to technology profiles directory")
    parser.add_argument("--reference-date", default=None, help="Reference date for freshness checking (YYYY-MM-DD)")
    args = parser.parse_args()

    profiles_dir = find_profiles_dir(args.profiles_dir)
    if not profiles_dir.is_dir():
        print(f"Error: Profiles directory '{profiles_dir}' not found.", file=sys.stderr)
        sys.exit(1)

    if args.reference_date:
        ref_date = datetime.strptime(args.reference_date, "%Y-%m-%d").date()
    else:
        ref_date = date.today()

    total_checked = 0
    all_errors: Dict[str, List[str]] = {}

    for cat_dir in sorted(profiles_dir.iterdir()):
        if not cat_dir.is_dir():
            continue
        category = cat_dir.name
        for pfile in sorted(cat_dir.glob("*.md")):
            total_checked += 1
            rel_name = f"{category}/{pfile.name}"
            errs = validate_profile(pfile, category, ref_date)
            if errs:
                all_errors[rel_name] = errs

    print(f"Technology Profile Validator: Inspected {total_checked} profiles across '{profiles_dir}' (ref date: {ref_date}).")

    if all_errors:
        print(f"\nFAILED with {sum(len(e) for e in all_errors.values())} error(s) in {len(all_errors)} profile(s):", file=sys.stderr)
        for rel_name, errs in sorted(all_errors.items()):
            print(f"\n  [{rel_name}]:", file=sys.stderr)
            for err in errs:
                print(f"    - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"SUCCESS: All {total_checked} technology profiles are fresh, valid, and conform to multi-tier version policies.")
        sys.exit(0)


if __name__ == "__main__":
    main()
