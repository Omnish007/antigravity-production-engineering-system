#!/usr/bin/env python3
"""
validate-policy-registry.py

Validates the integrity of policy-registry.yaml:
- Ensures all canonical owner files, schemas, and supporting artifacts exist on disk.
- Ensures no duplicate policy domains or competing canonical owners.
- Validates required fields across all registered policy entries.

Usage:
  python3 validate-policy-registry.py [--registry-file PATH]
"""

import argparse
import os
import sys
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None


def parse_registry(file_path: str) -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if yaml:
        return yaml.safe_load(content) or {}

    # Simple fallback parser for policy-registry.yaml structure
    data: Dict[str, Any] = {"policies": []}
    current_policy: Dict[str, Any] = {}
    current_list_key = None

    for line in content.splitlines():
        raw = line.rstrip()
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- domain:"):
            if current_policy:
                data["policies"].append(current_policy)
            val = stripped.split(":", 1)[1].strip().strip('"')
            current_policy = {"domain": val, "supportingArtifacts": []}
            current_list_key = None
        elif current_policy:
            if stripped.startswith("canonicalOwner:"):
                current_policy["canonicalOwner"] = stripped.split(":", 1)[1].strip().strip('"')
                current_list_key = None
            elif stripped.startswith("schema:"):
                current_policy["schema"] = stripped.split(":", 1)[1].strip().strip('"')
                current_list_key = None
            elif stripped.startswith("authority:"):
                current_policy["authority"] = stripped.split(":", 1)[1].strip().strip('"')
                current_list_key = None
            elif stripped == "supportingArtifacts:":
                current_list_key = "supportingArtifacts"
            elif stripped.startswith("- ") and current_list_key == "supportingArtifacts":
                item = stripped[2:].strip().strip('"')
                current_policy["supportingArtifacts"].append(item)

    if current_policy:
        data["policies"].append(current_policy)

    return data


def validate_registry(registry_file: str) -> List[str]:
    errors: List[str] = []
    if not os.path.isfile(registry_file):
        return [f"Policy registry file '{registry_file}' not found."]

    base_dir = os.path.dirname(os.path.abspath(registry_file))
    try:
        data = parse_registry(registry_file)
    except Exception as e:
        return [f"Failed to parse policy registry: {e}"]

    policies = data.get("policies", [])
    if not policies:
        return ["Policy registry contains no policies."]

    seen_domains = set()
    seen_owners = set()

    for idx, p in enumerate(policies, 1):
        domain = p.get("domain")
        owner = p.get("canonicalOwner")
        authority = p.get("authority")
        schema = p.get("schema")
        supporting = p.get("supportingArtifacts", [])

        if not domain:
            errors.append(f"Policy #{idx}: Missing required 'domain' field")
            continue

        if domain in seen_domains:
            errors.append(f"Duplicate policy domain: '{domain}'")
        seen_domains.add(domain)

        if not owner:
            errors.append(f"Policy '{domain}': Missing 'canonicalOwner'")
        else:
            if owner in seen_owners:
                errors.append(f"Competing canonical owner: '{owner}' assigned to multiple policies")
            seen_owners.add(owner)

            owner_path = os.path.normpath(os.path.join(base_dir, owner))
            if not os.path.isfile(owner_path):
                errors.append(f"Policy '{domain}': Canonical owner file '{owner}' does not exist (resolved: {owner_path})")

        if not authority:
            errors.append(f"Policy '{domain}': Missing 'authority' description")

        if schema:
            schema_path = os.path.normpath(os.path.join(base_dir, schema))
            if not os.path.isfile(schema_path):
                errors.append(f"Policy '{domain}': Schema file '{schema}' does not exist (resolved: {schema_path})")

        for art in supporting:
            art_path = os.path.normpath(os.path.join(base_dir, art))
            if not os.path.exists(art_path):
                errors.append(f"Policy '{domain}': Supporting artifact '{art}' does not exist (resolved: {art_path})")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate policy registry integrity")
    parser.add_argument("--registry-file", default=None, help="Path to policy-registry.yaml")
    args = parser.parse_args()

    reg_file = args.registry_file
    if not reg_file:
        candidate = os.path.join(".agents", "orchestration", "policy-registry.yaml")
        if not os.path.isfile(candidate):
            candidate = os.path.join("workspace-template", ".agents", "orchestration", "policy-registry.yaml")
        reg_file = candidate

    errors = validate_registry(reg_file)
    if errors:
        print(f"Policy registry validation FAILED with {len(errors)} error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"[SUCCESS] Policy registry '{reg_file}' is valid and all referenced artifacts exist.")
        sys.exit(0)


if __name__ == "__main__":
    main()
