---
name: bug-fix
description: Resolve defects systematically by reproducing the issue, isolating root cause, applying the smallest coherent fix, and proving regression safety.
---

# Bug Fix Skill

## Workflow

1. Capture symptom and expected behavior.
2. Reproduce the failure if feasible.
3. Find the narrowest failing boundary.
4. Form explicit hypotheses.
5. Gather evidence that supports/refutes each hypothesis.
6. Identify root cause, not merely the visible error.
7. Implement the smallest coherent fix.
8. Add or strengthen regression coverage.
9. Re-run focused and broader tests according to impact.
10. Review for similar failure modes elsewhere in the codebase.
11. Synchronize project memory if a new convention, architectural insight, or durable workaround was discovered.

## Scope control

- Fix the reported bug; do not mix refactoring or feature work into the same change.
- If you discover related issues during investigation, document them separately.
- Keep the fix as small and targeted as possible to minimize regression risk.
- If the fix requires architectural changes, create an ADR and escalate.

## Risk assessment

Before applying the fix, assess:

- How many code paths are affected by this change?
- Could this fix break other functionality?
- Does this fix require a data migration or schema change?
- Is the fix backward-compatible?
- What is the blast radius if the fix has unintended consequences?

## Evidence hierarchy

Prefer direct evidence:

- failing test;
- runtime log/stack;
- network trace;
- database state;
- reproduction case;
- code path analysis;
- versioned documentation.

Do not "fix" a symptom by swallowing errors, disabling validation, increasing arbitrary timeouts, or adding retries without understanding the failure.

## Regression coverage

The regression test should:

- fail before the fix when practical, then pass after;
- test the specific failure condition, not just the general happy path;
- include edge cases discovered during investigation;
- be named descriptively so the original bug can be traced from the test name.

## Anti-patterns

Do not:

- "fix" a symptom by swallowing errors, disabling validation, increasing arbitrary timeouts, or adding retries without understanding the failure;
- apply a fix without reproducing the bug first (unless reproduction is infeasible);
- copy-paste a fix from an unverified external source without understanding it;
- close the bug without evidence that the fix works.

## Documentation

After the fix is verified:

- update the bug report with root cause, fix, and evidence;
- record any new convention or defensive pattern in `CONVENTIONS.md` if the bug class could recur;
- create an ADR if the fix revealed an architectural weakness;
- update `CURRENT_STATE.md` if the fix affects project health.
