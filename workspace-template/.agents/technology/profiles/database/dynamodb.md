---
name: DynamoDB
category: database
baselineVersion: Current AWS API
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: Current AWS API (2026)
supportedVersions:
- Current AWS SDK v3
legacyVersions:
- AWS SDK v2
prohibitedVersions:
- AWS SDK v1
sources:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/
- https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/dynamodb/
---
# Amazon DynamoDB Technology Profile

## 1. Scope
Applies to cloud-native applications utilizing Amazon DynamoDB as a managed NoSQL database.

## 2. Detection Signals
- Dependencies: `"@aws-sdk/client-dynamodb"`, `"@aws-sdk/lib-dynamodb"`, `"boto3"`
- Files: CDK / Terraform DynamoDB resource definitions

## 3. Supported-Version Policy
- Primary Target: DynamoDB with AWS SDK v3 (JavaScript/TypeScript) or Boto3 (Python).

## 4. Core Architectural Guidance
- **Single-Table Design**: Model multiple entity types in a single table using generic partition key (`PK`) and sort key (`SK`) naming (e.g., `PK: USER#<id>`, `SK: PROFILE`).
- **Access Patterns Before Modeling**: Define 100% of read and write query patterns before designing primary keys and Global Secondary Indexes (GSIs).
- **Avoid Table Scans**: Never perform full table scans (`ScanCommand`) in production request loops. All reads must use `GetItem` or `Query` against `PK` with optional `SK` condition expressions.
- **Transactions & Concurrency**:
  - Use `TransactWriteItems` for multi-item ACID operations.
  - Use conditional writes (`attribute_exists`, `version = :current_ver`) for optimistic concurrency control.

## 5. Security & Performance Guidance
- **Hot Partition Defense**: Distribute partition keys evenly across the keyspace; avoid sequential or monolithic partition keys that concentrate traffic onto a single partition.
- **Item Size Limits**: Keep item sizes well below the 400 KB limit. Offload large payloads or binary blobs to Amazon S3.
- **IAM Least Privilege**: Restrict IAM policies to specific table and index ARNs with required actions (`GetItem`, `PutItem`, `Query`).

## 6. Testing Guidance
- Local Testing: Use DynamoDB Local (via Docker or LocalStack) for integration test suites.
- Query Verification: Verify queries return expected consumed capacity using `ReturnConsumedCapacity: 'TOTAL'`.

## 7. Common Anti-patterns
- Designing relational tables with foreign keys and attempting client-side joins in DynamoDB.
- Using `Scan` operations for filtering data instead of querying indexed partition keys.
- Allowing unbounded collection growth in partition keys leading to hot partitions.
- Storing large document blobs exceeding item size limits.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/
- AWS SDK v3 Documentation: https://docs.aws.amazon.com/AWSJavaScriptSDK/v3/latest/client/dynamodb/
- Local Inspection: Inspect table definitions in infrastructure-as-code files.
