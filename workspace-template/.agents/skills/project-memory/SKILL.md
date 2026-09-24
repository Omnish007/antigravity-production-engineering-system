---
name: project-memory
id: SKILL-MEM-001
description: Detect durable knowledge from completed work and synchronize project context, architecture, conventions, ADRs, current state, and execution state.
---

# Project Memory Skill

<MISSION>
Detect durable knowledge from completed work and synchronize project context, architecture, conventions, ADRs, current state, and execution state.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring project-memory capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- For governed execution, the canonical task record `.agents/state/tasks/TASK-ID.json` must exist.
- Use the lifecycle state defined in `.agents/orchestration/task-lifecycle.md` for the current phase; do not require `IN_PROGRESS` merely because the skill is available during execution.
- Implementation-phase mutations require a `TASK_STARTED` event before code/configuration changes. Planning, requirements, analysis, review, verification, and memory-sync phases may legitimately run in their own lifecycle states.

### Pre-flight Checklist
- [ ] docs/ updated with actual execution facts
    - [ ] ADR recorded if Type 1 decision or architectural trade-off was made
    - [ ] No speculative documentation added
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Synchronize durable facts in docs/ (ARCHITECTURE.md, PROJECT_CONTEXT.md, CURRENT_STATE.md).
    - Never leave architecture decisions or conventions in ephemeral chat history.
    - Update docs only when actual execution changes a documented fact.
    - If a Type 1 decision or architectural pattern was introduced, an ADR MUST exist in `docs/decisions/` and be indexed in `docs/decisions/INDEX.md`.
</NON_NEGOTIABLES>

<PROCEDURE>
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
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Repository memory synchronized with verified codebase state.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Synchronized docs/ artifacts, updated ADRs, conventions, and current state reflections.
</DELIVERABLES>
