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

The structure below is the profile's preferred boundary pattern. Follow the project's accepted architecture and ADRs when they intentionally use a different valid structure.
- **Preferred Boundary Structure (RULE-ARCH-LAYER-001)**:
  - **Routes (`src/routes/`)**: Declarative schema definitions (TypeBox, JSON Schema) and route registrations only. Direct database operations inside route definitions or options are STRICTLY FORBIDDEN.
  - **Handlers / Controllers (`src/controllers/`)**: Thin adapter functions extracting `request.body` / `request.params` and returning results from domain services.
  - **Domain Services (`src/services/`)**: Transport-agnostic business logic. Passing Fastify `FastifyRequest` or `FastifyReply` into services is STRICTLY FORBIDDEN.
  - **Repositories (`src/repositories/`)**: Encapsulate all database interaction and query building.
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

## 7. Common Anti-patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Queries in Route Handlers
```typescript
// ❌ FORBIDDEN: Executing database queries directly in Fastify route handler
fastify.post('/items', async (request, reply) => {
  const item = await db.insertInto('items').values(request.body).execute(); // VIOLATION!
  return item;
});
```

### FORBIDDEN: Passing Reply or Request to Service Layer
```typescript
// ❌ FORBIDDEN: Leaking Fastify transport objects into services
class ItemService {
  async createItem(reply: FastifyReply, data: ItemDto) { // VIOLATION!
    reply.header('x-custom', '123');
  }
}
```

- Overriding Fastify's encapsulated scope by unnecessarily wrapping all plugins in `fastify-plugin`.
- Mixing `return data` and `reply.send(data)` in async handlers, leading to double-send errors.
- Omitting response schemas on high-throughput endpoints, reverting Fastify to slow `JSON.stringify`.
- Using Express middleware via `@fastify/express` for features natively supported by Fastify hooks.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://fastify.dev/docs/latest/
- Local Inspection: Inspect `node_modules/fastify/package.json` and TypeScript declaration files.

## 9. Standard Layered Code Blueprint

```typescript
// 1. DTO / Schema (src/dtos/item.schema.ts)
import { Type, Static } from '@sinclair/typebox';

export const CreateItemSchema = Type.Object({
  title: Type.String({ minLength: 1 }),
  price: Type.Number({ minimum: 0 }),
});
export type CreateItemDto = Static<typeof CreateItemSchema>;

export const ItemResponseSchema = Type.Object({
  id: Type.String(),
  title: Type.String(),
  price: Type.Number(),
});

// 2. Repository Layer (src/repositories/item.repository.ts)
export interface IItemRepository {
  create(data: CreateItemDto): Promise<ItemEntity>;
}
export class ItemRepository implements IItemRepository {
  constructor(private readonly db: DatabaseClient) {}
  async create(data: CreateItemDto): Promise<ItemEntity> {
    return this.db.item.create({ data });
  }
}

// 3. Domain Service Layer (src/services/item.service.ts)
export class ItemService {
  constructor(private readonly repo: IItemRepository) {}
  async createItem(dto: CreateItemDto): Promise<ItemEntity> {
    return this.repo.create(dto);
  }
}

// 4. Controller Adapter (src/controllers/item.controller.ts)
export class ItemController {
  constructor(private readonly service: ItemService) {}
  create = async (request: FastifyRequest<{ Body: CreateItemDto }>, reply: FastifyReply) => {
    const item = await this.service.createItem(request.body);
    reply.status(201);
    return item;
  };
}

// 5. Route Wiring (src/routes/item.routes.ts)
export async function itemRoutes(fastify: FastifyInstance, opts: { controller: ItemController }) {
  fastify.post('/items', {
    schema: {
      body: CreateItemSchema,
      response: { 201: ItemResponseSchema },
    },
    handler: opts.controller.create,
  });
}
```
