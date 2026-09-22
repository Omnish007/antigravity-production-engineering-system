# Antigravity Production Engineering System — Version Specification

- **System Version**: `4.0.0`
- **Release Status**: `PRODUCTION_CERTIFIED` (100% Pass Across Final Master Certification Matrix)
- **Freeze Date**: `2026-09-22`
- **Specification**: Final Master Audit & Architecture Freeze Specification (Audit 5 Compliant)

---

## 1. System Identity & Architecture

The **Antigravity Multi-Stack Production Engineering System** operates as a fully governed, deterministic, stateful development framework built atop the Google Antigravity 2.0 Native Runtime.

```text
Antigravity Native Runtime
        │
        ├── Permissions (Interactive Terminal Sandboxing)
        ├── Planning / Task Groups (Native Implementation Plans)
        ├── Artifacts / Review (walkthrough.md, implementation_plan.md)
        └── Hooks (PreToolUse, PostToolUse, Stop)
                │
                ▼
        Custom Agent Layer (Least-Privilege Roles & Bindings)
                │
        ┌───────┼────────┐
        ▼       ▼        ▼
      Rules   Skills   Technology Profiles
        │       │        │
        └───────┼────────┘
                ▼
      Canonical State Layer (.agents/state/tasks/, governance/, events/, blockers/)
                │
                ▼
      Authoritative Verification Engine (.agents/validation/core/)
        ├── workspace_resolver.py (Deterministic root discovery)
        ├── verification_policy.py (16 canonical task types, dynamic gate registry)
        └── governance_core.py (Task-scoped stop evaluation, monotonic event sequences)
```

## 2. Canonical Freeze Inventory

1. **State Architecture (P0-04, P0-06, P1-01, P1-03, P1-05, P1-06)**:
   - Sole Canonical State: `.agents/state/tasks/*.json`, `.agents/state/governance/*.json`, `.agents/state/events/*.jsonl`, `.agents/state/blockers/*.json`.
   - Strict Schemas: `task-record.schema.json`, `governance-record.schema.json`, `blocker-record.schema.json`, `event.schema.json` with `additionalProperties: false`.
   - Derived Aggregates: Rebuilt from scratch via `aggregate-state.py` using atomic writes (`tempfile` + `fsync` + `os.replace`).
   - Drift Detection & Reconciliation: `reconcile-state.py` supporting `--check` (SHA-256 full content comparison) and `--fix` (non-destructive rebuild).

2. **Governance & Stop Hook (P0-01, P0-02, P0-03, P0-08, P0-09, P0-25, P0-26)**:
   - Shared Authoritative Evaluator: `.agents/validation/core/governance_core.py`.
   - Task-Scoped Stop Evaluation: Scoped strictly to the active task without cross-task interference or fallback to unrelated tasks.
   - Strict `fullyIdle` Requirement: Requires boolean `True`; rejects missing, string `"true"`, `None`, and `False`.
   - Dynamic Gate Evaluation: Derived from `verification_policy.py` across 16 canonical types; rejects `not_configured` and enforces substantive evidence for `not_applicable`.
   - Lifecycle Invariants: Enforces monotonic sequence numbers and `TASK_STARTED` < `TASK_COMPLETED`.

3. **Security & Boundary Enforcement (P0-14, P0-15, P0-17, P0-18, P0-19, P0-20, P1-34)**:
   - PreToolUse Hook: `hook-pre-tool.py` enforcing realpath canonicalization, path traversal containment (`rel_path.startswith("..")` hard deny), and protection of control-plane files (`.agents/**`, `AGENTS.md`, `.github/**`, `.env`).
   - Covered Mutations: Intercepts `run_command`, `write_to_file`, `replace_file_content`, and `multi_replace_file_content`.
   - PostToolUse Hook: `hook-post-tool.py` writing to per-task streams with regex-based credential and secret redaction.
   - Control-Plane Integrity: `validate-control-plane.py` verifying CODEOWNERS coverage and cryptographic checksums in `CONTROL_PLANE_MANIFEST.json`.

4. **Rules, Skills & Agents (P1-19, P1-20, P1-21, P1-22)**:
   - 15 Rules (`RULE-CORE-001` through `RULE-OBS-001`) with declarative activation matrix.
   - 28 Skills mechanically validated via `validate-skills.py` with PyYAML and standard section requirements (`MISSION`, `WHEN_TO_USE`, `PRECONDITIONS`, `NON_NEGOTIABLES`, `PROCEDURE`).
   - 9 Agent definitions validated via `validate-agents.py` with dynamic tool registry loading from `antigravity-tool-registry.json`.

5. **Technology Catalog (P1-36, P1-37, P1-38)**:
   - 30 Profiles with multi-tier version specifications (`preferredVersion`, `supportedVersions`, `legacyVersions`, `prohibitedVersions`).
   - Enforced freshness dates (`lastVerified`, `reviewAfter`) and official source citations validated via `validate-technology-profiles.py`.

6. **Execution Lanes & Policy Registry (P1-14, P1-15, P1-16, P1-17)**:
   - Machine-readable `lane-policy.yaml` governing Lane A (Fast Low-Risk Governed Mutation), Lane B (Standard), and Lane C (High Assurance).
   - Deterministic context merge precedence: `REQUIRED > RECOMMENDED > OPTIONAL > DEFERRED > EXCLUDED`.

7. **Validation & Testing Matrix**:
   - 12/12 Validator Test Fixtures (`test-validators.py`).
   - 16/16 Full Lifecycle Simulation Tests (`test-lifecycle-simulation.py`).
