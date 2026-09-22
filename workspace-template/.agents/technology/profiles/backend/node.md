---
name: Node.js
category: backend
baselineVersion: 22 / 24 LTS, 26 Current
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 22.x LTS
supportedVersions:
- 22.x LTS
- 24.x LTS
- 26.x Current
legacyVersions:
- 20.x
prohibitedVersions:
- < 20.x
sources:
- https://nodejs.org/docs/latest/api/
---
# Node.js Technology Profile

## 1. Scope
Applies to backend applications, REST/GraphQL services, workers, and CLI tools running on Node.js (Active and Maintenance LTS lines: Node 22.x, 24.x, and Current line 26.x).

## 2. Detection Signals
- Files: `package.json`, `.nvmrc`, `.node-version`
- Dependencies: Node-specific packages (`express`, `fastify`, `ioredis`, etc.)

## 3. Supported-Version Policy
- Primary Target: Active and Maintenance LTS releases (Node 22.x LTS, Node 24.x LTS).
- Forward Compatibility: Node 26.x (Current).
- Production Rule: Applications must run on Active or Maintenance LTS (Node 22+, Node 24+); Node 20 and earlier releases have reached End-of-Life (EOL) and are prohibited for new production deployments.
- Detect declared version from `.nvmrc`, `.node-version`, or `package.json:engines.node`.

## 4. Documentation Sources
- Official: https://nodejs.org/docs/latest/api/

## 5. Core Architectural Guidance
- **Mandatory Layered Separation (RULE-ARCH-LAYER-001)**:
  - All Node.js backend services—whether built with lightweight frameworks, raw `node:http`, or message consumers—must enforce strict separation of concerns:
    - **Transport / Entrypoint**: Route bindings, HTTP servers (`node:http`), WebSocket servers, or queue consumers (`node:events`). Contains zero business rules and zero database queries.
    - **Controllers / Adapters**: Adapt network requests to typed parameters, invoke domain services, and format network responses.
    - **Domain Services**: Pure business logic and workflow orchestration with zero transport dependencies.
    - **Repositories / Persistence**: Encapsulate all database queries, query builders, and database drivers (MongoDB, PostgreSQL, SQLite).
- **Event Loop Protection**:
  - The main JavaScript thread must remain unblocked. Offload CPU-intensive operations (cryptographic hashing, image compression, large JSON transformations) to Worker Threads (`node:worker_threads`) or child processes.
- **Async I/O & Promises**:
  - Use `async`/`await` consistently with native promise-based APIs: `node:fs/promises`, `node:stream/promises`, `node:timers/promises`.
  - Always handle promise rejections: register process-level listeners (`unhandledRejection`, `uncaughtException`) that log error details and trigger graceful termination.
- **Graceful Shutdown**:
  - Listen for `SIGTERM` and `SIGINT` signals.
  - Stop accepting incoming HTTP requests, wait for ongoing requests to drain with a timeout (e.g. 15-30s), close database connection pools, and exit with code 0.
- **Context Propagation & Tracing**:
  - Use `node:async_hooks:AsyncLocalStorage` to propagate request correlation IDs, tenant contexts, and user identities across asynchronous call chains.

## 6. Security Guidance
- Audit dependencies using `npm audit`, `pnpm audit`, or `yarn audit` in CI/CD pipelines.
- Enforce strict timeouts on all external network requests using `AbortSignal.timeout(ms)`.
- Secure process execution: avoid `child_process.exec` with string concatenation; prefer `child_process.execFile` or `spawn` with argument arrays.
- Configure secure HTTP headers (via Helmet or equivalent) and enforce body size limits to prevent DoS.

## 7. Performance Guidance
- Stream large files or HTTP response bodies rather than buffering entire payloads into memory (`node:stream` or Web Streams).
- Connection Pooling: Size database pools to match Node concurrency and database server connection limits.
- Diagnostics: Utilize Node's built-in diagnostic reports (`--report-on-fatalerror`) and heap profiling for memory leak investigations.

## 8. Testing Guidance
- Unit & Integration: Vitest, Jest, or Node's native test runner (`node --test`).
- HTTP Mocking: `msw` (Mock Service Worker) or `nock` for mocking external HTTP services.

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Queries in HTTP Handlers / Utility Files
```javascript
// ❌ FORBIDDEN: Raw server callback querying database directly
import http from 'node:http';
import { db } from './db.js';

http.createServer(async (req, res) => {
  // VIOLATION: Database query directly in transport server listener
  const users = await db.query('SELECT * FROM users');
  res.writeHead(200, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify(users));
});
```

### FORBIDDEN: Inline Business Logic in Event Emitters / Sockets
```javascript
// ❌ FORBIDDEN: Inline DB mutation inside event listener
socket.on('message', async (data) => {
  await UserModel.updateOne({ id: data.userId }, { lastSeen: new Date() }); // VIOLATION!
});
```

- Using synchronous file operations (`fs.readFileSync`, `fs.writeFileSync`) in request handlers.
- Forgetting to attach error handlers to EventEmitters or stream pipelines, causing silent process crashes.
- Storing request-scoped state in global variables or module-level singletons.
- Swallowing unhandled rejections without logging or exiting.

## 10. Verification Commands
- Check Node version: `node -v`
- Lint: `npm run lint` or `npx eslint .`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Test: `npm test` or `node --test`
- Start / Build: `npm run build --if-present && npm start`

## 11. Standard Layered Code Blueprint

```typescript
// 1. Domain Types & DTO (src/dtos/account.dto.ts)
import { z } from 'zod';

export const DepositSchema = z.object({
  accountId: z.string().uuid(),
  amount: z.number().positive(),
});
export type DepositDto = z.infer<typeof DepositSchema>;

// 2. Repository Interface & Implementation (src/repositories/account.repository.ts)
export interface IAccountRepository {
  findById(id: string): Promise<AccountRecord | null>;
  updateBalance(id: string, newBalance: number): Promise<void>;
}

export class AccountRepository implements IAccountRepository {
  constructor(private readonly pool: PgPool) {}

  async findById(id: string): Promise<AccountRecord | null> {
    const res = await this.pool.query('SELECT * FROM accounts WHERE id = $1', [id]);
    return res.rows[0] || null;
  }

  async updateBalance(id: string, newBalance: number): Promise<void> {
    await this.pool.query('UPDATE accounts SET balance = $1 WHERE id = $2', [newBalance, id]);
  }
}

// 3. Domain Service (src/services/account.service.ts) - Pure logic, no HTTP/transport
export class AccountService {
  constructor(private readonly repo: IAccountRepository) {}

  async deposit(dto: DepositDto): Promise<{ balance: number }> {
    const account = await this.repo.findById(dto.accountId);
    if (!account) throw new NotFoundError('Account not found');
    const newBalance = account.balance + dto.amount;
    await this.repo.updateBalance(dto.accountId, newBalance);
    return { balance: newBalance };
  }
}
```
