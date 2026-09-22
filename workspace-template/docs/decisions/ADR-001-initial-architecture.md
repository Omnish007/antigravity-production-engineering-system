# ADR-001: Initial Architecture & Framework Selection

## Status
Accepted

## Date
2026-09-01

## Context
The repository requires a structured, multi-stack engineering governance and execution architecture with clear separation of concerns, progressive disclosure of skills, and fail-closed quality gates.

## Decision
1. Establish Antigravity Native Runtime (Planning, Tasks, Artifacts, Permissions, Sandboxing) as the primary execution authority.
2. Structure project memory under `docs/` with ADR-driven architectural decisions.
3. Organize skills under `.agents/skills/` and rules under `.agents/rules/`.
4. Enforce automated governance validation via `validate-governance.py`.

## Consequences
- Positive: High predictability, clear compliance auditability, fail-closed verification.
- Trade-off: Requires maintaining machine-readable state and adherence to the 3-lane execution model.
