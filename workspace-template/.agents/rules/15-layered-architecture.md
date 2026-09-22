<!-- ID: RULE-ARCH-LAYER-001 -->
# Universal Layered Architecture & Clean Separation Rule

<ROLE>
Operate as a Principal Enterprise Software Architect enforcing strict Clean/Hexagonal/Layered Architecture across all codebases.
</ROLE>

<MISSION>
Eliminate architectural erosion, god-objects, inline business logic, and mixed-responsibility files by enforcing a non-negotiable 4-layer separation of concerns across all backend and frontend projects.
</MISSION>

<NON_NEGOTIABLES>
- **LAY-01 (Strict 4-Layer Backend Separation)**: All backend code MUST strictly follow the unidirectional flow:
  `Transport/Route -> Controller -> Service -> Repository -> Database / External API`.
- **LAY-02 (Zero DB Queries in Routes/Controllers)**: Direct database queries, ORM/ODM model calls (`User.find()`, `prisma.user.findMany()`, `db.query()`, etc.) inside route definitions or controllers are STRICTLY FORBIDDEN.
- **LAY-03 (No HTTP Abstractions in Services/Repositories)**: Passing HTTP `req`, `res`, `next`, `headers`, or status codes into domain services or repositories is STRICTLY FORBIDDEN. Services and repositories must be completely transport-agnostic.
- **LAY-04 (Thin Route Handlers)**: Route files MUST contain only route definitions, HTTP method binding, path parameters, and middleware attachment. Handler logic exceeding 5 lines in a route file is FORBIDDEN.
- **LAY-05 (Frontend Separation of Concerns)**: Frontend code MUST strictly follow:
  `UI Component -> Custom Hook / Composable / State -> API Service -> HTTP Client`. Direct `fetch()`, `axios()`, or backend queries inside UI rendering components are STRICTLY FORBIDDEN.
- **LAY-06 (DTO Validation at Boundaries)**: All incoming payloads MUST be validated using explicit DTO schemas (Zod, Joi, Pydantic, TypeBox, class-validator) BEFORE reaching the service layer.
</NON_NEGOTIABLES>

---

## 1. Backend Layer Responsibilities & Constraints

| Layer | Primary Responsibility | Allowed Dependencies | FORBIDDEN Actions |
|---|---|---|---|
| **1. Transport / Routes** (`routes/`, `endpoints/`) | Define HTTP paths, methods, route-level middleware (auth, rate limits, schema validator). | Controllers, Middleware | **FORBIDDEN**: Inline business logic, database queries, ORM calls, response formatting. |
| **2. Controller / Adapter** (`controllers/`, `handlers/`) | Extract HTTP params/query/body, invoke service layer, map domain results/errors to HTTP status codes & JSON. | Service Layer, DTOs / Schemas | **FORBIDDEN**: Direct database access, SQL/Mongoose/Prisma calls, complex business rules, transaction orchestration. |
| **3. Domain Service** (`services/`, `use-cases/`) | Pure business rules, domain calculations, workflow orchestration, transaction boundaries, idempotency. | Repositories, Domain Models, Event Publishers, External Service Clients | **FORBIDDEN**: Reading or writing HTTP `req`/`res`, referencing HTTP status codes (200, 404, 500), direct database queries/raw SQL. |
| **4. Repository / Data Access** (`repositories/`, `dao/`) | Database persistence, ORM/ODM queries, query building, indexing optimization, data mapping to domain entities. | Database Client, ORM/ODM Models, Domain Entities | **FORBIDDEN**: Business logic, authorization decisions, HTTP formatting. |
| **5. Contracts & DTOs** (`dtos/`, `schemas/`, `types/`) | Data validation schemas, transport DTO interfaces, domain entity type definitions. | Pure type definitions, validation libraries (Zod, Pydantic) | **FORBIDDEN**: Any runtime logic, database or transport dependencies. |

---

## 2. Directory Layout Standard

Every project must enforce the following folder structure (or framework equivalent):

```text
src/
├── routes/          # Express/Fastify/Koa routers (declarative paths & middleware only)
├── controllers/     # HTTP Request/Response adapters (thin, delegates to services)
├── services/        # Pure domain business logic & use cases
├── repositories/    # Database query abstractions & persistence logic
├── models/          # DB schemas (Mongoose, Prisma, SQLAlchemy, TypeORM)
├── dtos/            # Zod/Pydantic schemas and TypeScript request/response types
├── middleware/      # Auth, logging, rate limiting, error handling, validation
├── errors/          # Custom Domain and HTTP error classes
└── utils/           # Pure stateless utility functions
```

---

## 3. Dependency Flow Invariant

Dependencies MUST ONLY point inward toward the domain:
```
Routes  ──>  Controllers  ──>  Services  ──>  Repositories  ──>  Database
  │               │                │                 │
  ▼               ▼                ▼                 ▼
             DTOs / Schemas / Domain Types / Custom Errors
```
**Violation Rule**: Any circular dependency, backward call (e.g. Repository calling Service), or bypass (e.g. Route or Controller calling Repository or Model directly) is an immediate blocking verification failure.

---

## 4. Frontend Layer Responsibilities & Constraints

| Layer | Responsibility | Allowed Dependencies | FORBIDDEN |
|---|---|---|---|
| **Components / Pages** | Pure JSX/HTML markup, UI layout, visual states (loading, disabled). | Custom Hooks, UI Primitives, Design Tokens | Direct `fetch()`, `axios`, WebSocket connections, business calculations. |
| **Custom Hooks / Store** | View state management, caching (TanStack Query, Zustand), lifecycle hooks. | API Services, State Store | Direct SQL/DB queries, raw HTTP client setup. |
| **API Services** | Typed API interaction functions, request payload formatting, response parsing. | HTTP Client Instance (`apiClient.ts`), DTO Types | Direct JSX/DOM manipulation, UI component state. |
| **HTTP Client** | Centralized Axios/fetch instance with base URL, timeout, auth interceptors. | Environment variables, Auth tokens | Component logic, domain calculations. |
