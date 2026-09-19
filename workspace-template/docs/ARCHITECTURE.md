# Architecture

> This document describes the actual chosen architecture. Replace placeholders from repository evidence during initialization.

## Architectural style

Default starting point: modular monolith with explicit boundaries. Avoid microservices unless a concrete requirement justifies the operational complexity.

## System context

```text
[User Browser]
      |
      v
[Next.js / React Web]
      |
      v
[Express API]
      |
      v
[Application / Domain Logic]
      |
      v
[MongoDB]
```

External services and async systems should be added here when actually adopted.

## Repository structure

Document the actual structure here. For a common full-stack layout:

```text
apps/web      # Next.js application
apps/api      # Express application
packages/*    # only justified shared code/contracts
```

## Frontend architecture

Document:

- routing;
- Server/Client Component boundaries;
- state management;
- data-fetching/caching model;
- component organization;
- form/validation approach;
- endpoint client/registry location;
- error/loading strategy.

## Backend architecture

Document:

- HTTP layer;
- middleware;
- validation;
- authorization;
- application/service layer;
- domain modules;
- persistence/data-access layer;
- background jobs if any;
- observability/error handling.

## Database architecture

Document:

- collections;
- ownership/relationships;
- indexes;
- validation;
- transaction boundaries;
- migration/backfill approach;
- archival/retention strategy.

## Trust boundaries

Document browser/API, API/database, API/external-service, worker/database, and other relevant boundaries with authentication/authorization and data sensitivity.

## Runtime/deployment architecture

Document hosts, processes, containers, reverse proxies, storage, queues, monitoring, and secrets management.

## Dependency direction

Document the allowed dependency graph and prohibited shortcuts.

## Architecture evolution

Any material structural change should be recorded as an ADR and reflected here after acceptance.
