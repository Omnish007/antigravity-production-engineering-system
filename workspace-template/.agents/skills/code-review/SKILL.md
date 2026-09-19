---
name: code-review
description: Review completed changes for correctness, architecture, security, maintainability, performance, testing, and unintended scope.
---

# Code Review Skill

## Review order

1. Requirement/acceptance alignment.
2. Correctness and edge cases.
3. Authorization/security.
4. Data integrity and concurrency.
5. Architecture/dependency direction.
6. Maintainability/readability.
7. Performance/resource behavior.
8. Test quality.
9. Observability/error handling.
10. Scope and diff hygiene.

## Findings

Use:

- `CRITICAL` — security, data loss, severe correctness, or production-blocking issue;
- `HIGH` — significant defect or regression risk;
- `MEDIUM` — maintainability/performance/test gap worth addressing;
- `LOW` — minor improvement that should not block delivery.

Only label a finding when concrete evidence supports it.

## Review anti-patterns

Do not request rewrites just to match personal style. Existing conventions and accepted ADRs matter.

## Final review

Inspect the final diff, not only individual files. Verify that the implementation, tests, docs, and state agree with one another.
