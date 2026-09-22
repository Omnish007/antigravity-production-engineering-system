---
name: Redis
category: database
baselineVersion: 8.10 (7.4 compatibility)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: '8.10'
supportedVersions:
- '8.10'
- '7.4'
- 7.2 LTS
legacyVersions:
- '7.0'
prohibitedVersions:
- < 7.0
sources:
- https://redis.io/docs/
---
# Redis Technology Profile

## 1. Scope
Applies to applications utilizing Redis for caching, session storage, rate limiting, pub/sub messaging, queues, and distributed locking.

## 2. Detection Signals
- Dependencies: `"ioredis"`, `"redis"`, `"redis-py"`
- Services: `redis-server`

## 3. Supported-Version Policy
- Primary Target: Redis 8.10 (with 7.4 compatibility).

## 4. Documentation Sources
- Official: https://redis.io/docs/

## 5. Core Architectural Guidance
- **Structured Key Namespacing**:
  - Use colon-delimited key names following the pattern: `<domain>:<entity>:<id>:<attribute>` (e.g. `auth:session:usr_123:token`, `ratelimit:ip:192.168.1.1`).
- **TTL Discipline**:
  - Every cache key MUST have an explicit Time-To-Live (TTL via `EXPIRE` or `SET ... EX <seconds>`).
  - Keys without TTLs must be reserved strictly for persistent state (e.g. stream offsets) and audited regularly.
- **Appropriate Data Structure Selection**:
  - **Strings**: Simple values, serialized JSON, counters (`INCR`), and locks.
  - **Hashes**: Objects with multiple fields where individual fields need atomic reads/updates (`HSET`, `HGET`).
  - **Sets**: Unique collections, tagging, and set operations (`SADD`, `SISMEMBER`, `SINTER`).
  - **Sorted Sets (ZSet)**: Leaderboards, sliding-window rate limiters, priority queues (`ZADD`, `ZRANGEBYSCORE`).
  - **Streams**: Durable event streams and consumer groups (`XADD`, `XREADGROUP`).
- **Atomic Operations & Lua Scripts**:
  - Use atomic primitives (`MSET`, `HINCRBY`, `SET ... NX EX`) or Lua scripts (`EVALSHA`) for multi-step mutations to prevent race conditions.
- **Cache-Aside Pattern**:
  - Read from cache $	o$ on miss, read from database $	o$ write to cache with TTL $	o$ invalidate cache on database mutation.

## 6. Security Guidance
- Network Isolation: Bind Redis to `127.0.0.1` or private VPC subnets; never expose Redis directly to the public internet.
- Access Control: Use Redis ACLs with dedicated user accounts and least-privilege command permissions.
- Disable Dangerous Commands: Rename or disable destructive commands in production (`FLUSHALL`, `FLUSHDB`, `CONFIG`, `KEYS`).
- Encryption in Transit: Enforce TLS for all remote or cloud-hosted Redis connections.

## 7. Performance Guidance
- Prohibit `KEYS *`: Never use `KEYS` in production (it blocks the single-threaded server). Use `SCAN` with cursor iteration.
- Memory & Eviction: Configure `maxmemory` and an appropriate eviction policy (`volatile-lru`, `allkeys-lru`, or `volatile-ttl`).
- Pipelining: Pipeline commands (`pipeline()`) to batch multiple commands into a single network round-trip.

## 8. Testing Guidance
- Integration Testing: Use Testcontainers (`redis:7-alpine`) for realistic integration tests.
- Unit Testing: Use mock/in-memory drivers (`fakeredis` in Python, `ioredis-mock` in Node.js) for isolated unit tests.

## 9. Common Anti-Patterns
- Storing keys without TTLs, eventually exhausting server memory.
- Executing `KEYS *` in application request paths.
- Storing massive multi-megabyte payloads in a single string key.
- Implementing non-atomic distributed locks that fail to release on crash.

## 10. Verification Commands
- Ping Check: `redis-cli ping`
- Memory & Stats: `redis-cli info memory`
