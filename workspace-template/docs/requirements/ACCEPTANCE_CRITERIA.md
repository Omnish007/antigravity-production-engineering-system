# Acceptance Criteria Register

> Optional central register for projects with multiple features. Feature-specific criteria may live beside the feature specification.

## Criteria table

| ID | Requirement/feature | Criterion (Given/When/Then or measurable threshold) | Priority | Status | Verification evidence | Verified by | Date |
|---|---|---|---|---|---|---|---|

## Status values

| Status | Meaning |
|---|---|
| Draft | Criterion written but not yet reviewed or agreed upon |
| Ready | Criterion reviewed, agreed, and ready for implementation |
| In progress | Implementation work has started |
| Verified | Criterion met with objective evidence linked |
| Failed | Verification attempted but criterion not met |
| Deferred | Criterion postponed to a future iteration |
| Blocked | Verification cannot proceed due to a dependency or blocker |

## Writing effective criteria

- Use Given/When/Then format for behavioral criteria.
- Use measurable thresholds for performance/reliability criteria (e.g., "response time < 200ms at P95").
- Each criterion should be independently verifiable without requiring subjective judgment.
- Avoid criteria that can only be verified by "it works" or "it looks right."
- Link to specific test cases, verification reports, or screenshots as evidence.

## Priority levels

| Priority | Meaning |
|---|---|
| Must | Required for the feature to be considered complete |
| Should | Expected but the feature can ship without it under time pressure |
| Could | Desirable enhancement if time permits |

## Traceability

Every non-trivial criterion should trace to:

1. A source requirement (PRD, feature spec, or user story).
2. A verification method (automated test, manual verification, or metric).
3. Evidence of the result (test output, screenshot, metric dashboard).

When a criterion is verified, update the status, link the evidence, and record who verified it and when.

## Cross-feature criteria

For criteria that span multiple features (e.g., "all API endpoints return errors in the standard format"), track them here rather than duplicating across feature specs.

## Review cadence

Review this register when:

- A new feature is planned (add criteria);
- A feature is completed (verify and link evidence);
- A requirement changes (update or supersede affected criteria);
- A bug reveals a missing criterion (add the gap).
