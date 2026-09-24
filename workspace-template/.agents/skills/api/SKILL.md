---
name: api
id: SKILL-API-001
description: Design and implement predictable, secure, versioned APIs across REST, GraphQL, gRPC, and event-driven protocols with contract-first schemas and strict authorization.
---

# API Development Skill

<MISSION>
Design and implement predictable, secure, versioned APIs across REST, GraphQL, gRPC, and event-driven protocols with contract-first schemas and strict authorization.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring api capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- For governed execution, the canonical task record `.agents/state/tasks/TASK-ID.json` must exist.
- Use the lifecycle state defined in `.agents/orchestration/task-lifecycle.md` for the current phase; do not require `IN_PROGRESS` merely because the skill is available during execution.
- Implementation-phase mutations require a `TASK_STARTED` event before code/configuration changes. Planning, requirements, analysis, review, verification, and memory-sync phases may legitimately run in their own lifecycle states.
    - Must be loaded as part of the Atomic Backend Bundle alongside `.agents/skills/backend/SKILL.md`, `.agents/skills/security/SKILL.md`, and `.agents/rules/07-security.md`.

### Pre-flight Checklist
- [ ] Input schema validation active on all routes
    - [ ] Standard error envelope returned on failure
    - [ ] Auth & authorization checks enforced server-side
    - [ ] API documentation/contracts updated
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Strict adherence to RULE-ARCH-LAYER-001 (15-layered-architecture.md). Placing business logic, database queries, or ORM/ODM calls directly in API route handlers or controllers is STRICTLY FORBIDDEN.
- Mandate explicit DTO schema validation (Zod, Pydantic, TypeBox, class-validator) on every incoming endpoint payload BEFORE reaching the domain service layer.
- Enforce server-side schema validation on all endpoints.
- Use standard HTTP status codes (200, 201, 400, 401, 403, 404, 409, 422, 500).
- Enforce constant-time comparison (e.g. `timingSafeEqual`, `hmac.compare_digest`) for webhook and token signatures.
- Every mutating endpoint must have an explicit trust model and abuse-control model: user-authenticated (session/token), cryptographically verified (webhook signature), or intentionally public with documented abuse controls (rate limiting, CAPTCHA, or proof-of-work).
</NON_NEGOTIABLES>

<PROCEDURE>
## Protocol selection

Choose the appropriate API protocol based on client requirements and architectural patterns:

- **RESTful HTTP**: Default choice for public-facing, resource-oriented APIs, third-party integrations, and web/mobile clients.
- **GraphQL**: Best for complex, interconnected frontend applications requiring flexible data fetching, client-specified queries, and minimal over-fetching.
- **gRPC / Protocol Buffers**: Best for internal microservice-to-microservice communication, low-latency RPCs, and high-throughput streaming.
- **WebSockets / SSE (Server-Sent Events)**: Best for real-time bidirectional messaging (WebSockets) or server-to-client event streaming (SSE).
- **Webhooks**: Best for asynchronous outbound event delivery to external consumer systems.

## Contract-first design

Define explicit machine-readable contracts before implementation:

- **REST**: OpenAPI 3.1 / Swagger specification defining paths, query parameters, request bodies, responses, status codes, and security schemes.
- **GraphQL**: Schema Definition Language (SDL) defining types, queries, mutations, subscriptions, and custom scalars.
- **gRPC**: Protocol Buffers (`.proto`) files defining services, RPC methods, and strongly-typed request/response messages.
- **Webhooks**: JSON Schema defining the event payload envelope and HMAC signature verification header.

## API versioning and evolution

- **REST versioning**:
  - Use URI path versioning (`/api/v1/resources`) for major breaking architectural changes.
  - Prefer additive, non-breaking schema evolution (adding optional fields) over introducing new version numbers.
  - Deprecate endpoints gracefully using `Sunset` and `Deprecation` HTTP headers before decommissioning.
- **GraphQL / gRPC evolution**:
  - Add new fields with defaults; never remove or rename existing fields without a formal deprecation period.
  - In Protobuf, maintain tag number stability; never renumber or repurpose existing field numbers.

## Endpoint and client registry

- Maintain an explicit API client/registry module for frontend and consuming services.
- Centralize endpoint URL definitions, base configuration, and auth header injection.
- Generate client SDKs or types directly from OpenAPI/GraphQL/Protobuf schemas where supported.

## Request and response envelopes

- **Predictable error envelope**: Expose consistent machine-readable error structures:
  ```json
  {
    "error": {
      "code": "RESOURCE_NOT_FOUND",
      "message": "The requested user does not exist.",
      "details": [{ "field": "userId", "issue": "Must be a valid UUID" }],
      "requestId": "req_01h8x4k2..."
    }
  }
  ```
- **Success payloads**: Avoid arbitrary nesting; return the resource or resource collection directly, with pagination metadata when applicable.

## Validation and authorization

- **Boundary validation**: Reject malformed inputs before reaching domain logic. Validate type, length, range, format, and enum values.
- **Authorization boundaries**: Enforce object-level (Broken Object Level Authorization - BOLA) and property-level (BPLA) authorization on every request.
- **Mass assignment defense**: Bind only explicitly allowed fields from request bodies to domain models.

## Pagination, filtering, and sorting

- **Cursor-based pagination**: Default to cursor/keyset pagination for large or rapidly changing datasets:
  ```text
  GET /api/v1/orders?limit=25&after=cursor_xyz
  ```
- **Offset pagination**: Use offset pagination (`limit` & `offset`) only for small, stable datasets with total count requirements.
- **Filtering & Sorting**: Use explicit, sanitized query parameters (e.g., `status=active&sort=-created_at`). Validate sort fields against an allowlist.

## Idempotency and resilience

- **Idempotency keys**: Require `Idempotency-Key` headers for critical mutating operations (e.g., payment, checkout, order placement) to prevent duplicate side effects upon retries.
- **Rate limiting**: Apply rate limits based on client IP, authenticated user, or API key. Include `RateLimit-*` and `Retry-After` headers in responses.
- **HTTP caching**: Use `ETag` and `Cache-Control` headers for read-heavy resources to enable 304 Not Modified responses.
</PROCEDURE>

<VERIFICATION_POLICY>
## Verification

Verify every API with:
- Contract conformance tests (verifying actual payloads match OpenAPI/GraphQL/Protobuf schemas);
- Schema validation tests for invalid types, missing required fields, and boundary limits;
- Authentication (401) and authorization (403) boundary tests;
- Idempotency tests verifying that duplicate requests with the same key produce identical results without duplicate side effects;
- Rate limit enforcement tests.

### Exit Criteria
API contract verified via automated integration tests with exit code 0.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Verified API endpoints with input validation schemas, error handling, and automated integration tests.
- Updated API documentation and contract specifications.
</DELIVERABLES>
