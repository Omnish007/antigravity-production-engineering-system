---
name: MySQL
category: database
baselineVersion: 8.x / 9.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 8.4 LTS
supportedVersions:
- 8.4 LTS
- '8.0'
- 9.x Innovation
legacyVersions:
- '5.7'
prohibitedVersions:
- < 5.7
sources:
- https://dev.mysql.com/doc/refman/8.0/en/
---
# MySQL Technology Profile

## 1. Scope
Applies to applications utilizing MySQL or MariaDB as a relational database (via Prisma, TypeORM, Sequelize, SQLAlchemy, or native drivers).

## 2. Detection Signals
- Dependencies: `"mysql2"`, `"mysql"`, `"mysqlclient"`, `"pymysql"`
- Connection strings: `mysql://`

## 3. Supported-Version Policy
- Primary Target: MySQL 8.0+ / 8.4 LTS (InnoDB engine).
- Baseline: MySQL 8.0.

## 4. Core Architectural Guidance
- **InnoDB Engine**: Ensure all tables use InnoDB for ACID transactions, foreign key enforcement, and row-level locking.
- **Character Set & Collation**: Use `utf8mb4` with `utf8mb4_0900_ai_ci` (or `utf8mb4_unicode_ci`) for complete Unicode and emoji support.
- **Index Optimization**:
  - Compound indexes must respect the leftmost prefix rule.
  - Keep primary keys compact (e.g., `BIGINT AUTO_INCREMENT`) because secondary indexes store the primary key value as their pointer.
- **Zero-Downtime Migrations**: Use online DDL or tools like `gh-ost` / `pt-online-schema-change` for altering large production tables.

## 5. Security & Performance Guidance
- **Query Parameterization**: Always use parameterized prepared statements to eliminate SQL injection vulnerabilities.
- **Connection Management**: Configure application connection pools with max connections aligned with `max_connections` server configuration.
- **Slow Query Log**: Monitor queries exceeding `long_query_time` threshold.

## 6. Testing Guidance
- Integration Testing: Test migrations and queries against an ephemeral MySQL instance via Docker or Testcontainers.
- Verification: Run `EXPLAIN` on critical queries to verify index usage (`ref`, `range` vs `ALL`).

## 7. Common Anti-patterns
- Using `utf8` (which only supports 3-byte characters) instead of `utf8mb4`, causing data corruption on emojis or multi-byte characters.
- Using wide composite primary keys or UUID strings as primary keys without ordering, causing heavy B-tree index fragmentation.
- Performing table alterations with full table locks during peak production traffic.
- Over-indexing small tables or under-indexing columns used in `WHERE` and `ORDER BY` clauses.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://dev.mysql.com/doc/refman/8.0/en/
- Local Inspection: Inspect ORM configuration and database migration directories.
