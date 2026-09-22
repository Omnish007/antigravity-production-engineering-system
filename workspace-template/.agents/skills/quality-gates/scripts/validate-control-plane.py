#!/usr/bin/env python3
"""
validate-control-plane.py

Control-Plane Integrity Validator (P1-34):
- Verifies integrity of all core control-plane components:
  1. Hooks configuration (.agents/hooks.json)
  2. Rule definitions (.agents/rules/*.md)
  3. Skill definitions (.agents/skills/*/SKILL.md)
  4. Agent definitions (.agents/agents/*.md)
  5. Schemas (.agents/state/*.schema.json, .agents/orchestration/*.schema.json)
  6. Core validators (.agents/skills/quality-gates/scripts/*.py, .agents/validation/core/*.py)
  7. Policy registries (.agents/orchestration/policy-registry.yaml, lane-policy.yaml, verification-policy.yaml)
  8. CI workflow files (.github/workflows/*.yml)
  9. Code ownership protections (.github/CODEOWNERS)
- Verifies that .github/CODEOWNERS explicitly covers control-plane directories.
- Supports generating and verifying against CONTROL_PLANE_MANIFEST.json.
- Returns exit code 0 on PASS, 1 on FAIL.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional, Set, Tuple

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


def compute_sha256(filepath: Path) -> str:
    """Compute SHA-256 digest of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def find_roots(project_override: Optional[str] = None) -> Tuple[Path, Path]:
    """Find (project_root, governance_root)."""
    if project_override:
        p = Path(project_override).resolve()
        gov = p / ".agents"
        if not gov.is_dir() and (p / "workspace-template" / ".agents").is_dir():
            gov = p / "workspace-template" / ".agents"
        return p, gov

    if resolve_workspace is not None:
        try:
            ws = resolve_workspace()
            return ws.project_root, ws.governance_root
        except Exception:
            pass

    cand_template = Path("workspace-template").resolve()
    if (cand_template / ".agents").is_dir():
        return cand_template, cand_template / ".agents"

    p = Path(".").resolve()
    return p, p / ".agents"


def collect_control_plane_files(project_root: Path, gov_root: Path) -> Dict[str, Path]:
    """Collect all critical control plane files mapped by their relative path."""
    files: Dict[str, Path] = {}

    def add_file(rel_path: str, abs_path: Path):
        if abs_path.is_file():
            files[rel_path] = abs_path

    def add_glob(base_dir: Path, rel_prefix: str, pattern: str):
        if base_dir.is_dir():
            for p in sorted(base_dir.glob(pattern)):
                if p.is_file() and not p.name.startswith("."):
                    rel = str(p.relative_to(project_root))
                    files[rel] = p

    # 1. Hooks configuration
    add_file(".agents/hooks.json", gov_root / "hooks.json")

    # 2. Rules
    add_glob(gov_root / "rules", ".agents/rules", "*.md")

    # 3. Skills
    add_glob(gov_root / "skills", ".agents/skills", "*/SKILL.md")

    # 4. Agents
    add_glob(gov_root / "agents", ".agents/agents", "*.md")

    # 5. Schemas
    add_glob(gov_root / "state", ".agents/state", "*.schema.json")
    add_glob(gov_root / "orchestration", ".agents/orchestration", "*.schema.json")

    # 6. Validators & scripts
    add_glob(gov_root / "skills" / "quality-gates" / "scripts", ".agents/skills/quality-gates/scripts", "*.py")
    add_glob(gov_root / "validation" / "core", ".agents/validation/core", "*.py")

    # 7. Policy registries
    add_file(".agents/orchestration/policy-registry.yaml", gov_root / "orchestration" / "policy-registry.yaml")
    add_file(".agents/orchestration/lane-policy.yaml", gov_root / "orchestration" / "lane-policy.yaml")
    add_file(".agents/orchestration/verification-policy.yaml", gov_root / "orchestration" / "verification-policy.yaml")

    # 8. Workflows
    add_glob(project_root / ".github" / "workflows", ".github/workflows", "*.yml")
    add_glob(project_root / ".github" / "workflows", ".github/workflows", "*.yaml")

    # 9. CODEOWNERS
    add_file(".github/CODEOWNERS", project_root / ".github" / "CODEOWNERS")

    return files


def verify_codeowners_coverage(project_root: Path) -> List[str]:
    """Verify that .github/CODEOWNERS exists and protects control plane."""
    errors = []
    codeowners_file = project_root / ".github" / "CODEOWNERS"
    if not codeowners_file.is_file():
        return [f"Missing required control-plane protection file: {codeowners_file}"]

    content = codeowners_file.read_text(encoding="utf-8")
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]

    has_agents_rule = any(".agents" in l for l in lines)
    has_github_rule = any(".github" in l for l in lines)

    if not has_agents_rule:
        errors.append("CODEOWNERS does not contain a rule protecting '.agents/**'")
    if not has_github_rule:
        errors.append("CODEOWNERS does not contain a rule protecting '.github/**'")

    return errors


def main():
    parser = argparse.ArgumentParser(description="Validate Antigravity control-plane integrity (P1-34)")
    parser.add_argument("--project-root", default=None, help="Root directory of the project")
    parser.add_argument("--generate-manifest", action="store_true", help="Generate CONTROL_PLANE_MANIFEST.json")
    parser.add_argument("--check-manifest", action="store_true", help="Verify against CONTROL_PLANE_MANIFEST.json")
    args = parser.parse_args()

    project_root, gov_root = find_roots(args.project_root)
    print(f"Control-Plane Validator: Project='{project_root}', Governance='{gov_root}'")

    errors: List[str] = []

    # 1. Verify CODEOWNERS
    co_errs = verify_codeowners_coverage(project_root)
    errors.extend(co_errs)

    # 2. Collect control plane files
    cp_files = collect_control_plane_files(project_root, gov_root)
    if len(cp_files) < 10:
        errors.append(f"Insufficient control-plane files found ({len(cp_files)} files). Expected at least 10.")

    manifest_path = gov_root / "CONTROL_PLANE_MANIFEST.json"

    # Compute hashes
    current_manifest: Dict[str, Any] = {
        "schemaVersion": "1.0.0",
        "description": "Authoritative SHA-256 integrity manifest for Antigravity control-plane files",
        "fileCount": len(cp_files),
        "files": {},
    }

    for rel_path, abs_path in sorted(cp_files.items()):
        digest = compute_sha256(abs_path)
        current_manifest["files"][rel_path] = {
            "sha256": digest,
            "bytes": abs_path.stat().st_size,
        }

    if args.generate_manifest:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(current_manifest, f, indent=2)
            f.write("\n")
        print(f"Generated control-plane integrity manifest with {len(cp_files)} files at '{manifest_path}'.")
        sys.exit(0)

    # If manifest exists or check-manifest requested, verify against it
    if args.check_manifest or manifest_path.is_file():
        if not manifest_path.is_file():
            errors.append(f"Manifest verification requested but '{manifest_path}' does not exist.")
        else:
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    stored = json.load(f)
                stored_files = stored.get("files", {})
                for rel, info in stored_files.items():
                    if rel not in current_manifest["files"]:
                        errors.append(f"Control-plane file '{rel}' in manifest is missing from filesystem.")
                    elif current_manifest["files"][rel]["sha256"] != info.get("sha256"):
                        errors.append(
                            f"Control-plane integrity violation for '{rel}': "
                            f"expected SHA-256 {info.get('sha256')}, got {current_manifest['files'][rel]['sha256']}"
                        )
                for rel in current_manifest["files"]:
                    if rel not in stored_files:
                        errors.append(f"New untracked control-plane file '{rel}' not present in manifest.")
            except Exception as e:
                errors.append(f"Failed to read/parse '{manifest_path}': {e}")

    print(f"Inspected {len(cp_files)} control-plane files.")

    if errors:
        print(f"\nFAILED: {len(errors)} control-plane integrity error(s):", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"SUCCESS: Control-plane integrity verified cleanly across {len(cp_files)} protected files.")
        sys.exit(0)


if __name__ == "__main__":
    main()
