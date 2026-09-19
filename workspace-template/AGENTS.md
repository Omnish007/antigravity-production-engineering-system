# Project Agent Entry Point

This repository uses `.agents/` for agent rules, skills, orchestration, state, and templates, and `docs/` for durable project memory.

## Before meaningful work

Read:

1. `docs/INDEX.md`
2. `docs/PROJECT_CONTEXT.md`
3. `docs/CURRENT_STATE.md`
4. `.agents/rules/00-core.md`
5. `.agents/rules/11-project-memory.md`
6. the relevant project rules and skills for the task

Read `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, and only the relevant ADRs whenever they affect the task.

## Next.js version-matched documentation

When making Next.js changes, use the documentation bundled with the installed `next` package when available, for example:

```text
node_modules/next/dist/docs/
```

Prefer version-matched installed documentation over stale model knowledge. Next.js documents this pattern specifically for AI coding agents.

## Completion

Before declaring completion:

- verify acceptance criteria;
- run appropriate checks;
- review the diff;
- synchronize durable project memory when needed;
- update `.agents/state/` when tracked execution state changed.

The repository is the source of truth; chat history is temporary context.
