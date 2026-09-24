---
name: quality-gates
id: SKILL-QUALITY-001
description: Evaluate agent output quality through self-assessment, trajectory analysis, regression detection, and CI/CD gating before declaring work complete.
---

# Quality Gates Skill

<MISSION>
Evaluate agent output quality through self-assessment, trajectory analysis, regression detection, and CI/CD gating before declaring work complete.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring quality-gates capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- For governed execution, the canonical task record `.agents/state/tasks/TASK-ID.json` must exist.
- Use the lifecycle state defined in `.agents/orchestration/task-lifecycle.md` for the current phase.
- Implementation-phase mutations require a `TASK_STARTED` event before code/configuration changes; planning and verification may run in their designated lifecycle states.

### Pre-flight Checklist
- [ ] Determine applicable quality gates based on project type and scope of change
- [ ] Applicable checks (format, lint, typecheck, tests, build) execute with exit code 0
- [ ] ADR in `docs/decisions/ADR-NNN-<slug>.md` verified if architectural trigger is met
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Every applicable quality gate configured for the project (e.g. format, lint, typecheck, test, build) must pass with exit code 0; gates irrelevant to the project type or task scope (e.g. accessibility audits on CLI scripts or browser E2E on pure libraries) are not required.
- Provide exact command output and exit codes as evidence for every executed gate.
- No applicable gate may be suppressed with `|| true` or ignored to force clearance.
- If the task met the Canonical ADR Trigger, an ADR in `docs/decisions/ADR-NNN-<slug>.md` is a mandatory prerequisite for gate clearance.
</NON_NEGOTIABLES>

<PROCEDURE>
## Purpose

Ensure that AI-generated changes meet production quality standards before they are declared complete or merged. This skill provides a structured evaluation framework for the agent's own output.

## Pre-completion checklist

Before declaring any task complete, verify:

1. **Requirement alignment**: Every acceptance criterion has been addressed with evidence.
2. **Scope discipline**: No unrelated changes were introduced.
3. **Code quality**: Format, lint, type-check pass.
4. **Test coverage**: New behavior has appropriate test coverage.
5. **Security**: No new vulnerabilities introduced; auth/validation intact.
6. **Performance**: No obvious performance regressions.
7. **Accessibility**: UI changes maintain accessibility standards.
8. **Documentation**: Relevant docs and memory updated.
9. **Diff review**: Final diff contains only intended changes.
10. **Architecture & ADRs**: If the task made a Type 1 decision or evaluated architectural trade-offs, verify that a formal ADR exists in `docs/decisions/` and is registered in `docs/decisions/INDEX.md`.

## Trajectory evaluation

Assess the quality of the path taken, not just the final output:

- Was the plan followed or did scope creep occur?
- Were unnecessary files loaded or modified?
- Were there doom loops or repeated failed attempts?
- Was the approach efficient or were there avoidable detours?
- Were decisions made with appropriate evidence?

Record trajectory observations in the task evidence for process improvement.

## Final-answer validation

Before presenting results:

- Re-read the original requirement.
- Compare the implemented behavior against each acceptance criterion.
- Verify that the code actually does what the documentation claims.
- Check that error handling covers realistic failure modes.
- Ensure the change works in the contexts it was designed for (responsive breakpoints, different user roles, edge cases).

## Regression detection

Verify that existing functionality is preserved:

- Run the full relevant test suite, not just new tests.
- Check that no previously passing tests now fail.
- Verify that unmodified features still function at the integration level.
- For UI changes, verify adjacent layouts and interactions are not broken.
- For API changes, verify backward compatibility or documented breaking changes.

## CI/CD gating criteria

AI-generated changes should pass the same gates as human-authored changes:

- all configured linters and formatters;
- full type-check;
- unit and integration test suites;
- security scanning (dependency audit, secret detection);
- build verification;
- accessibility checks where configured;
- performance budgets where configured.

If any gate fails, the change should not be merged. The agent should attempt to fix the failure or document it as a known limitation.

## Quality evidence

Produce a structured quality report as part of task completion:

```text
Quality Gate          | Status  | Evidence
─────────────────────|─────────|──────────────────
Acceptance criteria   | PASSED  | All 5 criteria verified
Type-check           | PASSED  | tsc exit 0
Lint                 | PASSED  | eslint exit 0
Tests (focused)      | PASSED  | 12/12
Tests (broad)        | PASSED  | 147/147
Build                | PASSED  | production build exit 0
Security scan        | PASSED  | dependency audit & secret scan: 0 vulnerabilities, 0 secrets
Diff review          | PASSED  | 6 files, no unintended changes
Regression           | PASSED  | No previously passing tests failed
Memory sync          | DONE    | CURRENT_STATE.md updated
```

## Continuous improvement

After completing the quality assessment:

- Identify recurring quality issues that could be prevented by better rules or conventions.
- Suggest process improvements when patterns emerge.
- Record prevention strategies in project memory when they are durable.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
All policy-mandated quality gates verified with exit code 0 and substantive evidence.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Quality gate evaluation report.
- Passing lint, typecheck, test, and build verifications recorded in verification evidence.
</DELIVERABLES>
