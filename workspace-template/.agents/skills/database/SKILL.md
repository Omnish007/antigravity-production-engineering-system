---
name: database
id: SKILL-DB-001
description: Design, model, optimize, and safely migrate both Relational (SQL) and Document/NoSQL databases with strict data integrity, indexing strategy, and zero-downtime evolution.
---

# Database Engineering Skill

<MISSION>
Design, model, optimize, and safely migrate both Relational (SQL) and Document/NoSQL databases with strict data integrity, indexing strategy, and zero-downtime evolution.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring database capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task record `.agents/state/tasks/TASK-ID.json` must be `IN_PROGRESS`.
- A `TASK_STARTED` event must be recorded in `.agents/state/events/TASK-ID.jsonl`.
- Must consult `.agents/state/stack.json` and load the matching profile from `.agents/technology/profiles/database/` (e.g. `postgresql.md`, `mongodb.md`, `mysql.md`, `sqlite.md`, `redis.md`, `dynamodb.md`).

### Pre-flight Checklist
- [ ] Active database profile loaded from `.agents/technology/profiles/database/`
- [ ] Access patterns and query shapes documented before schema design
- [ ] Schema changes verified against database paradigm (relational migrations vs document validation)
- [ ] Concurrency and atomicity controls verified for target database
- [ ] Parameterized queries or type-safe query builders verified (zero injection)
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Always use parameterized queries, typed ORM models, or prepared statements; string concatenation in queries is strictly forbidden.
- Structure data models around explicit, documented access patterns and cardinality boundaries.
- Schema changes must follow a controlled, verified evolution path appropriate to the engine (versioned migrations for relational systems; versioned validators/updaters for document stores).
- Atomicity and consistency boundaries must adhere to the target database's guarantees (ACID transactions in relational engines; single-document atomicity or multi-document transactions in MongoDB; DynamoDB TransactWriteItems; Redis pipelines/transactions).
- If meeting the Canonical ADR Trigger (Type 1 Reversibility OR any two of: D1 Blast Radius, D3 Trade-offs, D4 Non-Functional Impact), an ADR MUST be authored in `docs/decisions/ADR-NNN-<slug>.md` and `.agents/skills/architecture/SKILL.md` must be read before implementation.
</NON_NEGOTIABLES>

<PROCEDURE>
## Data modeling

Design data structures based on real access patterns, operational requirements, and consistency boundaries:

### Relational / SQL (PostgreSQL, MySQL, SQLite)
- **Normalization**: Default to 3rd Normal Form (3NF) to eliminate anomalies and redundancy. Denormalize deliberately only when query profiling proves read performance bottlenecks.
- **Constraints**: Enforce integrity at the database layer using `NOT NULL`, `FOREIGN KEY` (with explicit `ON DELETE` rules), `UNIQUE`, and `CHECK` constraints.
- **Primary keys**: Use surrogate keys (`UUIDv7`, `BIGINT IDENTITY`) or natural keys with strong domain uniqueness. Prefer time-ordered IDs (`UUIDv7` or ULID) for high-insert tables to prevent B-tree fragmentation.

### Document & NoSQL (MongoDB, DynamoDB, Cassandra)
- **Access-pattern driven**: Design schemas to serve complete queries in single round trips.
- **Embedding vs Referencing**:
  - Embed child entities when they are tightly bounded, queried together, and updated atomically with the parent.
  - Reference when entities have independent lifecycles, unbounded growth, or many-to-many relationships.
- **Size boundaries**: Respect document size limits (e.g., 16MB in MongoDB, 400KB in DynamoDB). Never allow unbounded array growth inside a single document.

## Indexing strategy

Derive indexes from actual query shapes and frequency:

- **Equality, Sort, Range (ESR)**: Order compound index fields with equality predicates first, followed by sort attributes, and finally range filters.
- **Specialized indexes**:
  - Use GIN / GiST indexes (Postgres) or text indexes for full-text search and JSONB containment queries.
  - Use Partial / Filtered indexes (`WHERE is_active = true`) to index only relevant subsets, saving memory and write overhead.
  - Use Covering indexes (`INCLUDE` columns) to satisfy queries directly from index pages without table lookups.
- **Verification**: Verify index utilization using `EXPLAIN ANALYZE` (SQL) or `.explain("executionStats")` (NoSQL). Ensure hot-path queries perform index scans, never sequential/collection scans.
- **Cost discipline**: Avoid redundant or speculative indexes. Every index increases write latency and disk consumption.

## Query discipline

- Project only needed columns/fields; avoid `SELECT *` or unbounded document fetches.
- Paginate large result sets using cursor-based pagination (keyset) for high-churn tables; avoid large-offset pagination (`LIMIT 100 OFFSET 100000`).
- Use atomic updates (`UPDATE ... SET ... WHERE ...`, `$inc`, `$set`) for simple state transitions.
- Use read-only query optimizations where supported (e.g., `.as_no_tracking()` in EF Core, `.lean()` in Mongoose).

## Transactions and concurrency

- Choose the appropriate transaction isolation level (Read Committed, Repeatable Read, Serializable) based on consistency requirements.
- Use **Optimistic Concurrency Control** (version/timestamp checks) for low-contention updates to prevent lost updates.
- Keep transactions short: do not perform external HTTP calls, file I/O, or heavy hashing inside database transactions.
- Implement explicit retry logic with exponential backoff for transient deadlock/serialization failures.

## Zero-downtime migrations

When modifying schemas in production:

### Expand / Migrate / Contract pattern
1. **Expand**: Add new columns, tables, or collections without removing old structures. New columns must be nullable or have safe defaults. Application code begins dual-writing to both old and new formats.
2. **Migrate**: Backfill historical data in bounded, throttled batches to prevent table locks and replication lag.
3. **Contract**: Update application code to read solely from the new structure. After verification, remove the old column/table and clean up dual-write code.

### Safe migration rules
- Never rename a column or table in a single atomic release on live traffic.
- Create indexes concurrently (`CREATE INDEX CONCURRENTLY` in Postgres) to avoid locking tables against writes.
- Always prepare a verified rollback or forward-fix script before executing migrations.
- Test migrations against realistic data volumes in a staging environment.

## Connection management & operational health

- **Pool sizing**: Configure connection pool limits based on server resources, database server connection limits, and application concurrency.
- **Health probes**: Implement liveness/readiness database checks with strict timeouts (e.g., 2-5s) to avoid hanging processes during database failover.
- **High availability & caching**: Route read/write workloads according to active database capabilities (e.g., read replicas for relational databases, secondary reads for document stores, replica nodes for distributed caches).
- **Data retention & TTL**: Implement automatic TTL indexes, key expirations, or scheduled archival for ephemeral data (sessions, verification tokens, temporary caches).
</PROCEDURE>

<VERIFICATION_POLICY>
## Universal Database Verification

Verify database changes according to the active database technology profile:
- **Schema & Migration Verification**: Verify schema changes apply cleanly and rollback/forward scripts execute idempotently (SQL migrations, MongoDB collection validators, or DynamoDB table definitions).
- **Access Pattern & Query Verification**: Verify query performance using technology-appropriate tooling (e.g., `EXPLAIN (ANALYZE, BUFFERS)` in PostgreSQL, `explain("executionStats")` in MongoDB, consumed capacity checks in DynamoDB, `SLOWLOG` in Redis).
- **Integrity & Constraint Verification**: Test domain constraints (unique collisions, foreign keys, or document validation rules) on representative data volumes.
- **Concurrency & Atomicity Verification**: Test concurrent write operations, optimistic locking versions, or transaction boundaries under load.
- **Data Backfill Verification**: Verify backfill scripts execute idempotently in bounded batches without exhausting database memory or connection pools.

### Exit Criteria
Schema changes apply cleanly, queries execute within target latency budgets, and data integrity tests pass with zero regressions.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Schema definitions, migrations, indexes, and queries.
- Verified migration execution and query performance test evidence.
</DELIVERABLES>
