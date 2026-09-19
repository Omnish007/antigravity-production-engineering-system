---
name: api
description: Design and implement predictable HTTP APIs with validated contracts, resource-level authorization, centralized endpoints, error semantics, and documentation.
---

# API Development Skill

## Contract first

For meaningful API changes, define:

- method and path;
- purpose;
- auth requirement;
- request schema;
- response schema;
- status codes;
- validation failures;
- authorization failure behavior;
- pagination/filter/sort semantics;
- idempotency/retry behavior;
- rate/resource limits;
- observability expectations.

## Paths

Use consistent resource-oriented naming. For public/external contracts, establish an explicit versioning strategy and record it in an ADR when the API is expected to evolve over time.

## Endpoint registry

Frontend clients should use the project's centralized endpoint registry/module. The server route definitions remain close to the backend resource module. The two responsibilities are related but should not be conflated.

## Response shape

Use a stable project-defined envelope only if it materially improves consistency. Do not create wrappers merely for aesthetic uniformity. Errors should expose stable machine-readable codes and safe human-readable messages where practical.

## Validation and authorization

Validate all external input on the server. Authorize every sensitive object/action combination server-side. Avoid mass-assignment patterns that allow clients to set protected fields.

## Pagination

Prefer cursor-based pagination for large/churn-heavy datasets where stable ordering matters. Offset pagination is acceptable for small, stable datasets when its trade-offs are understood and documented.

## Testing

Every non-trivial endpoint should have tests covering validation, auth, primary success, common client failure, and relevant persistence behavior. Add idempotency/concurrency tests when the endpoint triggers side effects.
