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
10. Review for similar failure modes elsewhere.
11. Synchronize project memory if a new convention, architectural insight, or durable workaround was discovered.

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

The regression test should fail before the fix when practical, then pass after the fix.
