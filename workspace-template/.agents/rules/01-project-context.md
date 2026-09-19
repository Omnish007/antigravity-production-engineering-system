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
- relevant files under `docs/decisions/`

Use `.agents/orchestration/context-router.md` to avoid loading unrelated material.

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

If a required project fact is unknown but can be safely researched from the repository, research it. If it is a business decision or high-impact ambiguity that cannot be inferred, request the missing decision rather than inventing it.
