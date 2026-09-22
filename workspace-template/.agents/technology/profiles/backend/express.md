---
name: Express
category: backend
baselineVersion: 5.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 5.x
supportedVersions:
- 5.x
- 4.x
legacyVersions:
- 4.x
prohibitedVersions:
- < 4.x
sources:
- https://expressjs.com/en/5x/api.html
---
# Express.js Technology Profile

## 1. Scope
Applies to HTTP services, REST APIs, and backend microservices built with Express.js (Express 5.x and Express 4.x).

## 2. Detection Signals
- Dependencies: `"express"` in `package.json`
- Entrypoints: `app.listen`, `express()`, `routes/`, `controllers/`

## 3. Supported-Version Policy
- Primary Target: Express 5.x (native Promise handling in route handlers and middleware).
- Compatibility Target: Express 4.x (wrap async route handlers with an async boundary/error wrapper to catch unhandled rejections).

## 4. Core Architectural Guidance
- **Layered Architecture**:
  - **Routes**: Define HTTP paths, methods, and attach validation/auth middleware.
  - **Controllers**: Parse request params/body, invoke service layer, and return HTTP responses.
  - **Services**: Pure business logic, independent of Express `req`/`res` objects.
  - **Repositories / Data Access**: Encapsulate database queries and transactions.
- **Middleware Ordering**:
  1. Security headers (`helmet`)
  2. CORS configuration (`cors`)
  3. Body parsing (`express.json({ limit: '1mb' })`)
  4. Request logging & correlation IDs
  5. Authentication & rate limiting
  6. Domain routes
  7. 404 Not Found handler
  8. Centralized error handling middleware `(err, req, res, next)` with exactly 4 parameters.

## 5. Security & Performance Guidance
- **Security Headers**: Always configure `helmet` for secure HTTP headers (HSTS, CSP, X-Frame-Options).
- **Abuse Controls**: Apply rate limiting (`express-rate-limit`) to authentication and mutating endpoints.
- **Input Validation**: Validate `req.body`, `req.query`, and `req.params` with Zod or Joi schemas before processing.
- **Process Protection**: Handle `uncaughtException` and `unhandledRejection` with graceful process termination.

## 6. Testing Guidance
- Integration Testing: Use `supertest` against the Express `app` instance without binding to a live network port.
- Unit Testing: Test service and domain functions in isolation with mocked repositories.
- Verification: `npm test` and `npm run lint`.

## 7. Common Anti-patterns
- Omitting the `next` parameter in 4-argument error handling middleware, causing Express to treat it as standard middleware.
- Missing `await` or unhandled promise rejections in Express 4.x route handlers, causing server hangs.
- Putting database queries or business logic directly inside route handler callbacks.
- Storing request-scoped state on global variables or Express application instances.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://expressjs.com/en/5x/api.html
- Local Inspection: Inspect `node_modules/express/package.json` for installed version.
