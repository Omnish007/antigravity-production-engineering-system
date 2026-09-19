---
name: documentation
description: Maintain durable technical documentation, API docs, project context, conventions, and ADRs without duplicating source-of-truth information.
---

# Documentation Skill

## Documentation hierarchy

- `docs/INDEX.md`: entry point and navigation map for all project knowledge.
- `docs/PROJECT_CONTEXT.md`: what/why/who/constraints.
- `docs/ARCHITECTURE.md`: how the system is structured.
- `docs/CONVENTIONS.md`: how this project consistently works.
- `docs/CURRENT_STATE.md`: where the project is now.
- `docs/REFERENCES.md`: version-sensitive external documentation used by the project.
- `docs/decisions/INDEX.md`: index of architectural and technical decisions.
- `docs/decisions/ADR-*.md`: individual decision records.
- `docs/requirements/`: product requirements, acceptance criteria, feature specs.

## Principles

- Document decisions, invariants, and non-obvious constraints — not every line of code.
- Prefer links to canonical implementation files over copying code into docs.
- Keep docs updated in the same task when behavior materially changes.
- Mark deprecated/superseded material explicitly; do not silently delete history.
- Avoid contradictory duplicate documentation; use one canonical source and link to it.
- Write for the future reader who has no context; include the "why," not just the "what."
- Use specific, concrete language; avoid vague statements that cannot be acted upon.

## Writing quality

- Use consistent heading levels and formatting.
- Write actionable instructions, not aspirational goals.
- Use tables for structured information with multiple dimensions.
- Include examples where they clarify abstract concepts.
- Keep documents focused; split into separate files when a document exceeds its scope.

## ADRs

Use the ADR template (`.agents/templates/adr-template.md`). Include:

- context and problem statement;
- decision and alternatives considered;
- rationale with trade-offs and evidence;
- consequences (positive, negative, operational, migration);
- implementation impact and verification;
- links to related ADRs, requirements, and architecture docs.

Never renumber, reuse, or silently rewrite an ADR. Supersede with a new ADR and link the successor.

## API documentation

- Document externally visible contracts using the API template.
- Include authentication, authorization, validation, error responses, and rate limits.
- Keep API documentation synchronized with implementation.
- Use OpenAPI/Swagger specs when the project adopts them.

## Verification

Documentation changes should be checked for:

- broken file paths and links;
- stale commands or version-specific instructions;
- contradiction with source code, configuration, or other docs;
- completeness of cross-references (new files added to indexes, manifests);
- accuracy of examples and code snippets.

## Integration

- Update `docs/INDEX.md` when adding new documentation files.
- Update `FILE_MANIFEST.md` when adding new system files.
- Trigger memory sync (`.agents/skills/project-memory/SKILL.md`) when durable knowledge changes.
- Reference the verification template when producing formal reports.
