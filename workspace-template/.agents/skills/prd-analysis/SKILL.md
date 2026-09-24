---
name: prd-analysis
id: SKILL-PRD-001
description: Analyze an existing PRD and transform it into an implementation-ready specification with risks, gaps, dependencies, and acceptance criteria.
---

# PRD Analysis Skill

<MISSION>
Analyze an existing PRD and transform it into an implementation-ready specification with risks, gaps, dependencies, and acceptance criteria.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring prd-analysis capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- For governed execution, the canonical task record `.agents/state/tasks/TASK-ID.json` must exist.
- Use the lifecycle state defined in `.agents/orchestration/task-lifecycle.md` for the current phase; do not require `IN_PROGRESS` merely because the skill is available during execution.
- Implementation-phase mutations require a `TASK_STARTED` event before code/configuration changes. Planning, requirements, analysis, review, verification, and memory-sync phases may legitimately run in their own lifecycle states.

### Pre-flight Checklist
- [ ] Functional requirements cataloged
    - [ ] Non-functional constraints identified
    - [ ] Ambiguities resolved
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Extract every functional, non-functional, security, and performance requirement.
    - Identify underspecified requirements and resolve ambiguity before implementation.
    - Translate requirements into unambiguous acceptance criteria.
</NON_NEGOTIABLES>

<PROCEDURE>
## Phase 1 — Extract intent

Identify:

- product objective;
- target users;
- problem statement;
- success measures;
- scope;
- out-of-scope items;
- user journeys;
- functional requirements;
- non-functional requirements;
- constraints;
- dependencies;
- integrations.

## Phase 2 — Challenge the document

Look for:

- contradictions;
- ambiguous terminology;
- missing permissions;
- missing failure behavior;
- implicit business rules;
- unbounded inputs/storage;
- unclear lifecycle/retention;
- missing auditability;
- missing observability;
- untestable success criteria;
- unsupported performance claims;
- security assumptions that exist only in the UI.

## Phase 3 — Translate to engineering impact

Map requirements to:

- frontend surfaces;
- API endpoints;
- data models;
- authorization boundaries;
- background work;
- external integrations;
- tests;
- migrations;
- operational controls.

## Phase 4 — Produce implementation inputs

Create:

- requirement traceability table;
- acceptance criteria;
- architecture-impact summary;
- data-impact summary;
- API-impact summary;
- risks and open decisions;
- dependency list;
- phased implementation plan.

## Output integrity

Do not silently "fix" the product specification. Mark inferred behavior as assumptions. High-impact business questions remain open until explicitly resolved.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Complete requirements specification ready for task decomposition.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Decomposed PRD requirements, identified ambiguities, and edge cases.
- Structured requirement specifications ready for task decomposition.
</DELIVERABLES>
