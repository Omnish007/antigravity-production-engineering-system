---
name: verification
id: SKILL-VERIFY-001
description: Create objective verification evidence mapping acceptance criteria to commands, tests, outputs, changed files, and known limitations.
---

# Verification Skill

<MISSION>
Create objective verification evidence mapping acceptance criteria to commands, tests, outputs, changed files, and known limitations.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring verification capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task record `.agents/state/tasks/TASK-ID.json` must be `IN_PROGRESS`.
    - A `TASK_STARTED` event must be recorded in `.agents/state/events/TASK-ID.jsonl`.

### Pre-flight Checklist
- [ ] Canonical verification commands executed
    - [ ] Exit codes recorded (all 0)
    - [ ] Acceptance criteria mapped to proof
    - [ ] ADR in docs/decisions/ verified if Type 1 choices or architectural trade-offs made
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Provide objective command execution evidence with exit codes for every check.
- Code inspection is never a substitute for runtime execution.
- Every acceptance criterion must be marked PASSED with proof.
- If the task made a Type 1 decision or evaluated architectural trade-offs, verify that an ADR exists in docs/decisions/.
- Enforce mandatory gates and evidence requirements defined in `.agents/orchestration/verification-policy.yaml` and `.agents/orchestration/verification-schema.json`.
</NON_NEGOTIABLES>

<PROCEDURE>

</PROCEDURE>

<VERIFICATION_POLICY>
## Verification matrix

For each task, produce:

| Criterion/check | Evidence | Status |
|---|---|---|
| Acceptance criterion | test/manual/runtime evidence | PASSED/FAILED/SKIPPED |
| Type safety | type-check output | status |
| Lint | lint output | status |
| Tests | suite/count | status |
| Build | build command | status |
| Security | targeted checks | status |
| Architecture / ADR | ADR in docs/decisions/ (if pattern introduced) | PASSED/NA |

## Evidence rules

- Record commands exactly as executed.
- Record exit codes.
- Store concise diagnostic excerpts.
- Record file paths changed.
- Capture limitations and skipped checks.

## Risk-based scope

A tiny copy change may not need a full production build; an auth change may. The verification scope must be justified by impact.

## Final gate

A task can be `COMPLETED` only when:

- all required acceptance criteria pass;
- no blocking failure remains;
- relevant quality checks have run;
- any skipped checks have explicit follow-up;
- memory/state synchronization is complete.

### Exit Criteria
Complete verification report with objective proof of zero exit codes.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Comprehensive verification evidence artifact.
- Passing test logs, build logs, and quality check results.
</DELIVERABLES>
