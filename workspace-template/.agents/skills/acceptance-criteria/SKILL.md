---
name: acceptance-criteria
id: SKILL-AC-001
description: Convert requirements into objective, testable acceptance conditions that can be traced to implementation and verification evidence.
---

# Acceptance Criteria Skill

<MISSION>
Convert requirements into objective, testable acceptance conditions that can be traced to implementation and verification evidence.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring acceptance-criteria capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Criteria defined with quantitative thresholds
    - [ ] Negative and edge case criteria included
    - [ ] Verification method specified for each criterion
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Every criterion must be objectively verifiable (measurable number, status code, or observable output).
    - No ambiguous terms (e.g. "fast", "user-friendly", "robust") without specific thresholds.
    - All criteria must have binary outcomes (PASSED / FAILED).
</NON_NEGOTIABLES>

<PROCEDURE>
## Quality rules

Each criterion should be:

- observable;
- specific;
- independently testable where practical;
- tied to a user/system outcome;
- unambiguous;
- realistic for the stated scope.

## Preferred structure

Use Given/When/Then for behavioral flows:

```text
Given <precondition>
When <action>
Then <observable result>
And <additional invariant>
```

For non-behavioral constraints, use measurable statements, such as response status, data invariant, accessibility property, or build/test condition.

## Coverage prompts

For every meaningful feature consider:

- happy path;
- validation failure;
- unauthorized/forbidden;
- not found;
- conflict/duplicate;
- rate limit/resource constraint;
- empty state;
- retry/recovery;
- concurrency/idempotency;
- persistence invariant;
- accessibility;
- performance requirement when explicitly required.

## Traceability

Assign stable criterion IDs when the feature is complex, for example `AC-01`, `AC-02`. Map each criterion to implementation tasks and verification evidence.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Acceptance criteria mapped 1-to-1 with verification evidence.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Measurable acceptance criteria document or section with binary pass/fail conditions.
- Traceability mapping linking acceptance criteria to implementation tasks and verification tests.
</DELIVERABLES>
