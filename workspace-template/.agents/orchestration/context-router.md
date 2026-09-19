# Context Router

## Purpose

Load enough context to make a correct decision without flooding the agent with unrelated documents.

## Baseline context

For every meaningful task, read:

- `AGENTS.md` when present;
- `docs/INDEX.md`;
- `docs/PROJECT_CONTEXT.md`;
- `docs/CURRENT_STATE.md`;
- `.agents/rules/00-core.md`;
- `.agents/rules/11-project-memory.md`;
- `.agents/rules/12-requirements.md` when requirements are being interpreted.

Then add task-specific context.

## Context by task

### Requirements / PRD

- project context;
- current state;
- requirements rule;
- relevant PRD/requirements files;
- architecture when translating to implementation.

### Frontend

- Next/React rule;
- coding/naming;
- UI/UX;
- architecture;
- relevant feature conventions;
- affected source files;
- relevant ADRs.

### Backend/API

- coding/naming;
- architecture;
- security;
- API/backend skill;
- affected source files;
- relevant API/auth ADRs.

### Database

- architecture;
- database skill;
- backend rule;
- security where sensitive;
- affected schema/index/query files;
- relevant data-model ADRs.

### Bug fix

- current state;
- debugging + bug-fix + testing + verification;
- affected domain rules;
- relevant ADRs;
- failing test/log evidence.

### Deployment

- tech stack;
- security;
- deployment;
- verification;
- environment/configuration docs;
- current state.

### Performance

- performance skill;
- frontend/backend/database skill depending on scope;
- architecture;
- affected source files;
- relevant ADRs;
- current performance baselines if documented.

### Refactoring

- refactoring skill;
- architecture;
- coding/naming;
- testing;
- affected source files;
- relevant ADRs;
- existing test coverage for affected modules.

### Infrastructure

- deployment skill;
- security;
- tech stack;
- environment configuration;
- CI/CD configuration files;
- current state.

### Migration

- database skill;
- backend skill;
- security;
- architecture;
- affected schema/migration files;
- relevant data-model ADRs;
- current state.

## Routing principles

1. Never assume every skill is relevant.
2. Read indexes first; open full documents only when needed.
3. Prefer affected source/config files over broad source dumps.
4. When a task crosses layers, combine their context groups.
5. When an accepted decision is relevant, read the exact ADR rather than guessing from its title.
6. When version behavior matters, read installed package documentation before implementation.
7. Respect the context budget policy (`.agents/orchestration/context-budget-policy.md`): load invariant rules first, volatile data last.
8. Monitor context consumption; if the session becomes heavily loaded, decompose into sub-tasks.

## Do not load

Unless specifically investigating them:

- lockfiles (`package-lock.json`, `yarn.lock`);
- generated code and build artifacts;
- `node_modules/` contents (except version-matched framework docs);
- large binary or media files;
- unrelated test fixtures and sample data;
- files clearly outside the affected scope.
