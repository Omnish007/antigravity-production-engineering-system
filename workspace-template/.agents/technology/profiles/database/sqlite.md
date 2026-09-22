---
name: SQLite
category: database
baselineVersion: 3.45+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 3.45+
supportedVersions:
- 3.45+
- 3.40+
legacyVersions:
- 3.35+
prohibitedVersions:
- < 3.35
sources:
- https://www.sqlite.org/docs.html
---
# SQLite Technology Profile

## 1. Scope
Applies to embedded, mobile, CLI, desktop, and single-instance server applications utilizing SQLite (via `better-sqlite3`, `sqlite3`, `rusqlite`, Python `sqlite3`, etc.).

## 2. Detection Signals
- Dependencies: `"better-sqlite3"`, `"sqlite3"`, `"rusqlite"`
- Files: `*.sqlite`, `*.sqlite3`, `*.db`

## 3. Supported-Version Policy
- Primary Target: SQLite 3.35+ (supports `RETURNING`, UPSERT, and window functions).
- Engine Mode: Always configure Write-Ahead Logging (`WAL`) mode.

## 4. Documentation Sources
- Official: https://www.sqlite.org/docs.html

## 5. Core Architectural Guidance
- **WAL Mode Configuration**:
  - Always enable Write-Ahead Logging on database initialization: `PRAGMA journal_mode = WAL;`.
  - WAL mode permits unlimited concurrent readers while a write is occurring.
- **Concurrency & Busy Timeouts**:
  - SQLite enforces single-writer concurrency (one active write transaction at a time).
  - Always configure a busy timeout on connection initialization: `PRAGMA busy_timeout = 5000;`. This causes concurrent writers to wait for locks up to 5 seconds rather than immediately failing with `SQLITE_BUSY`.
  - Keep write transactions short and focused; avoid performing network I/O or heavy hashing inside write transactions.
- **Foreign Key Constraints**:
  - SQLite disables foreign key enforcement by default for backward compatibility. Always execute `PRAGMA foreign_keys = ON;` on every opened connection.
- **Synchronous Mode**:
  - In WAL mode, set `PRAGMA synchronous = NORMAL;` for high throughput while maintaining crash durability.

## 6. Security Guidance
- Parameterized Queries: Always use parameterized queries or prepared statements; string interpolation in SQL is strictly forbidden.
- Filesystem Permissions: Restrict database file and directory permissions (`chmod 0600` on the `.db` file; `chmod 0700` on the parent directory).
- Safe Backups: Use the SQLite Online Backup API or `VACUUM INTO 'backup.db'` to take atomic snapshots without locking live traffic.

## 7. Performance Guidance
- Prepared Statements: Cache and reuse prepared statements (`db.prepare(...)`) for repeated queries to eliminate query parsing overhead.
- Batch Transactions: Wrap bulk inserts and updates in an explicit transaction (`BEGIN ... COMMIT`); executing thousands of inserts in autocommit mode causes disk write amplification.
- Indexing: Create indexes on foreign key columns and columns frequently used in `WHERE`, `JOIN`, and `ORDER BY` clauses.

## 8. Testing Guidance
- In-Memory Testing: Use in-memory SQLite (`:memory:`) for fast, isolated unit test execution.
- Migration Tests: Test migration scripts against real file-based SQLite databases to verify schema upgrades and data preservation.

## 9. Common Anti-Patterns
- Forgetting to execute `PRAGMA foreign_keys = ON;`, allowing orphan records.
- Running in default `DELETE` journal mode instead of `WAL` mode.
- Accessing SQLite from multiple processes without configuring `busy_timeout`.
- Performing heavy multi-record inserts without an enclosing transaction.

## 10. Verification Commands
- Integrity Check: `sqlite3 <db-file> "PRAGMA integrity_check;"`
- Foreign Key Check: `sqlite3 <db-file> "PRAGMA foreign_key_check;"`
