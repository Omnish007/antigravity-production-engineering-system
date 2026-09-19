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

## External dependencies

Use bounded retries only for operations that are safe to retry. Add idempotency keys or deduplication where a repeated request could create duplicate side effects.

## Verification

Test success, validation failures, authorization failures, not-found/conflict behavior, persistence effects, and dependency failure paths.
