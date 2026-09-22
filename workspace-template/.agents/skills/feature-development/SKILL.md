---
name: feature-development
id: SKILL-FEATURE-001
description: Deliver a feature end-to-end using project memory, architecture, focused implementation, impact-aware testing, verification, and memory synchronization.
---

# Feature Development Skill

<MISSION>
Deliver a feature end-to-end using project memory, architecture, focused implementation, impact-aware testing, verification, and memory synchronization.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring feature-development capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Acceptance criteria defined and agreed
- [ ] Architectural boundaries and layer separation identified from docs/ARCHITECTURE.md
- [ ] Project context, conventions, and existing ADRs reviewed
- [ ] Task scope and expected outputs explicitly defined in tasks.json
- [ ] Dependencies and test harness operational
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Map all feature requirements to explicit acceptance criteria before coding.
- Respect established project architectural boundaries and layer separation as defined in docs/ARCHITECTURE.md; do not force an unchosen architectural style.
- All new features must include unit and integration tests.
- If the feature introduces Type 1 architectural decisions, evaluates competing trade-offs, or crosses the 5 architectural planes, author an ADR in `docs/decisions/` before writing code.
</NON_NEGOTIABLES>

<PROCEDURE>
## Lifecycle

```text
Understand -> Plan -> Implement -> Test -> Verify -> Review -> Memory Sync
```

## Understand

- Read project context, current state, architecture, conventions, and relevant ADRs.
- Identify acceptance criteria and trust boundaries.
- Search for existing abstractions before creating new ones.

## Plan

For localized low-risk work, use a compact plan. For cross-layer or high-risk work, use the full planning skill and task graph.

## Implement

Respect layer boundaries:

- UI handles presentation and interaction.
- API handlers handle transport and authorization boundaries.
- Services/use cases own business behavior.
- Repositories/data access own persistence concerns.
- Validation occurs at external boundaries and is reused where appropriate.

## Test

Add tests for new logic, error paths, authorization, data invariants, and critical user behavior according to risk.

## Verify

Run focused checks first, then broader checks required by the change. Review the final diff.

## Memory sync

Determine whether the feature introduced:

- a durable decision;
- a reusable convention;
- an architecture change;
- a changed current state.

Update the appropriate files before completion.

## Output

Report changed files, verification evidence, known limitations, and memory updates.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Feature implemented, fully tested, and verified against acceptance criteria.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Complete feature implementation adhering to architectural boundaries.
- Passing acceptance criteria, verification tests, and updated project state.
</DELIVERABLES>
