# Project Knowledge Index

This file is the first documentation entry point for every AI chat.

## Start here

1. `PROJECT_CONTEXT.md` — what the project is and why it exists.
2. `CURRENT_STATE.md` — where the project stands now.
3. `ARCHITECTURE.md` — how the system is structured.
4. `CONVENTIONS.md` — how this project consistently works.
5. `decisions/INDEX.md` — important decisions and their status.
6. `REFERENCES.md` — version-sensitive external documentation used by this project.

## Requirements

The canonical location is `docs/requirements/`. Start with `docs/requirements/PRD.md` and `docs/requirements/ACCEPTANCE_CRITERIA.md`; feature-specific files may live under `docs/requirements/features/` for larger projects. The reusable authoring templates live in `.agents/templates/`.

## Source-of-truth rule

The repository is durable project memory. Chat history is transient.

## Update rule

When a task changes a documented fact, update the appropriate canonical document in the same task. Do not maintain duplicate descriptions in several documents unless one explicitly links to the other as the canonical source.
