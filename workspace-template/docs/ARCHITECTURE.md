# Architecture

> This document describes the actual chosen architecture. Replace placeholders from repository evidence during project initialization; do not invent values.

## Architectural style

Document the chosen architectural pattern:
- **Modular Monolith**: In-process domain modules with explicit interfaces and boundary enforcement.
- **Clean / Hexagonal Architecture**: Pure domain core, application use cases, and interchangeable infrastructure/presentation adapters.
- **Client-Server / Multi-tier**: Dedicated frontend (Web/Mobile) communicating with backend API services.
- **Microservices / Event-Driven**: Distributed autonomous services communicating via HTTP/gRPC and event brokers.

## System context

```text
[User Clients / Browsers / Mobile]
               |
               v
     [Load Balancer / CDN]
               |
               v
    [Frontend Application]  ---> [Backend API Service]
                                         |
                       +-----------------+-----------------+
                       |                                   |
                       v                                   v
             [Primary Database]                   [Cache / Queue]
             (SQL / Document)                     (Redis / RabbitMQ)
```

> Adapt this diagram to reflect the actual components and external integrations in the repository.

## Repository structure

Document the actual repository layout:

```text
# Example Monorepo:
apps/
  web/             # Frontend application
  api/             # Backend service
packages/
  domain/          # Shared domain models and core business rules
  contracts/       # API contracts (OpenAPI, DTOs, schemas)

# Example Single-Service Clean Architecture:
src/
  domain/          # Pure domain entities, value objects, domain events
  application/     # Use cases, application services, port interfaces
  infrastructure/  # Database adapters, external API clients, message brokers
  presentation/    # HTTP controllers, CLI commands, middleware
```

## Frontend architecture

Document:
- Framework and rendering strategy (SSR, SSG, SPA, Isomorphic);
- Routing and navigation architecture;
- State management strategy (server cache vs local/global client state);
- Component hierarchy and design token integration;
- Form handling and validation approach;
- API client integration and error/loading handling.

## Backend architecture

Document:
- Runtime, framework, and transport layer (HTTP, gRPC, WebSocket);
- Middleware pipeline (security, logging, rate limiting, validation, auth);
- Application and domain service boundaries;
- Data access / repository layer patterns;
- Background job processing, workers, and queues;
- Observability (structured logging, tracing, metrics).

## Database architecture

Document:
- Database engines (e.g., PostgreSQL, MySQL, SQLite, MongoDB, DynamoDB, Redis);
- Schemas, tables/collections, and entity relationships;
- Indexing strategy for query performance;
- Data integrity constraints and validation boundaries;
- Transaction management and isolation levels;
- Migration and schema evolution strategy (expand/migrate/contract).

## Trust boundaries & security

Document:
- Client-to-API boundary (HTTPS, authentication, rate limiting, CORS);
- API-to-Database boundary (connection credentials, least privilege, VPC);
- Internal service-to-service boundaries (mTLS, service tokens);
- Third-party webhook and external API boundaries (signature verification, timeouts).

## Runtime and deployment architecture

Document:
- Target runtime environment (Containers/Docker, Kubernetes, Serverless, VM);
- Process model, scaling policies, and reverse proxies;
- Configuration and secret management (12-Factor environment variables, secret vaults);
- Health checks (`/health/live`, `/health/ready`) and graceful shutdown.

## Cross-cutting concerns

Document:
- Structured logging format, correlation ID propagation, and log aggregation;
- Centralized error handling and machine-readable error codes;
- Distributed tracing (OpenTelemetry);
- Feature flag management.

## Scalability and disaster recovery

Document:
- Caching strategy (browser, CDN, application, database);
- Connection pooling and read replica routing;
- Backup strategy, schedule, and recovery testing;
- Recovery Time Objective (RTO) and Recovery Point Objective (RPO).

## Dependency direction

Document the allowed dependency graph:
- Inward dependencies only (Presentation -> Application -> Domain);
- Infrastructure implements interfaces defined by the Application/Domain layer;
- Prohibited shortcuts (e.g., UI directly querying database, domain logic depending on HTTP frameworks).

## Architecture evolution

Material changes to this architecture require an ADR (`docs/decisions/ADR-*.md`) before acceptance and implementation.
