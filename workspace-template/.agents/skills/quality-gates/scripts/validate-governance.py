#!/usr/bin/env python3
"""
validate-governance.py

Automated semantic validator for task-scoped governance records in governance.json.
Enforces a 5-layer validation architecture:

Layer 1: JSON Parsing
  - Validates JSON syntax and basic well-formedness across state files.

Layer 2: JSON Schema Validation
  - Evaluates governance.json directly against governance.schema.json (Draft 2020-12).
  - Uses the jsonschema package if installed, or the built-in Draft 2020-12 schema
    evaluator ensuring complete schema enforcement without external dependency failure.

Layer 3: Semantic & Physical Reference Validation
  - Scans .agents/rules/*.md for defined Rule IDs (<!-- ID: RULE-... -->).
  - Scans .agents/skills/*/SKILL.md for defined Skill IDs (id: SKILL-...).
  - Scans .agents/technology/profiles/ for existing technology profiles.
  - Scans docs/decisions/ for existing ADR IDs.
  - Verifies that all referenced rules, skills, profiles, and ADRs exist on disk.
  - Enforces mandatory security rules (RULE-SEC-001, SKILL-SEC-001) for security/high-risk tasks.
  - Validates required technology profiles for implementation tasks (rejects empty profiles).
  - Validates ADR evaluation for architecture-impacting tasks (rejects silent architectural changes).

Layer 4: Task, Event, Lifecycle & Blocker Consistency
  - Cross-references tasks.json: ensures completed tasks have complete governance.
  - Ensures governance completion requires terminal-eligible task state (GOVERNANCE_CHECK or COMPLETED).
  - Verifies classification alignment between tasks.json and governance.json.
  - Cross-references blockers.json: ensures no active blockers exist for completed tasks.
  - Cross-references events.jsonl: ensures completed tasks contain coherent event history
    (TASK_STARTED present, no unresolved blockers or failures).
  - Flags orphan governance records not tracked in tasks.json.

Layer 5: Completion Eligibility (Grouped Completion Invariants: Groups A–J)
  - Enforces all completion invariants when governanceStatus is "complete":
    1. requiredRules non-empty and verified on disk.
    2. requiredSkills non-empty and verified on disk for implementation tasks.
    3. requiredTechnologyProfiles non-empty and verified on disk for implementation tasks.
    4. relevantAdrs evaluated and verified on disk for architectural/high-risk tasks.
    5. qualityGates non-empty with at least one required gate (rejects zero-gate laundering).
    6. Rejects all-N/A laundering (at least one substantive verification gate).
    7. Passed gates require valid non-empty command, exitCode == 0, valid timestamp, and substantive evidence.
       Rejects fake/dummy/trivial evidence ("trust me", "passed", "works", "dummy", etc.).
    8. not_applicable gates require explicit, non-empty reason strings.
    9. No gate may be failed, blocked, pending, not_configured, or unknown.
    10. Applicable test execution evidenced for behavioral implementation tasks.
    11. Acceptance criteria from tasks.json objectively mapped to satisfied evidence.
    12. Security checks satisfied with substantive evidence for high-risk/security tasks.
    13. Diff review structured record verified (files reviewed, unrelated changes = false, evidence).
    14. Approvals satisfied with documented approver when required.
    15. Memory synchronization completed when required (mandatory for durable knowledge changes).
    16. No active blockers in blockers.json.
    17. completedAt is a valid ISO 8601 timestamp and not in the future.

Returns exit code 0 on PASS, 1 on FAIL or BLOCKED.
"""

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Set, Any, Optional, Tuple

# Ensure core validation package is on sys.path
_script_dir = os.path.dirname(os.path.abspath(__file__))
_core_dir = os.path.join(_script_dir, "..", "..", "..", "validation", "core")
if os.path.isdir(_core_dir) and _core_dir not in sys.path:
    sys.path.insert(0, _core_dir)

try:
    from workspace_resolver import resolve_workspace
    from verification_policy import (
        CANONICAL_TASK_TYPES,
        CANONICAL_GATE_REGISTRY,
        GateKind,
        is_canonical_task_type,
        normalize_task_type,
    )
except ImportError:
    CANONICAL_TASK_TYPES = {
        "simple", "bug", "feature", "complex-feature", "refactor",
        "architecture", "security", "database", "migration", "performance",
        "testing", "deployment", "documentation", "requirements",
        "investigation", "infrastructure",
    }
    CANONICAL_GATE_REGISTRY = {}
    GateKind = None

VALID_GOVERNANCE_STATUSES = {
    "pending",
    "ready",
    "in_progress",
    "verification_required",
    "blocked",
    "failed",
    "complete",
}

# The 7 standardized check statuses
VALID_CHECK_STATUSES = {
    "pending",
    "passed",
    "failed",
    "blocked",
    "not_applicable",
    "not_configured",
    "unknown",
}

# 16 Canonical Task Types (P0-23)
VALID_CLASSIFICATION_TYPES = set(CANONICAL_TASK_TYPES)

IMPLEMENTATION_TYPES = {
    "bug",
    "feature",
    "complex-feature",
    "refactor",
    "database",
    "migration",
    "performance",
    "infrastructure",
    "deployment",
}

BEHAVIORAL_IMPLEMENTATION_TYPES = {
    "bug",
    "bugfix",
    "feature",
    "complex-feature",
    "refactor",
    "testing",
    "test",
}

ARCHITECTURAL_TYPES = {
    "architecture",
    "database",
    "migration",
    "infrastructure",
}

VALID_RISKS = {"low", "medium", "high", "critical"}

RULE_ID_PATTERN = re.compile(r"^RULE-[A-Z0-9_-]+$")
SKILL_ID_PATTERN = re.compile(r"^SKILL-[A-Z0-9_-]+$")
GATE_ID_PATTERN = re.compile(r"^GATE-[A-Z0-9_-]+$")
TASK_ID_PATTERN = re.compile(r"^TASK-[0-9]{3,}$")
ISO_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?$"
)

# Trivial / fake / dummy evidence strings that must be rejected
TRIVIAL_EVIDENCE_STRINGS = {
    "trust me",
    "done",
    "passed",
    "pass",
    "ok",
    "okay",
    "works",
    "working",
    "true",
    "yes",
    "verified",
    "tested",
    "good",
    "looks good",
    "dummy",
    "placeholder",
    "todo",
    "fixme",
    "n/a",
    "na",
    "none",
    "null",
    "test",
    "see output",
    "all good",
}

DUMMY_GATE_IDENTIFIERS = {
    "dummy",
    "placeholder",
    "gate-dummy",
    "test-gate",
    "fake",
}

DUMMY_COMMANDS = {
    "true",
    ":",
    "echo passed",
    "echo pass",
    "echo ok",
    "exit 0",
    "dummy",
}


# =============================================================================
# Helper Utilities
# =============================================================================

def is_fake_or_dummy_evidence(ev: Optional[str]) -> bool:
    """Return True if evidence string is missing, trivial, or hand-waving."""
    if not ev or not isinstance(ev, str):
        return True
    trimmed = ev.strip()
    if not trimmed:
        return True
    lower = trimmed.lower()
    if lower in TRIVIAL_EVIDENCE_STRINGS:
        return True
    if any(re.search(p, lower) for p in [r"\btrust me\b", r"\bworks for me\b", r"\bit works\b", r"\bhand-waving\b", r"\bplaceholder\b", r"\bdummy\b"]):
        return True
    if re.match(r"^(?:trust me|pass|passed|ok|done|test|placeholder|dummy|works|all good)[\.!]?$", lower):
        return True
    if len(trimmed) < 12 and not re.search(r"\d", trimmed):
        return True
    return False


def is_valid_iso_timestamp(ts: Optional[str], check_future: bool = True) -> Tuple[bool, str]:
    """Validate ISO 8601 timestamp format and ensure it is not in the future."""
    if not ts or not isinstance(ts, str):
        return False, "Missing timestamp"
    if not ISO_TIMESTAMP_PATTERN.match(ts):
        return False, f"Timestamp '{ts}' does not match ISO 8601 pattern"

    if check_future:
        try:
            clean_ts = ts
            if clean_ts.endswith("Z"):
                clean_ts = clean_ts[:-1] + "+00:00"
            dt = datetime.fromisoformat(clean_ts)
            now = datetime.now(timezone.utc)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # Allow up to 5 minutes clock skew
            if dt > now + timedelta(minutes=5):
                return False, f"Timestamp '{ts}' is in the future relative to current time"
        except Exception as e:
            return False, f"Failed to parse timestamp '{ts}': {e}"

    return True, ""


# =============================================================================
# Workspace Resolution & Discovery
# =============================================================================

def find_workspace_root(start_path: str) -> str:
    """Traverse upwards or use resolve_workspace to deterministically locate workspace root."""
    try:
        info = resolve_workspace(start_path=start_path)
        return str(info.project_root)
    except Exception:
        pass
    current = os.path.abspath(start_path)
    if os.path.isfile(current):
        current = os.path.dirname(current)

    for _ in range(5):
        if os.path.isdir(os.path.join(current, ".agents")) or os.path.isdir(
            os.path.join(current, "docs")
        ):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent

    return os.getcwd()


def discover_rule_ids(workspace_root: str, errors: Optional[List[str]] = None) -> Set[str]:
    """Scan .agents/rules/*.md for defined Rule IDs."""
    rules_dir = os.path.join(workspace_root, ".agents", "rules")
    rule_ids: Set[str] = set()
    if not os.path.isdir(rules_dir):
        return rule_ids

    id_regex = re.compile(r"<!--\s*ID:\s*(RULE-[A-Z0-9_-]+)\s*-->")
    for fname in sorted(os.listdir(rules_dir)):
        if fname.endswith(".md"):
            if fname in ["README.md", "RULE_ACTIVATION.md"]:
                continue
            fpath = os.path.join(rules_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    content = f.read(1024)
                    match = id_regex.search(content)
                    if match:
                        rule_ids.add(match.group(1))
                    else:
                        if errors is not None:
                            errors.append(f"Corrupt rule metadata: Rule file '{fname}' is missing valid Rule ID comment tag <!-- ID: RULE-... -->.")
            except Exception as e:
                if errors is not None:
                    errors.append(f"Fatal: Failed to read rule file '{fname}': {e}")
    return rule_ids


def discover_skill_ids(workspace_root: str, errors: Optional[List[str]] = None) -> Set[str]:
    """Scan .agents/skills/*/SKILL.md for defined Skill IDs."""
    skills_dir = os.path.join(workspace_root, ".agents", "skills")
    skill_ids: Set[str] = set()
    if not os.path.isdir(skills_dir):
        return skill_ids

    id_regex = re.compile(r"^id:\s*(SKILL-[A-Z0-9_-]+)", re.MULTILINE)
    for skill_name in sorted(os.listdir(skills_dir)):
        skill_path = os.path.join(skills_dir, skill_name)
        if os.path.isdir(skill_path):
            skill_md = os.path.join(skill_path, "SKILL.md")
            if os.path.isfile(skill_md):
                try:
                    with open(skill_md, "r", encoding="utf-8") as f:
                        content = f.read(1024)
                        match = id_regex.search(content)
                        if match:
                            skill_ids.add(match.group(1))
                        else:
                            if errors is not None:
                                errors.append(f"Corrupt skill metadata: Skill file '{skill_name}/SKILL.md' is missing valid id frontmatter.")
                except Exception as e:
                    if errors is not None:
                        errors.append(f"Fatal: Failed to read skill file '{skill_name}/SKILL.md': {e}")
    return skill_ids


def discover_technology_profiles(workspace_root: str, errors: Optional[List[str]] = None) -> Set[str]:
    """Scan .agents/technology/profiles/ for existing profile names and paths."""
    profiles_dir = os.path.join(workspace_root, ".agents", "technology", "profiles")
    profiles: Set[str] = set()
    if not os.path.isdir(profiles_dir):
        return profiles

    for root, _, files in os.walk(profiles_dir):
        for fname in files:
            if fname.endswith(".md"):
                rel_path = os.path.relpath(os.path.join(root, fname), profiles_dir)
                profiles.add(rel_path)
                if rel_path.endswith(".md"):
                    profiles.add(rel_path[:-3])
                base = os.path.basename(fname)
                profiles.add(base)
                if base.endswith(".md"):
                    profiles.add(base[:-3])
    return profiles


def discover_adrs(workspace_root: str, errors: Optional[List[str]] = None) -> Set[str]:
    """P0-29: Scan docs/decisions/ and require registration in INDEX.md."""
    decisions_dir = os.path.join(workspace_root, "docs", "decisions")
    adrs: Set[str] = set()
    if not os.path.isdir(decisions_dir):
        return adrs

    index_path = os.path.join(decisions_dir, "INDEX.md")
    registered_ids: Set[str] = set()
    if os.path.isfile(index_path):
        try:
            with open(index_path, "r", encoding="utf-8") as f:
                for line in f:
                    for m in re.findall(r"ADR-[0-9]{3,}", line):
                        registered_ids.add(m)
        except Exception as e:
            if errors is not None:
                errors.append(f"Corrupt ADR index: Failed to read docs/decisions/INDEX.md: {e}")

    # Map files on disk
    adr_file_regex = re.compile(r"^(?:ADR-)?([0-9]{3,})")
    disk_files: Dict[str, str] = {}
    for fname in sorted(os.listdir(decisions_dir)):
        if fname.endswith(".md") and fname != "INDEX.md":
            match = adr_file_regex.match(fname)
            if match:
                canon_id = f"ADR-{match.group(1)}"
                disk_files[canon_id] = fname

    # Only registered ADRs that also exist on disk are considered valid
    for reg_id in registered_ids:
        if reg_id in disk_files:
            adrs.add(reg_id)
            num = reg_id.split("-")[1]
            adrs.add(num)
            fname = disk_files[reg_id]
            adrs.add(fname)
            adrs.add(fname[:-3])

    return adrs


def load_active_blockers(workspace_root: str, errors: Optional[List[str]] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Load active blockers from .agents/state/blockers.json and .agents/state/blockers/*.json mapped by taskId."""
    active_by_task: Dict[str, List[Dict[str, Any]]] = {}
    blockers_path = os.path.join(workspace_root, ".agents", "state", "blockers.json")
    if os.path.isfile(blockers_path):
        try:
            with open(blockers_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                for b in data.get("active", []):
                    if isinstance(b, dict):
                        t_id = b.get("taskId")
                        if t_id:
                            active_by_task.setdefault(t_id, []).append(b)
                        else:
                            active_by_task.setdefault("__global__", []).append(b)
        except Exception as e:
            if errors is not None:
                errors.append(f"Fatal: Failed to parse blockers file '{blockers_path}': {e}")

    # Also check per-task blockers directory
    b_dir = os.path.join(workspace_root, ".agents", "state", "blockers")
    if os.path.isdir(b_dir):
        for fname in sorted(os.listdir(b_dir)):
            if fname.endswith(".json"):
                b_file = os.path.join(b_dir, fname)
                try:
                    with open(b_file, "r", encoding="utf-8") as f:
                        b_data = json.load(f)
                        b_items = b_data.get("active", [b_data]) if isinstance(b_data, dict) else b_data
                        if isinstance(b_items, list):
                            for b in b_items:
                                if isinstance(b, dict) and b.get("status") != "resolved":
                                    t_id = b.get("taskId")
                                    if t_id:
                                        active_by_task.setdefault(t_id, []).append(b)
                                    else:
                                        active_by_task.setdefault("__global__", []).append(b)
                except Exception as e:
                    if errors is not None:
                        errors.append(f"Fatal: Failed to parse per-task blocker file '{b_file}': {e}")
    return active_by_task


def load_events(workspace_root: str, errors: Optional[List[str]] = None, validate_schema: bool = True) -> List[Dict[str, Any]]:
    """Load and schema-validate events from .agents/state/events.jsonl and .agents/state/events/*.jsonl."""
    events: List[Dict[str, Any]] = []
    events_file = os.path.join(workspace_root, ".agents", "state", "events.jsonl")

    events_schema = None
    if validate_schema:
        schema_path = os.path.join(workspace_root, ".agents", "state", "events.schema.json")
        if os.path.isfile(schema_path):
            try:
                with open(schema_path, "r", encoding="utf-8") as sf:
                    events_schema = json.load(sf)
            except Exception as e:
                if errors is not None:
                    errors.append(f"Fatal: Failed to parse events schema '{schema_path}': {e}")

    task_sequences: Dict[str, int] = {}

    def process_event_line(line_str: str, source_label: str, line_no: int):
        try:
            ev = json.loads(line_str)
        except Exception as e:
            if errors is not None:
                errors.append(f"Fatal: Failed to parse event JSON in '{source_label}' line {line_no}: {e}")
            return

        if not isinstance(ev, dict):
            if errors is not None:
                errors.append(f"Event in '{source_label}' line {line_no} must be a JSON object.")
            return

        # Schema validation
        if events_schema:
            schema_errs = validate_against_json_schema(ev, events_schema, schema_root=events_schema, path=f"{source_label}:{line_no}")
            if schema_errs and errors is not None:
                errors.extend(schema_errs)

        # Monotonic sequence validation if sequence is present
        seq = ev.get("sequence")
        t_id = ev.get("taskId") or "__global__"
        if isinstance(seq, int):
            prev_seq = task_sequences.get(t_id)
            if prev_seq is not None and seq <= prev_seq:
                if errors is not None:
                    errors.append(f"Event sequence violation in '{source_label}' line {line_no}: sequence {seq} is not greater than previous sequence {prev_seq} for task '{t_id}'.")
            task_sequences[t_id] = seq

        events.append(ev)

    if os.path.isfile(events_file):
        try:
            with open(events_file, "r", encoding="utf-8") as f:
                for line_no, line in enumerate(f, 1):
                    line_str = line.strip()
                    if line_str:
                        process_event_line(line_str, "events.jsonl", line_no)
        except Exception as e:
            if errors is not None:
                errors.append(f"Fatal: Failed to read events file '{events_file}': {e}")

    # Also check per-task events directory
    ev_dir = os.path.join(workspace_root, ".agents", "state", "events")
    if os.path.isdir(ev_dir):
        for fname in sorted(os.listdir(ev_dir)):
            if fname.endswith(".jsonl") or fname.endswith(".json"):
                ev_file = os.path.join(ev_dir, fname)
                try:
                    with open(ev_file, "r", encoding="utf-8") as f:
                        for line_no, line in enumerate(f, 1):
                            line_str = line.strip()
                            if line_str:
                                process_event_line(line_str, fname, line_no)
                except Exception as e:
                    if errors is not None:
                        errors.append(f"Fatal: Failed to read per-task event file '{ev_file}': {e}")

    return events


def load_stack_config(workspace_root: str, errors: Optional[List[str]] = None) -> Dict[str, Any]:
    """Load tech stack configuration from .agents/state/stack.json."""
    stack_path = os.path.join(workspace_root, ".agents", "state", "stack.json")
    if not os.path.isfile(stack_path):
        return {}

    try:
        with open(stack_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        if errors is not None:
            errors.append(f"Fatal: Failed to parse stack configuration '{stack_path}': {e}")
        return {}


# =============================================================================
# Layer 2: Real JSON Schema Validation
# =============================================================================

def validate_against_json_schema(
    instance: Any, schema: Dict[str, Any], schema_root: Optional[Dict[str, Any]] = None, path: str = "root"
) -> List[str]:
    """
    Evaluates instance against a JSON Schema (Draft 2020-12).
    Uses the official jsonschema package if available, or falls back to
    this comprehensive recursive schema validator.
    """
    errors: List[str] = []
    if schema_root is None:
        schema_root = schema

    # Resolve $ref if present
    if "$ref" in schema:
        ref_path = schema["$ref"]
        if ref_path.startswith("#/$defs/"):
            def_name = ref_path[len("#/$defs/") :]
            resolved = schema_root.get("$defs", {}).get(def_name)
            if resolved:
                return validate_against_json_schema(instance, resolved, schema_root, path)
            else:
                return [f"{path}: Unresolved $ref '{ref_path}' in schema."]

    # Type check
    expected_type = schema.get("type")
    if expected_type:
        types = [expected_type] if isinstance(expected_type, str) else expected_type
        type_matched = False
        for t in types:
            if t == "object" and isinstance(instance, dict):
                type_matched = True
            elif t == "array" and isinstance(instance, list):
                type_matched = True
            elif t == "string" and isinstance(instance, str):
                type_matched = True
            elif t == "integer" and isinstance(instance, int) and not isinstance(instance, bool):
                type_matched = True
            elif t == "number" and (isinstance(instance, (int, float)) and not isinstance(instance, bool)):
                type_matched = True
            elif t == "boolean" and isinstance(instance, bool):
                type_matched = True
            elif t == "null" and instance is None:
                type_matched = True
        if not type_matched:
            errors.append(f"{path}: Expected type '{expected_type}', got '{type(instance).__name__}'.")
            return errors

    # Const check
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{path}: Expected const value '{schema['const']}', got '{instance}'.")

    # Enum check
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{path}: Value '{instance}' is not one of allowed enum values: {schema['enum']}.")

    # String pattern check
    if isinstance(instance, str) and "pattern" in schema:
        if not re.search(schema["pattern"], instance):
            errors.append(f"{path}: String '{instance}' does not match pattern '{schema['pattern']}'.")

    # Object validation
    if isinstance(instance, dict):
        required_props = schema.get("required", [])
        for req in required_props:
            if req not in instance:
                errors.append(f"{path}: Missing required property '{req}'.")

        properties = schema.get("properties", {})
        additional_allowed = schema.get("additionalProperties", True)

        for k, v in instance.items():
            if k in properties:
                sub_errs = validate_against_json_schema(v, properties[k], schema_root, f"{path}.{k}")
                errors.extend(sub_errs)
            elif not additional_allowed:
                errors.append(f"{path}: Additional property '{k}' is not allowed by schema.")

    # Array validation
    if isinstance(instance, list):
        items_schema = schema.get("items")
        if items_schema:
            for idx, item in enumerate(instance):
                sub_errs = validate_against_json_schema(item, items_schema, schema_root, f"{path}[{idx}]")
                errors.extend(sub_errs)

    # oneOf validation
    if "oneOf" in schema:
        matches = 0
        for opt_schema in schema["oneOf"]:
            opt_errs = validate_against_json_schema(instance, opt_schema, schema_root, path)
            if not opt_errs:
                matches += 1
        if matches != 1:
            errors.append(f"{path}: Value does not match exactly one of the oneOf schemas (matches={matches}).")

    return errors


def run_layer2_schema_validation(gov_data: Any, schema_path: str) -> List[str]:
    """Execute Layer 2 JSON Schema validation."""
    if not os.path.isfile(schema_path):
        return [f"Layer 2 Schema Error: Schema file not found at '{schema_path}'."]

    try:
        with open(schema_path, "r", encoding="utf-8") as sf:
            schema = json.load(sf)
    except Exception as e:
        return [f"Layer 2 Schema Error: Failed to parse schema '{schema_path}': {e}"]

    # Try official jsonschema if available
    try:
        import jsonschema
        validator = jsonschema.Draft202012Validator(schema)
        errors = []
        for err in sorted(validator.iter_errors(gov_data), key=lambda e: e.path):
            p = ".".join(str(elem) for elem in err.path) or "root"
            errors.append(f"Schema violation at {p}: {err.message}")
        return errors
    except ImportError:
        # Standalone Draft 2020-12 schema evaluator
        return validate_against_json_schema(gov_data, schema)


# =============================================================================
# Full 5-Layer Governance Validator
# =============================================================================

def validate_governance_layers(
    gov_data: Dict[str, Any],
    tasks_data: Dict[str, Any],
    gov_filepath: str,
    workspace_root: Optional[str] = None,
    schema_path: Optional[str] = None,
) -> Tuple[List[str], Dict[str, Any]]:
    """
    Executes Layers 2 through 5 and returns (errors, metrics).
    """
    errors: List[str] = []
    metrics: Dict[str, Any] = {
        "records_count": 0,
        "completed_count": 0,
        "gates_evaluated": 0,
        "layer_failures": {},
    }

    if workspace_root is None:
        workspace_root = find_workspace_root(gov_filepath)

    if schema_path is None:
        schema_path = os.path.join(os.path.dirname(gov_filepath), "governance.schema.json")
        if not os.path.isfile(schema_path):
            schema_path = os.path.join(workspace_root, ".agents", "state", "governance.schema.json")

    # -------------------------------------------------------------------------
    # Layer 2: JSON Schema Validation
    # -------------------------------------------------------------------------
    schema_errors = run_layer2_schema_validation(gov_data, schema_path)
    if schema_errors:
        errors.extend(schema_errors)
        metrics["layer_failures"]["Layer 2 (JSON Schema)"] = len(schema_errors)
        if not isinstance(gov_data, dict) or not isinstance(gov_data.get("records"), list):
            return errors, metrics

    records = gov_data.get("records", [])
    metrics["records_count"] = len(records)

    # -------------------------------------------------------------------------
    # Layer 3 & 4 Preparations: Discoveries & State Cross-references
    # -------------------------------------------------------------------------
    known_rules = discover_rule_ids(workspace_root, errors)
    known_skills = discover_skill_ids(workspace_root, errors)
    known_profiles = discover_technology_profiles(workspace_root, errors)
    known_adrs = discover_adrs(workspace_root, errors)
    active_blockers = load_active_blockers(workspace_root, errors)
    events = load_events(workspace_root, errors)
    stack_config = load_stack_config(workspace_root, errors)

    tasks_list = tasks_data.get("tasks", []) if isinstance(tasks_data, dict) else []
    tasks_by_id = {t.get("id"): t for t in tasks_list if isinstance(t, dict) and "id" in t}

    seen_gov_task_ids: Set[str] = set()

    for idx, rec in enumerate(records):
        if not isinstance(rec, dict):
            continue

        task_id = rec.get("taskId")
        if not task_id or not isinstance(task_id, str):
            continue

        if task_id in seen_gov_task_ids:
            errors.append(f"Duplicate taskId '{task_id}' in {gov_filepath}.")
        seen_gov_task_ids.add(task_id)

        status = rec.get("governanceStatus")
        clf = rec.get("classification", {})
        c_type = clf.get("type") if isinstance(clf, dict) else None
        c_risk = clf.get("risk") if isinstance(clf, dict) else None

        # ---------------------------------------------------------------------
        # Layer 3: Semantic & Physical Reference Validation
        # ---------------------------------------------------------------------
        rules = rec.get("requiredRules", [])
        if isinstance(rules, list):
            for r in rules:
                if isinstance(r, str):
                    if not RULE_ID_PATTERN.match(r):
                        errors.append(f"Task '{task_id}' has structurally invalid Rule ID '{r}'.")
                    elif r not in known_rules:
                        errors.append(
                            f"Task '{task_id}' references non-existent Rule ID '{r}' (not found in .agents/rules/)."
                        )

        skills = rec.get("requiredSkills", [])
        if isinstance(skills, list):
            for s in skills:
                if isinstance(s, str):
                    if not SKILL_ID_PATTERN.match(s):
                        errors.append(f"Task '{task_id}' has structurally invalid Skill ID '{s}'.")
                    elif s not in known_skills:
                        errors.append(
                            f"Task '{task_id}' references non-existent Skill ID '{s}' (not found in .agents/skills/*/SKILL.md)."
                        )

        profiles = rec.get("requiredTechnologyProfiles", [])
        if isinstance(profiles, list):
            for p in profiles:
                if isinstance(p, str) and p != "NOT_APPLICABLE" and p not in known_profiles:
                    errors.append(
                        f"Task '{task_id}' references non-existent Technology Profile '{p}' (not found in .agents/technology/profiles/)."
                    )

        adrs = rec.get("relevantAdrs", [])
        if isinstance(adrs, list):
            for a in adrs:
                if isinstance(a, str) and a not in known_adrs:
                    errors.append(
                        f"Task '{task_id}' references non-existent ADR '{a}' (not found in docs/decisions/)."
                    )

        # Mandatory security domain binding
        if c_type == "security" or c_risk in {"high", "critical"}:
            if "RULE-SEC-001" not in rules:
                errors.append(
                    f"Task '{task_id}' is classified as {c_type}/{c_risk} but omits mandatory 'RULE-SEC-001'."
                )
            if "SKILL-SEC-001" not in skills:
                errors.append(
                    f"Task '{task_id}' is classified as {c_type}/{c_risk} but omits mandatory 'SKILL-SEC-001'."
                )

        # ---------------------------------------------------------------------
        # Layer 4: Task, Event & Lifecycle Consistency & Blocker Prevention
        # ---------------------------------------------------------------------
        matching_task = tasks_by_id.get(task_id) if tasks_by_id else None
        if tasks_by_id and not matching_task:
            errors.append(
                f"Governance record '{task_id}' does not exist in tasks.json (orphan governance record)."
            )

        if matching_task:
            t_status = matching_task.get("status")
            t_type = matching_task.get("type")

            # Classification parity check
            if t_type and c_type and t_type != c_type:
                aliases = {("bug", "bugfix"), ("bugfix", "bug"), ("docs", "documentation"), ("documentation", "docs")}
                if (t_type, c_type) not in aliases:
                    errors.append(
                        f"Contradictory classification: Task '{task_id}' is type '{t_type}' in tasks.json but '{c_type}' in governance.json."
                    )

            # Circular bypass prevention: governance cannot be marked complete while task is still in-flight
            if status == "complete" and t_status not in {"GOVERNANCE_CHECK", "COMPLETED"}:
                errors.append(
                    f"Task '{task_id}' has governanceStatus 'complete' but task status in tasks.json is '{t_status}' (must reach GOVERNANCE_CHECK before completion)."
                )

        # Blocker check
        task_blockers = active_blockers.get(task_id, [])
        global_blockers = active_blockers.get("__global__", [])
        all_relevant_blockers = task_blockers + global_blockers
        if status == "complete" and all_relevant_blockers:
            b_ids = [b.get("id") for b in all_relevant_blockers]
            errors.append(
                f"Task '{task_id}' cannot reach complete governance while active blocker(s) {b_ids} remain unresolved."
            )

        # Event history cross-check for completed tasks
        if status == "complete" or (matching_task and matching_task.get("status") == "COMPLETED"):
            task_events = [e for e in events if e.get("taskId") == task_id]
            if not task_events:
                errors.append(
                    f"Task '{task_id}' is marked completed/complete but has no execution event history in events.jsonl or events directory."
                )
            else:
                has_started = any(e.get("event") == "TASK_STARTED" for e in task_events)
                if not has_started:
                    errors.append(
                        f"Task '{task_id}' is marked completed/complete but event history contains no TASK_STARTED event."
                    )
                has_completed = any(e.get("event") == "TASK_COMPLETED" for e in task_events)
                if not has_completed:
                    errors.append(
                        f"Task '{task_id}' is marked completed/complete but event history contains no TASK_COMPLETED event."
                    )

                # Check for unrecovered failures or unresolved blockers in event stream
                last_blocking_event_idx = -1
                last_unblock_event_idx = -1
                last_failure_idx = -1
                last_recovery_idx = -1

                for e_idx, e in enumerate(task_events):
                    ev_type = e.get("event")
                    if ev_type in {"TASK_BLOCKED", "BLOCKER_RECORDED"}:
                        last_blocking_event_idx = e_idx
                    elif ev_type in {"BLOCKER_RESOLVED"}:
                        last_unblock_event_idx = e_idx
                    elif ev_type in {"TASK_FAILED", "VERIFICATION_FAILED"}:
                        last_failure_idx = e_idx
                    elif ev_type in {"RECOVERY_ATTEMPTED", "RETRY_RECORDED", "VERIFICATION_PASSED"}:
                        last_recovery_idx = e_idx

                if last_blocking_event_idx > last_unblock_event_idx:
                    errors.append(
                        f"Task '{task_id}' event history records blocking event without subsequent BLOCKER_RESOLVED."
                    )
                if last_failure_idx > last_recovery_idx:
                    errors.append(
                        f"Task '{task_id}' event history records failure event without subsequent recovery/retry."
                    )

        # ---------------------------------------------------------------------
        # Layer 5: Completion Eligibility (Grouped Completion Invariants: Groups A–J)
        # ---------------------------------------------------------------------
        gates = rec.get("qualityGates", [])
        if isinstance(gates, list):
            metrics["gates_evaluated"] += len(gates)

        if status == "complete":
            metrics["completed_count"] += 1

            # 1. Required rules non-empty
            if not rules:
                errors.append(f"Task '{task_id}' is marked 'complete' but has empty 'requiredRules'.")

            # 2. Required skills non-empty for implementation tasks
            if c_type in IMPLEMENTATION_TYPES and not skills:
                errors.append(
                    f"Task '{task_id}' is an implementation task ({c_type}) but has empty 'requiredSkills'."
                )

            # 3. Technology profile resolution
            if c_type in IMPLEMENTATION_TYPES:
                if not profiles or profiles == ["NOT_APPLICABLE"]:
                    errors.append(
                        f"Task '{task_id}' is an implementation task ({c_type}) but has empty/unresolved 'requiredTechnologyProfiles'."
                    )

            # 4. ADR evaluation for architecture-impacting tasks
            if (c_type in ARCHITECTURAL_TYPES or c_risk in {"high", "critical"}) and not adrs:
                errors.append(
                    f"Task '{task_id}' is architectural/high-risk ({c_type}/{c_risk}) but has empty 'relevantAdrs' (silent architectural change)."
                )

            # 5. Quality gates non-empty
            if not gates:
                errors.append(f"Task '{task_id}' is marked 'complete' but has zero 'qualityGates'.")
            else:
                has_required_gate = False
                all_na = True
                has_test_execution = False

                for g_idx, gate in enumerate(gates):
                    if not isinstance(gate, dict):
                        continue
                    g_id = str(gate.get("id", f"GATE-{g_idx}"))
                    g_name = str(gate.get("name", f"gate-{g_idx}"))
                    g_status = gate.get("status")
                    g_required = gate.get("required", True)

                    # Reject dummy gate identifiers
                    if g_id.lower() in DUMMY_GATE_IDENTIFIERS or g_name.lower() in DUMMY_GATE_IDENTIFIERS:
                        errors.append(
                            f"Task '{task_id}' quality gate '{g_id}' / '{g_name}' is a dummy/placeholder gate."
                        )

                    if g_required:
                        has_required_gate = True

                    if g_status != "not_applicable":
                        all_na = False

                    # Fail-closed: No gate may be failed, blocked, pending, not_configured, or unknown
                    if g_status in {"failed", "blocked", "pending", "not_configured", "unknown"}:
                        errors.append(
                            f"Task '{task_id}' is marked 'complete' but quality gate '{g_name}' is '{g_status}'."
                        )

                    # Passed gates require command, exitCode == 0, timestamp, and substantive evidence
                    if g_status == "passed":
                        ev = gate.get("evidence")
                        if is_fake_or_dummy_evidence(ev):
                            errors.append(
                                f"Task '{task_id}' passed quality gate '{g_name}' without substantive evidence (found trivial/hand-waving string: '{ev}')."
                            )

                        cmd = gate.get("command")
                        if not cmd or not isinstance(cmd, str) or not cmd.strip():
                            errors.append(
                                f"Task '{task_id}' passed quality gate '{g_name}' without an executed command."
                            )
                        elif cmd.strip().lower() in DUMMY_COMMANDS:
                            errors.append(
                                f"Task '{task_id}' passed quality gate '{g_name}' with dummy command '{cmd}'."
                            )

                        exit_code = gate.get("exitCode")
                        if exit_code is None or exit_code != 0:
                            errors.append(
                                f"Task '{task_id}' passed quality gate '{g_name}' with non-zero or missing exit code ({exit_code})."
                            )

                        ts = gate.get("timestamp")
                        ts_valid, ts_err = is_valid_iso_timestamp(ts, check_future=True)
                        if not ts_valid:
                            errors.append(
                                f"Task '{task_id}' passed quality gate '{g_name}' with invalid timestamp: {ts_err}."
                            )

                        # P0-27: Structured gate kind check (no keyword substring matching)
                        g_kind = gate.get("kind") or CANONICAL_GATE_REGISTRY.get(g_name, {}).get("kind")
                        if g_kind == "test" or (GateKind and g_kind == GateKind.TEST) or g_name in {"test", "testing", "migrationTest", "benchmark", "smokeTest", "dryRun"}:
                            has_test_execution = True

                    # P0-25: N/A gates require explicit non-empty reason and applicabilityEvidence
                    if g_status == "not_applicable":
                        reason = gate.get("reason")
                        if not reason or not isinstance(reason, str) or not reason.strip():
                            errors.append(
                                f"Task '{task_id}' marked quality gate '{g_name}' as 'not_applicable' without an explicit reason."
                            )
                        app_ev = gate.get("applicabilityEvidence") or gate.get("evidenceRef") or gate.get("evidence")
                        if not app_ev and (not reason or len(reason.strip()) < 10):
                            errors.append(
                                f"Task '{task_id}' marked quality gate '{g_name}' as 'not_applicable' without required applicability evidence or substantive justification."
                            )

                # Rejects zero required gates
                if not has_required_gate:
                    errors.append(
                        f"Task '{task_id}' is marked 'complete' but has zero required quality gates."
                    )

                # Rejects all-N/A laundering
                if all_na:
                    errors.append(
                        f"Task '{task_id}' is marked 'complete' but all quality gates are 'not_applicable' (verification laundering)."
                    )

                # 6. Applicable tests check for behavioral implementation tasks
                if c_type in BEHAVIORAL_IMPLEMENTATION_TYPES and not has_test_execution:
                    errors.append(
                        f"Task '{task_id}' is a behavioral implementation task ({c_type}) but has no passing test execution gate."
                    )

            # 7. Acceptance criteria mapping check
            if matching_task:
                task_ac = matching_task.get("acceptanceCriteria", [])
                if isinstance(task_ac, list) and task_ac:
                    gov_ac_ev = rec.get("acceptanceCriteriaEvidence", [])
                    gov_ev_reqs = rec.get("evidenceRequirements", [])

                    # Map evidence by criterion description
                    ev_map = {}
                    if isinstance(gov_ac_ev, list):
                        for item in gov_ac_ev:
                            if isinstance(item, dict) and "criterion" in item:
                                ev_map[item["criterion"]] = item
                    if isinstance(gov_ev_reqs, list):
                        for item in gov_ev_reqs:
                            if isinstance(item, dict) and "description" in item:
                                ev_map[item["description"]] = item

                    for ac_item in task_ac:
                        ev_entry = ev_map.get(ac_item)
                        if not ev_entry:
                            errors.append(
                                f"Task '{task_id}' acceptance criterion '{ac_item}' has no objective evidence mapping in governance record."
                            )
                        else:
                            st = ev_entry.get("status")
                            ev_text = ev_entry.get("evidence")
                            if st not in {"satisfied", "passed"}:
                                errors.append(
                                    f"Task '{task_id}' acceptance criterion '{ac_item}' status is '{st}' (must be 'satisfied')."
                                )
                            elif is_fake_or_dummy_evidence(ev_text):
                                errors.append(
                                    f"Task '{task_id}' acceptance criterion '{ac_item}' lacks substantive evidence."
                                )

            # 8. Security checks enforcement
            sec_checks = rec.get("securityChecks", [])
            if (c_type == "security" or c_risk in {"high", "critical"}) and not sec_checks:
                errors.append(
                    f"Task '{task_id}' is high-risk/security ({c_type}/{c_risk}) but has zero security checks recorded."
                )

            for s_idx, sc in enumerate(sec_checks):
                if isinstance(sc, dict):
                    s_name = sc.get("name", f"security-check-{s_idx}")
                    s_status = sc.get("status")
                    if s_status in {"failed", "blocked", "pending", "not_configured", "unknown"}:
                        errors.append(
                            f"Task '{task_id}' is marked 'complete' but security check '{s_name}' is '{s_status}'."
                        )
                    elif s_status == "passed":
                        s_ev = sc.get("evidence")
                        if not s_ev or not isinstance(s_ev, str) or not s_ev.strip() or is_fake_or_dummy_evidence(s_ev):
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' without substantive evidence."
                            )

                        s_tool = sc.get("tool")
                        if not s_tool or not isinstance(s_tool, str) or not s_tool.strip():
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' without an identified tool."
                            )

                        s_tool_ver = sc.get("toolVersion")
                        if not s_tool_ver or not isinstance(s_tool_ver, str) or not s_tool_ver.strip():
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' without a specified toolVersion."
                            )

                        s_cmd = sc.get("command")
                        if not s_cmd or not isinstance(s_cmd, str) or not s_cmd.strip():
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' without an executed command."
                            )
                        elif s_cmd.strip().lower() in DUMMY_COMMANDS:
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' with dummy command '{s_cmd}'."
                            )

                        s_code = sc.get("exitCode")
                        if s_code is None or s_code != 0:
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' with non-zero or missing exit code ({s_code})."
                            )

                        s_scope = sc.get("scope")
                        if not s_scope or not isinstance(s_scope, str) or not s_scope.strip():
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' without a specified scope."
                            )

                        s_ts = sc.get("timestamp")
                        ts_valid, ts_err = is_valid_iso_timestamp(s_ts, check_future=True)
                        if not ts_valid:
                            errors.append(
                                f"Task '{task_id}' passed security check '{s_name}' timestamp is invalid: {ts_err}"
                            )
                    elif s_status == "not_applicable":
                        s_reason = sc.get("reason")
                        if not s_reason or not isinstance(s_reason, str) or not s_reason.strip():
                            errors.append(
                                f"Task '{task_id}' marked security check '{s_name}' as 'not_applicable' without an explicit reason."
                            )

            # Group F: Scope & Diff Review Invariants (for implementation / high-risk tasks)
            diff_review = rec.get("diffReview")
            if c_type in IMPLEMENTATION_TYPES or c_risk in {"medium", "high", "critical"}:
                if not diff_review or not isinstance(diff_review, dict):
                    errors.append(
                        f"Task '{task_id}' is an implementation/high-risk task but records no structured 'diffReview'."
                    )
                else:
                    dr_status = diff_review.get("status")
                    if dr_status not in {"reviewed", "passed"}:
                        errors.append(
                            f"Task '{task_id}' diffReview status is '{dr_status}' (must be 'reviewed' or 'passed')."
                        )
                    if diff_review.get("unrelatedChangesDetected") is not False:
                        errors.append(
                            f"Task '{task_id}' diffReview reports unrelatedChangesDetected is not false."
                        )
                    dr_files = diff_review.get("filesReviewed")
                    if not dr_files or not isinstance(dr_files, list) or len(dr_files) == 0:
                        errors.append(
                            f"Task '{task_id}' diffReview must record a non-empty list of 'filesReviewed'."
                        )
                    dr_id = diff_review.get("reviewId")
                    if not dr_id or not isinstance(dr_id, str) or not dr_id.strip():
                        errors.append(
                            f"Task '{task_id}' diffReview lacks a specified 'reviewId'."
                        )
                    dr_reviewer = diff_review.get("reviewer") or diff_review.get("reviewerAgent")
                    if not dr_reviewer or not isinstance(dr_reviewer, str) or not dr_reviewer.strip():
                        errors.append(
                            f"Task '{task_id}' diffReview lacks a specified 'reviewer' or 'reviewerAgent'."
                        )
                    dr_ev = diff_review.get("evidence")
                    if not dr_ev or not isinstance(dr_ev, str) or not dr_ev.strip() or is_fake_or_dummy_evidence(dr_ev):
                        errors.append(
                            f"Task '{task_id}' diffReview lacks substantive review evidence."
                        )

            # Group H: Memory & Knowledge Sync Invariants
            if c_type in ARCHITECTURAL_TYPES or c_type in {"documentation", "docs"} or c_risk in {"high", "critical"}:
                if not rec.get("memorySyncRequired"):
                    errors.append(
                        f"Task '{task_id}' impacts durable knowledge ({c_type}/{c_risk}) but memorySyncRequired is false."
                    )

            if rec.get("memorySyncRequired") and not rec.get("memorySyncCompleted"):
                errors.append(
                    f"Task '{task_id}' is marked 'complete' but required memorySyncCompleted is false."
                )

            # Group I: External Approval Invariants
            approvals = rec.get("approvalRequirements", {})
            if isinstance(approvals, dict):
                if approvals.get("required"):
                    if not approvals.get("satisfied"):
                        errors.append(
                            f"Task '{task_id}' is marked 'complete' but required approval is not satisfied."
                        )
                    if not approvals.get("approver") or not str(approvals.get("approver")).strip():
                        errors.append(
                            f"Task '{task_id}' requires approval but records no valid approver identifier."
                        )
                    app_source = approvals.get("approvalSource")
                    if not app_source or not str(app_source).strip():
                        errors.append(
                            f"Task '{task_id}' requires approval but records no valid 'approvalSource' (e.g. 'antigravity-artifact-review', 'github-pr-review')."
                        )
                    app_id = approvals.get("approvalId")
                    if not app_id or not str(app_id).strip():
                        errors.append(
                            f"Task '{task_id}' requires approval but records no valid 'approvalId'."
                        )
                    app_ts = approvals.get("approvedAt")
                    ts_valid, ts_err = is_valid_iso_timestamp(app_ts, check_future=True)
                    if not ts_valid:
                        errors.append(
                            f"Task '{task_id}' approval 'approvedAt' timestamp is invalid: {ts_err}."
                        )
                    app_ev = approvals.get("approvalEvidence")
                    if not app_ev or not str(app_ev).strip() or is_fake_or_dummy_evidence(app_ev):
                        errors.append(
                            f"Task '{task_id}' requires approval but lacks substantive, non-dummy 'approvalEvidence'."
                        )

            # Group J: Finalization & Blocker Resolution Invariants
            completed_at = rec.get("completedAt")
            ts_valid, ts_err = is_valid_iso_timestamp(completed_at, check_future=True)
            if not ts_valid:
                errors.append(
                    f"Task '{task_id}' is marked 'complete' but completedAt is invalid: {ts_err}."
                )

    # -------------------------------------------------------------------------
    # Cross-reference tasks.json: all COMPLETED tasks must have complete governance
    # -------------------------------------------------------------------------
    for t_id, task in tasks_by_id.items():
        t_status = task.get("status")
        if t_status == "COMPLETED":
            if t_id not in seen_gov_task_ids:
                errors.append(
                    f"Task '{t_id}' is COMPLETED in tasks.json but has no record in {gov_filepath}."
                )
            else:
                gov_rec = next((r for r in records if r.get("taskId") == t_id), None)
                if gov_rec and gov_rec.get("governanceStatus") != "complete":
                    errors.append(
                        f"Task '{t_id}' is COMPLETED in tasks.json but governanceStatus is '{gov_rec.get('governanceStatus')}'."
                    )
        elif t_status == "GOVERNANCE_CHECK":
            if t_id not in seen_gov_task_ids:
                errors.append(
                    f"Task '{t_id}' is in GOVERNANCE_CHECK in tasks.json but has no record in {gov_filepath}."
                )

    return errors, metrics


# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    try:
        info = resolve_workspace()
        default_gov = str(info.state_root / "governance.json")
    except Exception:
        default_gov = os.path.join(".agents", "state", "governance.json")

    gov_path = sys.argv[1] if len(sys.argv) > 1 else default_gov
    tasks_path = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.path.join(os.path.dirname(gov_path), "tasks.json")
    )

    if not os.path.exists(gov_path):
        print(f"Error: governance file not found at '{gov_path}'")
        sys.exit(1)

    # Layer 1: JSON Parsing
    try:
        with open(gov_path, "r", encoding="utf-8") as f:
            gov_data = json.load(f)
    except Exception as e:
        print(f"Layer 1 JSON Parse Error in '{gov_path}': {e}")
        sys.exit(1)

    # Merge per-task governance records if governance directory exists (per-task is canonical source of truth)
    gov_dir = os.path.join(os.path.dirname(gov_path), "governance")
    if os.path.isdir(gov_dir):
        per_task_records = {}
        for fname in sorted(os.listdir(gov_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(gov_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        rec = json.load(f)
                        if isinstance(rec, dict) and rec.get("taskId"):
                            per_task_records[rec["taskId"]] = rec
                except Exception as e:
                    print(f"Layer 1 Fatal: Failed to parse per-task governance file '{fpath}': {e}")
                    sys.exit(1)
        # Per-task records override aggregate records
        records_map = {r.get("taskId"): r for r in gov_data.get("records", []) if isinstance(r, dict) and r.get("taskId")}
        records_map.update(per_task_records)
        gov_data["records"] = list(records_map.values())

    tasks_data = {}
    if os.path.exists(tasks_path):
        try:
            with open(tasks_path, "r", encoding="utf-8") as f:
                tasks_data = json.load(f)
        except Exception as e:
            print(f"Layer 1 JSON Parse Error in tasks file '{tasks_path}': {e}")
            sys.exit(1)

    # Merge per-task tasks if tasks directory exists (per-task is canonical source of truth)
    tasks_dir = os.path.join(os.path.dirname(tasks_path), "tasks")
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
                    print(f"Layer 1 Fatal: Failed to parse per-task task file '{fpath}': {e}")
                    sys.exit(1)
        # Per-task tasks override aggregate tasks
        tasks_map = {t.get("id"): t for t in tasks_data.get("tasks", []) if isinstance(t, dict) and t.get("id")}
        tasks_map.update(per_task_tasks)
        tasks_data["tasks"] = list(tasks_map.values())

    errors, metrics = validate_governance_layers(gov_data, tasks_data, gov_path)

    if errors:
        print(f"Governance Validation FAILED ({len(errors)} errors):")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print(
            f"Governance Validation PASSED for '{gov_path}' "
            f"({metrics['records_count']} records, {metrics['gates_evaluated']} gates verified across all 5 layers)."
        )
        sys.exit(0)


if __name__ == "__main__":
    main()
