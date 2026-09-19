# Requirements Index

This directory is the canonical home for product requirements in this template.

## Files

- `PRD.md` — the current product/feature requirements document when the project has one.
- `ACCEPTANCE_CRITERIA.md` — cross-feature acceptance criteria register when a central register is useful.
- `features/` — optional feature-specific specifications for larger projects.

## Rules

- Requirements describe desired product behavior; architecture docs describe implementation structure.
- Do not hide business decisions inside technical documents.
- Mark assumptions explicitly.
- Keep acceptance criteria observable and testable.
- Link material technical decisions to ADRs.
- When requirements change after implementation begins, update affected planning, tests, architecture, and ADRs rather than letting the code silently diverge.
