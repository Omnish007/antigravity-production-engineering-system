# Task Lifecycle

## Canonical flow

```text
INTAKE
  -> CONTEXT
  -> CLASSIFY
  -> PLAN (when needed)
  -> IMPLEMENT
  -> TEST
  -> VERIFY
  -> REVIEW
  -> MEMORY SYNC
  -> STATE UPDATE
  -> COMPLETE
```

## Intake

Capture the request, scope, affected areas, constraints, and acceptance criteria. Assign a stable task ID for tracked multi-step work.

## Context

Load project memory and relevant rules/skills. Inspect existing implementations before creating alternatives.

## Classify

Use `task-classifier.md`. Do not run the entire agent library for every task.

## Plan

Planning is mandatory for:

- complex features;
- cross-layer changes;
- architecture changes;
- database migrations;
- security-sensitive changes;
- work with multiple dependencies;
- tasks with significant unknowns.

Small isolated changes may use an abbreviated plan.

## Implement

Make coherent changes in small, verifiable increments. Preserve unrelated user work.

## Test

Use impact-aware testing. Add regression coverage for bugs and contract tests for APIs where applicable.

## Verify

Map acceptance criteria to evidence. Run formatting, linting, type checking, tests, build, and runtime checks according to risk.

## Review

Review the final diff for correctness, security, architecture, regressions, and scope creep. High-risk changes should receive a dedicated code-review pass.

## Memory sync

Apply `.agents/orchestration/memory-sync-policy.md`.

## State update

Update `.agents/state/` only with facts that reflect actual execution. State is not a speculative TODO list.

## Completion states

```text
PENDING -> READY -> IN_PROGRESS -> VERIFYING -> COMPLETED
                         |                 |
                         v                 v
                       BLOCKED           FAILED
                         |                 |
                         +----> READY <---+
```

Blocked tasks require a documented blocker and next unblock condition. Failed tasks must preserve prior evidence; retries are scoped to the failure.
