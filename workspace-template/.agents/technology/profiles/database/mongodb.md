---
name: MongoDB
category: database
baselineVersion: 8.3 / 8.0 / 7.0
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: '8.0'
supportedVersions:
- '8.3'
- '8.0'
- '7.0'
legacyVersions:
- '6.0'
prohibitedVersions:
- < 6.0
sources:
- https://www.mongodb.com/docs/manual/
- https://mongoosejs.com/docs/
---
# MongoDB Technology Profile

```yaml
technology: mongodb
supported_versions:
  - "8.3"
  - "8.0"
  - "7.0"
preferred_version: "8.3"
verified_at: "2026-09-22"
sources:
  - url: https://www.mongodb.com/docs/manual/
    verified_at: "2026-09-22"
review_policy:
  max_age_days: 30
```

## 1. Scope
Applies to applications utilizing MongoDB as a primary document store or secondary database (via native MongoDB driver, Mongoose, PyMongo, or Motor).

## 2. Detection Signals
- Dependencies: `"mongodb"`, `"mongoose"` in `package.json`, `"pymongo"`, `"motor"` in Python
- Connection strings: `mongodb://`, `mongodb+srv://`

## 3. Supported-Version Policy
- Primary Target: MongoDB 8.3 (Current stable release line as of 2026) / 8.0+ / 7.0+.
- Baseline: MongoDB 6.0+.

## 4. Core Architectural Guidance
- **Access-Pattern-Driven Modeling**: Model documents based on read/write query patterns rather than normalized entities.
  - **Embed When**: Data is accessed together, has a 1:1 or bounded 1:N relationship (e.g., user addresses, order line items), and does not grow unboundedly.
  - **Reference When**: Data is accessed independently, has an unbounded 1:N or M:N relationship, or is updated frequently by multiple concurrent operations.
- **Index Strategy**:
  - Follow the Equality, Sort, Range (ESR) rule when designing compound indexes.
  - Avoid over-indexing: every index increases write amplification and working-set memory pressure.
- **Schema Validation**: Enforce document schemas via JSON Schema validation at the collection level or through strict Mongoose schemas.
- **Transactions & Concurrency**:
  - Prefer single-document atomic operations (`$set`, `$inc`, `$push`) for high throughput.
  - Use multi-document transactions only when cross-collection atomic consistency is mandatory.

## 5. Security & Performance Guidance
- **Connection Management**: In serverless environments, manage connection pool size to prevent exceeding Atlas connection limits.
- **Query Hardening**: Prevent NoSQL injection by sanitizing object inputs and disabling dangerous operators (`$where`).
- **Working Set Sizing**: Ensure indexes fit entirely within RAM to prevent disk paging.

## 6. Testing Guidance
- Integration Testing: Use `mongodb-memory-server` for fast, isolated in-memory testing or Docker containers.
- Query Verification: Validate queries using `explain("executionStats")` to verify index coverage (`IXSCAN` vs `COLLSCAN`).

## 7. Common Anti-patterns
- Unbounded array growth in single documents leading to 16MB BSON limit violations.
- Using MongoDB as a pure relational substitute with massive `$lookup` join chains on every query.
- Missing compound indexes on frequently filtered and sorted fields, causing in-memory sort buffer overflow.
- Using `$where` or JavaScript evaluation in queries, opening severe security and performance risks.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://www.mongodb.com/docs/manual/
- Mongoose Documentation: https://mongoosejs.com/docs/
- Local Inspection: Inspect Mongoose schema files and collection initialization scripts.
