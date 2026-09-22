---
name: Fastify
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
- https://fastify.dev/docs/latest/
---
# Fastify Technology Profile

## 1. Scope
Applies to high-performance Node.js HTTP services and microservices built with Fastify.

## 2. Detection Signals
- Dependencies: `"fastify"` in `package.json`
- Configuration/Plugins: `fastify-plugin`, `fastify.register`

## 3. Supported-Version Policy
- Primary Target: Fastify 4.x / 5.x.
- Node.js Runtime: Node.js 20+ LTS.

## 4. Core Architectural Guidance
- **Plugin Encapsulation**: Use `fastify-plugin` (`fp`) for plugins meant to be shared across sibling scopes; maintain clean encapsulation boundaries for domain modules.
- **Schema Validation & Serialization**: Define JSON schemas for request validation (`params`, `body`, `querystring`) and response serialization (`response[200]`). Fastify compiles schemas using `fast-json-stringify` for maximum throughput.
- **Lifecycle Hooks**: Use appropriate hooks (`onRequest`, `preParsing`, `preValidation`, `preHandler`, `onResponse`, `onError`) rather than generic middleware.
- **Asynchronous Handlers**: Write route handlers as `async (request, reply) => { return data; }` rather than calling `reply.send()`.

## 5. Security & Performance Guidance
- **Security Headers**: Register `@fastify/helmet` and `@fastify/cors`.
- **Rate Limiting**: Apply `@fastify/rate-limit` to public and mutating routes.
- **Serialization Performance**: Always declare response schemas for hot endpoints to leverage `fast-json-stringify` compilation.
- **Logging**: Use built-in Pino logger (`fastify({ logger: true })`) with correlation IDs.

## 6. Testing Guidance
- In-memory Testing: Use `app.inject()` for fast, port-free HTTP integration testing.
- Unit Testing: Test plugins and service functions in isolation with Vitest or Node Test Runner.
- Verification: `npm test` and `npm run lint`.

## 7. Common Anti-patterns
- Overriding Fastify's encapsulated scope by unnecessarily wrapping all plugins in `fastify-plugin`.
- Mixing `return data` and `reply.send(data)` in async handlers, leading to double-send errors.
- Omitting response schemas on high-throughput endpoints, reverting Fastify to slow `JSON.stringify`.
- Using Express middleware via `@fastify/express` for features natively supported by Fastify hooks.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://fastify.dev/docs/latest/
- Local Inspection: Inspect `node_modules/fastify/package.json` and TypeScript declaration files.
