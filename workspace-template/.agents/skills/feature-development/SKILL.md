---
name: feature-development
description: Deliver a feature end-to-end using project memory, architecture, focused implementation, impact-aware testing, verification, and memory synchronization.
---

# Feature Development Skill

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
