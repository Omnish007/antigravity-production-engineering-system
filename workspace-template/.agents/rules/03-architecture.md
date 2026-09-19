# Architecture Rules

Recommended activation: **Model Decision** for architecture-sensitive tasks.

## Default architecture

Use a modular-monolith mindset by default:

- clear domain boundaries;
- explicit dependency direction;
- one responsibility per module;
- infrastructure isolated behind interfaces where that buys testability or replacement ability;
- no premature microservices.

For a full-stack application, a common baseline is:

```text
apps/web   -> Next.js / React UI
apps/api   -> Node.js / Express HTTP API
packages/* -> shared contracts/utilities only when justified
MongoDB    -> persistence
```

The actual repository layout may differ. The chosen layout belongs in `docs/ARCHITECTURE.md`.

## Dependency direction

Prefer:

```text
UI -> application/use-case layer -> domain -> infrastructure
HTTP/API -> application/use-case layer -> domain -> infrastructure
```

Infrastructure may implement interfaces defined by higher layers; domain logic should not depend directly on HTTP frameworks, UI libraries, or database drivers.

## Module boundaries

A feature module should own its:

- routes/controllers;
- input/output schemas;
- business services/use cases;
- domain logic;
- data access adapters;
- tests;
- feature-specific UI where the frontend architecture uses feature folders.

Shared code must be genuinely cross-domain. Do not create a `utils` or `common` bucket merely because ownership is inconvenient.

## Change rules

Architecture changes require:

- identified impact;
- alternatives considered when the choice is non-obvious;
- explicit decision;
- migration or compatibility strategy when existing behavior changes;
- relevant ADR;
- verification evidence.

## API boundary

Treat the API as a contract. Validate at the boundary, normalize inputs, enforce authorization, and keep transport concerns separate from domain logic.

## Data boundary

No arbitrary database access from UI components or HTTP handlers. Use a deliberate data-access/service path so validation, authorization, observability, and consistency can be enforced centrally.
