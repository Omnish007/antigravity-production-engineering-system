# Changelog

All notable changes to the **Antigravity Multi-Stack Production Engineering System** are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [4.0.0] - 2026-09-22 — Final Architecture Freeze & Master Audit (Production Certified)

### Added
- **Authoritative Core Engine (`.agents/validation/core/`)**:
  - `workspace_resolver.py`: Deterministic resolver discovering project, governance, and state roots with sentinel `.agents/state/project.json` check (`governanceMode == "managed"`) without hardcoded template fallbacks (P0-30, P0-31, P0-32).
  - `verification_policy.py`: Executable verification policy with 16 canonical task types, alias resolution, structured Gate Registry kinds (test, lint, etc.), `not_configured` rejection (P0-26), and required applicability evidence for `not_applicable` (P0-25, P0-27).
  - `governance_core.py`: Authoritative evaluator enforcing task-scoped stop evaluation (P0-02), strict `fullyIdle == True` (P0-03), event schema/monotonic sequences/`TASK_STARTED` < `TASK_COMPLETED` (P0-08, P0-09), scoped blocker isolation (P0-35, P0-36, P0-37), and external approval evidence (P0-22).
- **Control-Plane Integrity & Protection**:
  - `validate-control-plane.py`: Mechanical validator verifying integrity of hooks, rules, skills, agents, schemas, validators, and workflows against SHA-256 checksums in `CONTROL_PLANE_MANIFEST.json` and verifying `.github/CODEOWNERS` protection (P1-34).
  - `workspace-template/.github/CODEOWNERS`: Formal code ownership protecting control-plane files (`.agents/**`, `.github/**`, `AGENTS.md`) (P0-15).
  - `hook-pre-tool.py`: Enforces path canonicalization (`realpath`), path traversal containment (`rel_path.startswith("..")` hard deny), and control-plane mutation protection (P0-14, P0-17, P0-18, P0-19).
- **Mechanical Skill & Agent Validation**:
  - `validate-skills.py`: Mechanical Skill validator parsing SKILL.md with PyYAML, enforcing required tags (`MISSION`, `WHEN_TO_USE`, `PRECONDITIONS`, `NON_NEGOTIABLES`, `PROCEDURE`), unique IDs, and naming parity (P1-19, P1-20).
  - `antigravity-tool-registry.json`: Versioned tool registry categorizing native Antigravity tools by access, category, risk, and supported agent types (P1-21).
  - `validate-agents.py`: Updated with PyYAML parsing, dynamic tool registry lookup, and skill-to-agent binding validation (P1-20, P1-21, P1-22).
- **State Reconciliation & Hashing**:
  - `reconcile-state.py`: Enhanced with normalized canonical JSON SHA-256 hashing, exact field diffing, event stream parity verification, `--check` drift detection, and `--fix` non-destructive atomic rebuilding (P1-03, P1-05, P1-06).
  - `aggregate-state.py`: Authoritative scratch aggregator with atomic file writing (`tempfile` + `fsync` + `os.replace`) (P0-06, P1-03, P1-04).
- **Policy & Documentation Consistency**:
  - `lint-policy-consistency.py`: Automated semantic linter detecting obsolete phrases (e.g. "15 completion criteria", "5 quality gates", "14-phase lifecycle", "tasks.json is canonical") (P1-35).
  - `COMPATIBILITY.md`: Comprehensive platform, runtime, toolchain, schema, and standards compatibility specification (P1-67).
  - `lane-policy.yaml`: Machine-readable execution lane policy defining Lane A (Fast Low-Risk Governed Mutation), Lane B (Standard), and Lane C (High Assurance) (P1-14, P1-15).
- **Strict Canonical Schemas**:
  - Created `task-record.schema.json`, `governance-record.schema.json`, `blocker-record.schema.json`, and `event.schema.json` with strict `additionalProperties: false` (P0-38, P1-01).

### Changed
- **Stop Hook Semantics**: Rewrote `hook-stop.py` and `completion_gate.py` to delegate to `governance_core.py`, eliminating cross-task contamination and strictly evaluating active task scope (P0-02).
- **Recovery Invariants**: Rewrote `recover-task.py` to use canonical state only, enforce state machine transitions (terminal `COMPLETED`/`CANCELLED` are immutable), fail closed on git errors, and emit schematized recovery events (P0-10, P0-11, P0-12, P0-13).
- **Post-Tool Secret Redaction**: Rewrote `hook-post-tool.py` to write events to per-task streams (`events/TASK-xxx.jsonl`), treat tool executions as telemetry, and scrub bearer tokens, API keys, credentials, and passwords from paths, errors, and commands (P0-07, P0-20, P0-21).
- **Technology Profile Standards**: Enriched all 30 profiles with `lastVerified`, `reviewAfter`, `sources`, and multi-tier version specifications (`preferredVersion`, `supportedVersions`, `legacyVersions`, `prohibitedVersions`), enforced by `validate-technology-profiles.py` (P1-36, P1-37, P1-38).
- **External Standards Alignments**: Updated `RESEARCH_BASIS.md` to distinguish OWASP Top 10 for Agentic Applications (2026), OWASP Top 10 for LLM Applications (2025), and OWASP Agent Control Standard (September 2026), replacing claims of "compliance" with "aligned with" and "informed by" (P1-68, P1-69, P1-70).
- **Manifest Automation**: Enhanced `generate-manifest.py` with root-aware discovery (`--root`) and automated 100% parity verification (P1-63, P1-64).

---

## [3.0.0] - 2026-08-15

### Added
- Adaptive 3-Lane Execution Model (Lane A: Fast, Lane B: Standard, Lane C: High Assurance).
- Formal JSON Schema validation (Draft 2020-12) across all state files.
- Supply chain security enforcement with pinned 40-character commit SHAs in GitHub Actions workflows.
- Instruction tag standard and automated validator (`validate-instruction-tags.py`).

### Changed
- Refactored task lifecycle to execution activities mapped to persisted states.
- Enhanced context router with four-tier progressive disclosure (`REQUIRED`, `RECOMMENDED`, `OPTIONAL`, `EXCLUDED`).

---

## [2.0.0] - 2026-05-10

### Added
- Native Google Antigravity 2.0 integration (Planning Mode, Task Groups, Artifacts, Permissions, Terminal Sandboxing).
- 5-Layer semantic governance validation (`validate-governance.py`).
- 7-Point security evidence standard for SAST and dependency audits.
- Project memory synchronization framework (`docs/INDEX.md`, `docs/CURRENT_STATE.md`, `docs/CONVENTIONS.md`).

---

## [1.0.0] - 2026-01-20

### Added
- Initial release of baseline multi-stack engineering rules, skills, and templates.
