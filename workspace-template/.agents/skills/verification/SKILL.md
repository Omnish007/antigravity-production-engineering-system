---
name: verification
description: Create objective verification evidence mapping acceptance criteria to commands, tests, outputs, changed files, and known limitations.
---

# Verification Skill

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
