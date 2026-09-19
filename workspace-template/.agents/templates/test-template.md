# Test Specification

## Metadata

- Test ID:
- Related requirement/AC:
- Author:
- Last updated:

## Scenario

Describe the behavior being tested in one sentence.

## Risk addressed

What could go wrong if this behavior is broken? Why does this test exist?

## Level

Unit | Integration | API | E2E | Contract | Performance | Accessibility

## Preconditions

- System state required before the test runs.
- Data that must exist.
- Services that must be available.
- Authentication/authorization state.

## Given

Describe the initial context.

## When

Describe the action or trigger.

## Then

Describe the expected observable outcome.

## Edge cases

| Case | Given | When | Then |
|---|---|---|---|
| Empty input | | | |
| Maximum boundary | | | |
| Invalid input | | | |
| Concurrent access | | | |
| Timeout/slow response | | | |

## Error cases

| Case | Given | When | Then |
|---|---|---|---|
| Unauthorized | | | |
| Not found | | | |
| Validation failure | | | |
| Dependency failure | | | |

## Security cases

| Case | Given | When | Then |
|---|---|---|---|
| Injection attempt | | | |
| Privilege escalation | | | |
| CSRF/XSS | | | |

## Test data strategy

- How is test data created? (factories, fixtures, seeds, builders)
- How is test data isolated between runs?
- Are there data volume requirements?

## External dependency strategy

- What external services does this test depend on?
- Are they mocked, stubbed, or real?
- What happens if the dependency is unavailable?

## Cleanup / isolation

- How is state cleaned up after the test?
- Can tests run in parallel safely?
- Are database transactions rolled back?

## Expected evidence

- Command to execute:
- Expected exit code:
- Expected output patterns:
- Expected coverage impact:

## Related acceptance criteria

Link to the specific AC this test verifies.

## Maintenance notes

Any known fragility, flakiness, or special requirements for maintaining this test.
