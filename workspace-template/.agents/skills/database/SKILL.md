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

## Verification

Test schema invariants, indexes, query behavior, duplicate/conflict paths, and data migration outcomes. Use representative data volumes for performance-sensitive work.
