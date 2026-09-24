---
name: requirements-analysis
id: SKILL-REQ-ANALYSIS-001
description: Analyze structured or unstructured requirements for completeness, contradictions, risks, boundaries, dependencies, and implementation implications.
---

# Requirements Analysis Skill

<MISSION>
Analyze structured or unstructured requirements for completeness, contradictions, risks, boundaries, dependencies, and implementation implications.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring requirements-analysis capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- For governed execution, the canonical task record `.agents/state/tasks/TASK-ID.json` must exist.
- Use the lifecycle state defined in `.agents/orchestration/task-lifecycle.md` for the current phase; do not require `IN_PROGRESS` merely because the skill is available during execution.
- Implementation-phase mutations require a `TASK_STARTED` event before code/configuration changes. Planning, requirements, analysis, review, verification, and memory-sync phases may legitimately run in their own lifecycle states.

### Pre-flight Checklist
- [ ] Requirements parsed and validated
    - [ ] Edge cases documented
    - [ ] Traceability matrix established
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Every requirement must map to measurable acceptance criteria.
    - Identify security, concurrency, and performance constraints explicitly.
    - Detect conflicting requirements and escalate before coding.
</NON_NEGOTIABLES>

<PROCEDURE>
## Analysis model

For each requirement, identify:

- actor;
- trigger;
- preconditions;
- system behavior;
- postconditions;
- data touched;
- authorization;
- failure behavior;
- observability needs;
- acceptance criteria.

## Gap analysis

Check for:

- contradictory requirements;
- missing actor permissions;
- missing empty/error/loading behavior;
- unbounded inputs or data growth;
- concurrency/race conditions;
- idempotency requirements;
- retry semantics;
- timezone/date handling;
- localization/currency assumptions;
- privacy and deletion implications;
- migration/backward compatibility;
- external dependency failure;
- abuse/rate-limit scenarios.

## Requirement maturity

Classify items as:

- ready to build;
- buildable with a recorded assumption;
- needs research;
- needs user/product decision.

## Output

Produce a traceable mapping:

```text
Requirement -> acceptance criteria -> affected module(s) -> API/data impact -> test strategy
```

Do not design the implementation in detail until the product behavior is sufficiently unambiguous.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Validated requirements specification with zero unresolved ambiguities.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Detailed requirement specifications, domain entity models, and non-functional requirements catalog.
</DELIVERABLES>
