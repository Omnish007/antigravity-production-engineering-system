# Project Agent Entry Point

This repository uses `.agents/` for agent rules, skills, orchestration, state, and templates, and `docs/` for durable project memory.

## Critical commands

```bash
# Install dependencies
npm ci

# Format check
npm run format:check

# Lint
npm run lint

# Type check
npm run typecheck

# Run tests
npm test

# Build
npm run build
```

Adapt these commands to match the project's actual `package.json` scripts.

## Boundaries — do not modify without explicit task scope

- `.agents/rules/` — system rules, not application code
- `.agents/orchestration/` — system policies
- `.agents/state/` — modify only with actual execution facts
- `docs/decisions/` — never overwrite; supersede with new ADRs

## Before meaningful work

Read:

1. `docs/INDEX.md`
2. `docs/PROJECT_CONTEXT.md`
3. `docs/CURRENT_STATE.md`
4. `.agents/rules/00-core.md`
5. `.agents/rules/13-agent-safety.md`
6. `.agents/rules/11-project-memory.md`
7. the relevant project rules and skills for the task

Read `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, and only the relevant ADRs whenever they affect the task.

Use `.agents/orchestration/context-router.md` and `.agents/orchestration/context-budget-policy.md` to load the minimum sufficient context without wasting the context budget.

## Version-matched documentation

When making framework-specific changes, use the documentation bundled with the installed packages when available, for example:

```text
node_modules/next/dist/docs/
```

Prefer version-matched installed documentation over stale model knowledge.

## Stack

This system is stack-agnostic. The default baseline is documented in `.agents/rules/02-tech-stack.md`. The actual project stack is recorded in `docs/PROJECT_CONTEXT.md`. Adapt skill procedures to the project's chosen technologies.

## Completion

Before declaring completion:

- verify acceptance criteria;
- run appropriate checks (format, lint, type-check, test, build);
- review the diff;
- evaluate quality gates (`.agents/skills/quality-gates/SKILL.md`);
- synchronize durable project memory when needed;
- update `.agents/state/` when tracked execution state changed.

The repository is the source of truth; chat history is temporary context.

## Cross-tool compatibility

This system works with any AI coding agent that reads repository instructions:

- **Gemini / Antigravity**: reads `AGENTS.md` and `.agents/` natively
- **Cursor**: symlink or copy relevant content to `.cursor/rules/`
- **Claude Code**: symlink `ln -s AGENTS.md CLAUDE.md`
- **GitHub Copilot**: symlink or reference in `.github/copilot-instructions.md`
- **Other agents**: most tools read `AGENTS.md` at the repository root

The detailed rules, skills, and orchestration under `.agents/` provide depth; this file provides the essential entry point.
