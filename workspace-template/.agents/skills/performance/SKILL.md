---
name: performance
description: Measure, analyze, and optimize application performance across frontend, backend, database, and infrastructure using evidence-driven profiling.
---

# Performance Engineering Skill

## Core principle

Measure before optimizing. Every performance change must be backed by profiling data, not assumptions. Premature optimization is a source of complexity; evidence-driven optimization is a source of value.

## Frontend performance

### Core Web Vitals

Target at the 75th percentile:

- **LCP** (Largest Contentful Paint): ≤ 2.5 seconds
- **INP** (Interaction to Next Paint): ≤ 200 milliseconds
- **CLS** (Cumulative Layout Shift): ≤ 0.1

### Bundle optimization

- Analyze bundle size with tools appropriate to the build system.
- Implement code splitting at route and component boundaries.
- Use dynamic imports for heavy, non-critical functionality.
- Tree-shake unused exports.
- Monitor and enforce bundle size budgets where configured.

### Asset optimization

- Use modern image formats (WebP, AVIF) with fallbacks.
- Size images appropriately for their display context.
- Use responsive images with `srcSet` and `sizes`.
- Preload critical assets (fonts, hero images, above-the-fold CSS).
- Defer non-critical scripts and stylesheets.

### Rendering optimization

- Minimize client-side JavaScript; prefer Server Components for non-interactive UI.
- Avoid unnecessary re-renders; use `React.memo`, `useMemo`, and `useCallback` only where profiling justifies it.
- Prevent layout shifts with explicit dimensions and font display strategies.
- Use streaming SSR where supported and beneficial.
- Lazy-load below-the-fold content.

## Backend performance

### API latency

- Profile endpoint response times under realistic load.
- Identify slow middleware, service calls, and database queries.
- Set and monitor latency budgets for critical endpoints.
- Use caching (in-memory, Redis, HTTP cache headers) where read patterns justify it.

### Throughput

- Identify bottlenecks in request processing pipelines.
- Use connection pooling for database and external service connections.
- Implement request queuing for burst handling where appropriate.
- Profile memory usage under sustained load.

### Resource management

- Detect and fix memory leaks using heap analysis.
- Monitor event loop lag for Node.js applications.
- Set appropriate timeouts for all outbound dependencies.
- Implement graceful degradation when dependencies are slow.

## Database performance

### Query optimization

- Use `explain()` / query plans to verify index usage.
- Identify and eliminate collection scans on hot paths.
- Project only necessary fields.
- Use covered queries where index-only responses are possible.

### Index strategy

- Derive indexes from actual query patterns, not speculation.
- Follow the ESR guideline (Equality, Sort, Range) for compound indexes.
- Monitor index usage and remove unused indexes.
- Balance read performance against write/storage cost.

### Connection management

- Configure connection pool size based on actual concurrency.
- Monitor connection utilization and timeouts.
- Use read preferences for read-heavy workloads with replicas.

## Load testing

When performance requirements exist:

- Establish baseline performance with current implementation.
- Define load scenarios that represent realistic traffic patterns.
- Identify breaking points and degradation thresholds.
- Test with representative data volumes, not empty databases.
- Document results with specific metrics, not subjective assessments.

## Caching strategy

Apply caching at the appropriate layer:

| Layer | Tool | Use when |
|---|---|---|
| Browser | HTTP cache headers, service worker | static assets, rarely-changing API responses |
| CDN | edge caching | static content, geographically distributed users |
| Application | in-memory cache, Redis | computed results, session data, rate limiting |
| Database | query cache, materialized views | expensive aggregations, reporting queries |

Every cache must have an explicit invalidation strategy. Document cache TTLs and invalidation triggers.

## Verification

Performance improvements require evidence:

- before/after measurements for the specific metric;
- test methodology and conditions;
- statistical significance for variable metrics;
- no regression in other performance dimensions;
- no regression in correctness or security.

## Anti-patterns

Do not:

- optimize without profiling data;
- add caching without an invalidation plan;
- sacrifice readability for marginal gains;
- add indexes speculatively;
- use `React.memo` / `useMemo` / `useCallback` without measured re-render problems;
- introduce complexity for theoretical future scale without current evidence.
