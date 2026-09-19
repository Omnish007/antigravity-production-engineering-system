---
name: project-memory
description: Detect durable knowledge from completed work and synchronize project context, architecture, conventions, ADRs, current state, and execution state.
---

# Project Memory Skill

## Mission

A future AI chat must be able to understand the important outcomes of this task without access to today's conversation.

## Read

Start with:

- `docs/INDEX.md`;
- `docs/CURRENT_STATE.md`;
- relevant `docs/ARCHITECTURE.md`, `docs/CONVENTIONS.md`, and ADRs.

## Detect

Look for:

- new architecture;
- new reusable convention;
- changed API/data contract;
- chosen library/service/provider;
- security control or workaround;
- important migration choice;
- current milestone/blocker change.

## Write

- context change -> `PROJECT_CONTEXT.md`;
- architecture change -> `ARCHITECTURE.md`;
- reusable rule -> `CONVENTIONS.md`;
- durable trade-off -> new ADR;
- current progress -> `CURRENT_STATE.md`;
- tracked execution -> `.agents/state/`.

## ADR rules

Never erase decision history. Supersede old decisions explicitly. Link the new ADR to the old one and update the ADR index.

## Quality test

Read the resulting docs as if you were a new engineer joining the project tomorrow. The documents should explain what is true, why important choices were made, and what state remains.
