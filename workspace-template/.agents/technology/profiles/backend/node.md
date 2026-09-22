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

## 9. Common Anti-Patterns
- Using synchronous file operations (`fs.readFileSync`, `fs.writeFileSync`) in request handlers.
- Forgetting to attach error handlers to EventEmitters or stream pipelines, causing silent process crashes.
- Storing request-scoped state in global variables or module-level singletons.
- Swallowing unhandled rejections without logging or exiting.

## 10. Verification Commands
- Check Node version: `node -v`
- Lint: `npm run lint` or `npx eslint .`
- Test: `npm test` or `node --test`
- Start / Build: `npm run build --if-present && npm start`
