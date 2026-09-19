---
name: documentation
description: Maintain durable technical documentation, API docs, project context, conventions, and ADRs without duplicating source-of-truth information.
---

# Documentation Skill

## Documentation hierarchy

- `PROJECT_CONTEXT.md`: what/why/who/constraints.
- `ARCHITECTURE.md`: how the system is structured.
- `CONVENTIONS.md`: how this project consistently works.
- `CURRENT_STATE.md`: where the project is now.
- `decisions/ADR-*.md`: why important decisions were made.

## Principles

- Document decisions and invariants, not every line of code.
- Prefer links to canonical implementation files.
- Keep docs updated in the same task when behavior materially changes.
- Mark deprecated/superseded material explicitly.
- Avoid contradictory duplicate documentation.

## ADRs

Use the ADR template. Include context, decision, alternatives, rationale, consequences, implementation impact, and links.

## Verification

Documentation changes should be checked for broken paths, stale commands, and contradiction with source/configuration.
