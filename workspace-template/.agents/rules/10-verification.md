# Verification Rules

Recommended activation: **Always On**

## Completion gate

Do not claim completion unless the task has objective verification evidence.

At minimum, determine whether the task requires:

- formatter;
- linter;
- type-check;
- unit tests;
- integration/API tests;
- E2E tests;
- production build;
- targeted runtime smoke check;
- security checks.

## Acceptance criteria

Every acceptance criterion must be marked:

- `PASSED` with evidence;
- `FAILED` with a concrete reason; or
- `SKIPPED` only with an explicit justification and a statement of follow-up.

## Evidence

Capture:

- commands actually executed;
- exit codes;
- relevant test counts;
- files changed;
- build/lint/type status;
- acceptance-criteria evidence;
- failures and limitations.

Do not paste enormous logs into state. Store concise, diagnostic excerpts and point to repository artifacts where appropriate.

## Verification integrity

- Never state a check passed if it was not run.
- Do not treat code inspection as a substitute for runtime verification when runtime behavior matters.
- Do not treat a successful type-check as proof of authorization, UX, or business-rule correctness.
- Do not treat a passing unit test as proof that an API contract or E2E journey works.

## Final review

Before completion, inspect the final diff, confirm no unrelated changes are included, and ensure project memory reflects durable changes.
