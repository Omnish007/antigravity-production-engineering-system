# Project Memory Rules

Recommended activation: **Always On**

## Purpose

Make the repository remember important decisions and project knowledge across independent AI chats.

## Read before meaningful work

Start with:

- `docs/INDEX.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/CURRENT_STATE.md`

Then load:

- `docs/ARCHITECTURE.md` for structural changes;
- `docs/CONVENTIONS.md` for reusable implementation patterns;
- only the relevant ADRs from `docs/decisions/`.

## Classify new knowledge after work

### Do not store

- one-off debugging observations that are no longer relevant;
- trivial formatting changes;
- temporary implementation details;
- facts already represented accurately by source code and unlikely to help future reasoning.

### Store in `CONVENTIONS.md`

When a project adopts a repeatable implementation practice used by multiple features or expected for future work.

### Store in `ARCHITECTURE.md`

When the system structure, boundaries, data flow, runtime topology, or integration pattern changes.

### Store as an ADR

When a deliberate choice has meaningful trade-offs or durable consequences. Examples include:

- authentication/session architecture;
- API versioning;
- endpoint-definition strategy;
- database modeling strategy;
- state management architecture;
- caching approach;
- background-job system;
- storage provider;
- major dependency choice;
- security control with architectural consequences.

### Store in `CURRENT_STATE.md`

When completion, current work, blockers, next steps, or known risks change.

## ADR discipline

Never overwrite an accepted ADR to hide history. If the decision changes:

1. mark the previous ADR `Superseded`;
2. create a new ADR with the new decision;
3. link the two records;
4. update `docs/decisions/INDEX.md`;
5. update architecture/conventions if needed.

## End-of-task memory sync

Every meaningful feature, bug fix, refactor, architectural change, planning milestone, or release task must perform a memory review before completion.

The review asks:

- What changed permanently?
- Did we make a reusable convention?
- Did we make a deliberate decision?
- Did architecture change?
- Did current project state change?
- Are any old docs now inaccurate?

Never leave a significant project decision only in chat history.
