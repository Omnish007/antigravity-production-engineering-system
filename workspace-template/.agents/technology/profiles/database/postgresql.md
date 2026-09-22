---
name: PostgreSQL
category: database
baselineVersion: 18 / 17 / 16
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 17.x
supportedVersions:
- 18.x
- 17.x
- 16.x
legacyVersions:
- 15.x
- 14.x
prohibitedVersions:
- < 14.x
sources:
- https://www.postgresql.org/docs/current/
---
# PostgreSQL Technology Profile

```yaml
technology: postgresql
supported_versions:
  - "18"
  - "17"
  - "16"
preferred_version: "18"
verified_at: "2026-09-22"
sources:
  - url: https://www.postgresql.org/docs/current/
    verified_at: "2026-09-22"
review_policy:
  max_age_days: 30
```

## 1. Scope
Applies to applications utilizing PostgreSQL as a relational database (via Prisma, Drizzle, TypeORM, SQLAlchemy, or native drivers).

## 2. Detection Signals
- Dependencies: `"pg"`, `"@prisma/client"`, `"drizzle-orm"`, `"psycopg2"`, `"asyncpg"`
- Files: `schema.prisma`, `drizzle.config.ts`, `migrations/`
- Connection strings: `postgres://`, `postgresql://`

## 3. Supported-Version Policy
- Primary Target: PostgreSQL 18 / 17 / 16 (Current supported release lines as of 2026).
- Baseline: PostgreSQL 14+.

## 4. Core Architectural Guidance
- **Relational Integrity**: Enforce constraints at the database level using foreign keys, `CHECK` constraints, unique constraints, and `NOT NULL` columns.
- **Index Strategy**:
  - B-tree indexes for equality, range queries, and sorting.
  - GIN indexes for JSONB containment (`@>`), array operations, and full-text search.
  - Partial indexes (`WHERE is_active = true`) to index high-selectivity subsets efficiently.
- **Transactions & Concurrency**:
  - Default isolation level is Read Committed.
  - Use row-level locking (`SELECT ... FOR UPDATE`) or Serializable isolation when preventing write skew in financial or inventory mutations.
  - Keep transaction duration minimal to avoid lock contention and connection starvation.
- **Migrations & Zero-Downtime**:
  - All schema changes must be versioned, idempotent, and backward-compatible (expand/contract).
  - Use `CONCURRENTLY` for index creation in production (`CREATE INDEX CONCURRENTLY`) to avoid write locks.

## 5. Security & Performance Guidance
- **Connection Pooling**: Use connection poolers (PgBouncer, Supabase pooler, Neon serverless) to manage client connection limits.
- **Parameterization**: Always use parameterized queries (`$1`, `$2`); never interpolate raw values into SQL strings.
- **Role Permissions**: Restrict application database users to least-privilege roles (`SELECT`, `INSERT`, `UPDATE`, `DELETE`), preventing `DROP` or `ALTER` in runtime credentials.
- **Query Optimization**: Analyze slow queries with `EXPLAIN (ANALYZE, BUFFERS)` to verify index usage and buffer cache hits.

## 6. Testing Guidance
- Integration Testing: Use Testcontainers or ephemeral PostgreSQL Docker instances for integration tests.
- Schema Validation: Run migration verification against a fresh database in CI.
- Verification: Validate queries using `EXPLAIN` and verify migration scripts apply and rollback cleanly.

## 7. Common Anti-patterns
- Adding `NOT NULL` columns without a default on large tables without an expand/contract migration phase.
- Missing indexes on foreign key columns, leading to sequential table scans during cascade operations or joins.
- Performing unbounded queries without `LIMIT` and cursor-based pagination.
- Using `SELECT *` in production queries instead of selecting specific columns.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://www.postgresql.org/docs/current/
- Local Inspection: Inspect migration directories and database schema configuration files.
