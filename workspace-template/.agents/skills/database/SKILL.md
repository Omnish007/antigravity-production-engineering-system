---
name: database
description: Design MongoDB and Mongoose data models, validation, indexes, queries, and migrations with correctness and performance in mind.
---

# Database Engineering Skill

## Modeling

Design from actual access patterns, not from abstract normalization alone. Decide deliberately which data is embedded versus referenced.

Consider:

- read/write patterns;
- document growth;
- ownership boundaries;
- transaction needs;
- archival/retention;
- query frequency/selectivity;
- future scaling.

## Validation

Use application-level request validation at the API boundary and Mongoose/schema validation for persistence invariants. Where an established collection requires stronger guardrails, consider MongoDB schema validation as an additional boundary.

## Indexes

Derive indexes from real query shapes. For compound indexes, use the ESR guideline as a starting point: equality fields first, then sort or selective range based on the actual query behavior. Validate with explain/query plans where performance matters.

Do not add indexes speculatively; every index adds write/storage/maintenance cost.

## Query discipline

- project only needed fields;
- paginate large result sets;
- avoid unbounded array growth;
- avoid accidental collection scans on hot paths;
- use `lean()` for read-only Mongoose queries when document methods/virtual behavior are not needed;
- prefer atomic updates for simple state transitions;
- use transactions when multiple writes must commit atomically and the deployment supports the required guarantees.

## Data safety

- treat migrations/backfills as high-risk;
- make migrations idempotent when practical;
- define rollback or forward-fix strategy before production execution;
- never run destructive data operations against production without approval and a verified safety plan.

## Limits

Remember MongoDB's BSON document size limit and avoid indexed arrays whose growth is effectively unbounded.

## Connection management

- Configure connection pool size based on actual application concurrency and deployment topology.
- Monitor connection utilization, checkout latency, and pool exhaustion.
- Use connection pool events for observability.
- Close connections gracefully during application shutdown.

## Read preferences and replicas

When using replica sets:

- use `primary` reads for write-then-read consistency;
- use `secondaryPreferred` for read-heavy workloads where slight staleness is acceptable;
- use `nearest` for latency-sensitive, geo-distributed reads;
- document the read preference strategy in conventions when it affects application behavior.

## Change streams

For real-time data observation:

- use change streams instead of polling when reactive behavior is needed;
- handle resume tokens for reliable change stream consumption;
- filter change streams to the minimum required scope;
- implement error handling and reconnection for stream interruptions.

## Sharding awareness

When the project uses or plans to use sharded collections:

- choose shard keys based on query patterns and write distribution;
- avoid scatter-gather queries that hit all shards;
- design schemas that allow shard-key-based query routing;
- understand the limitations of transactions across shards.

## TTL and data lifecycle

- Use TTL indexes for automatic expiration of time-limited data (sessions, temporary tokens, audit logs with retention policies).
- Document retention policies and TTL configuration.
- Verify TTL behavior in test environments before production deployment.

## Verification

Test schema invariants, indexes, query behavior, duplicate/conflict paths, and data migration outcomes. Use representative data volumes for performance-sensitive work.
