---
name: backend
description: Implement production-grade Node.js and Express 5 backend modules with explicit boundaries, validation, authorization, error handling, and observability.
---

# Backend Development Skill

## Default structure

A feature can follow a modular pattern such as:

```text
feature/
  controller.ts
  service.ts
  repository.ts
  schema.ts
  types.ts
  routes.ts
  tests/
```

Adapt to the repository's actual architecture rather than forcing this exact tree.

## Request path

Prefer:

```text
request -> security middleware -> validation -> authorization -> controller -> service/use case -> repository -> response
```

Controllers should be thin. Business rules belong in services/domain logic.

## Express 5

Use native async/Promise error propagation rather than legacy async-error patches unless the repository has a justified compatibility reason. Centralize error handling in final error middleware.

## Validation

Validate params, query, headers, and bodies against explicit schemas. Apply server-side validation even when the frontend already validates.

## Authorization

Perform resource-level and action-level authorization in backend logic. Never trust a client-supplied role/owner field.

## Operational controls

Include where applicable:

- request IDs;
- structured logs;
- rate limits;
- body-size limits;
- timeouts for outbound dependencies;
- safe CORS;
- security headers;
- health/readiness endpoints;
- graceful shutdown.

### Structured logging

Use structured log output (JSON) with consistent fields:

- `requestId` / correlation ID for tracing;
- `userId` for authenticated requests (without sensitive fields);
- `action` / event type;
- `duration` for timed operations;
- `error` with structured error details for failures.

Propagate correlation IDs from incoming requests through all downstream calls.

### Circuit breaker

For external service dependencies:

- track failure rates over a sliding window;
- open the circuit after threshold failures to prevent cascade;
- provide fallback behavior when the circuit is open;
- periodically attempt recovery (half-open state);
- log circuit state transitions.

### Background jobs and queues

For work that does not need to be synchronous:

- use job queues for deferred processing when the project warrants them;
- ensure jobs are idempotent when retries are possible;
- implement dead-letter handling for permanently failed jobs;
- monitor queue depth and processing latency;
- set timeouts for job execution.

### Rate limiting

Implement rate limiting for:

- authentication endpoints (strict limits);
- API endpoints with costly operations;
- public-facing endpoints susceptible to abuse.

Return appropriate HTTP status (429) with `Retry-After` headers. Use sliding window or token bucket algorithms.

### Graceful shutdown

When receiving a termination signal:

- stop accepting new connections;
- complete in-flight requests within a reasonable timeout;
- close database connections and external clients;
- flush logs and metrics;
- exit cleanly.

## External dependencies

Use bounded retries only for operations that are safe to retry. Add idempotency keys or deduplication where a repeated request could create duplicate side effects.

## Verification

Test success, validation failures, authorization failures, not-found/conflict behavior, persistence effects, and dependency failure paths.
