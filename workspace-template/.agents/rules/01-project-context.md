# Project Context Rules

Recommended activation: **Always On**

## Purpose

Ensure every new chat can reconstruct the project's intent and present state from repository files.

## Required context

At the start of meaningful work, consult:

- `docs/INDEX.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/CURRENT_STATE.md`
- `docs/ARCHITECTURE.md` when structural behavior is relevant
- `docs/CONVENTIONS.md` when implementation conventions are relevant
- `docs/REFERENCES.md` when version-sensitive behavior matters
- `docs/requirements/` when requirements, acceptance criteria, or PRD affect the task
- relevant files under `docs/decisions/`

Use `.agents/orchestration/context-router.md` to load only what the task requires.
Use `.agents/orchestration/context-budget-policy.md` to manage context window capacity.

## Context priority

Treat as authoritative in this order:

1. Current safety/platform requirements.
2. Current explicit user request.
3. Accepted/superseding ADRs.
4. Project architecture and conventions.
5. Existing code pattern when not contradicted.
6. Installed-version vendor documentation.
7. General best practice.

## Stale or conflicting context

If documentation contradicts code:

1. Determine whether code is intentionally ahead of documentation.
2. Inspect recent history when available.
3. Prefer the latest accepted decision and current source of truth.
4. Repair stale documentation as part of the task if the change is meaningful.
5. Never silently choose a new architecture solely to resolve a documentation mismatch.

## Missing context

If a required project fact is unknown:

1. **Can it be researched from the repository?** → Research it (check source, config, history).
2. **Can it be inferred from existing patterns with high confidence?** → Infer it and document the inference.
3. **Is it a business decision, high-impact ambiguity, or architectural choice?** → Request the missing decision rather than inventing it.
4. **Is it a technical implementation detail with low risk?** → Choose the option most consistent with existing conventions and document the choice.

When context is missing and the decision matters, always prefer asking over guessing.

## Context freshness

Project memory can become stale. When documentation and code diverge:

- verify the actual state by reading source code and configuration;
- treat recent Git history as evidence of intent;
- update stale documentation as part of the current task when the fix is straightforward;
- create a separate task for large documentation repairs.
