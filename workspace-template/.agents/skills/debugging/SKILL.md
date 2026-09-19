---
name: debugging
description: Perform evidence-driven root-cause analysis across frontend, backend, API, database, and environment failures.
---

# Debugging Skill

## Investigation loop

```text
Observe -> Reproduce -> Narrow -> Hypothesize -> Test -> Explain -> Fix -> Verify
```

## Narrowing strategy

Start at the failing boundary and divide the path:

- browser/UI state;
- network request;
- API validation/auth;
- service/domain logic;
- database query/state;
- external dependency;
- environment/build/runtime.

## Hypothesis discipline

For each hypothesis, identify:

- evidence for;
- evidence against;
- fastest discriminating test;
- expected result if true.

Do not change multiple unrelated things before you know which change addressed the failure.

## Common traps

Avoid:

- adding broad retries to hide timeouts;
- disabling type checks;
- suppressing linter errors;
- bypassing authorization to "confirm" a path;
- deleting data to make a test pass;
- assuming caches are correct without checking invalidation;
- assuming a frontend error implies a backend defect.

## Output

Document root cause, evidence, fix, regression coverage, and any durable prevention rule worth recording.
