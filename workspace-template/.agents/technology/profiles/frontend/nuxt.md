---
name: Nuxt
category: frontend
baselineVersion: 4.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 4.x
supportedVersions:
- 4.x
- 3.x
legacyVersions:
- 3.x
prohibitedVersions:
- < 3.0
sources:
- https://nuxt.com/docs
---
# Nuxt Technology Profile

## 1. Scope
Applies to full-stack, SSR, SSG, and hybrid applications built with Nuxt (Nuxt 4.x active line, with support for legacy Nuxt 3.x).

## 2. Detection Signals
- Files: `nuxt.config.ts`, `nuxt.config.js`
- Dependencies: `"nuxt"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: Nuxt 4.x (Current active line).
- Backward Compatibility: Nuxt 3.x (Note: Nuxt 3 reached EOL on July 31, 2026; maintain legacy compatibility without forcing breaking migrations unless explicitly requested).
- Use the version declared in `package.json`.

## 4. Documentation Sources
- Official: https://nuxt.com/docs

## 5. Core Architectural Guidance
- **Mandatory Layered Separation (RULE-ARCH-LAYER-001)**:
  - Enforce the full-stack architectural pipeline:
    `pages/` & `components/` ──> `composables/` ──> `server/api/` (Nitro) ──> `server/services/` ──> `server/repositories/`
  - **Frontend UI (`pages/`, `components/`)**: Visual layout and state binding. Raw fetch calls directly in setup are FORBIDDEN; use composables and `useFetch()` wrappers.
  - **Composables (`composables/`)**: Auto-imported UI state and domain interaction logic.
  - **Nitro Route Handlers (`server/api/`)**: Thin HTTP endpoints. Validate input via Zod and invoke `server/services/`. Direct database queries or ORM calls in Nitro route handlers are FORBIDDEN.
  - **Server Services & Repositories (`server/services/`, `server/repositories/`)**: Encapsulated business logic and database persistence.
- **Data Fetching**:
  - Use `useFetch()` or `useAsyncData()` with explicit, stable keys for isomorphic, SSR-friendly data loading.
  - Never call raw `fetch()` directly in top-level setup scripts, which causes dual execution and hydration mismatch.
- **State Management**:
  - Use `useState()` for SSR-friendly, cross-request isolated reactive state.
  - Use Pinia (`@pinia/nuxt`) when complex domain stores with actions and getters are required.
- **Server Engine (Nitro)**:
  - Implement API endpoints with `defineEventHandler()`.
  - Validate request bodies and query parameters with runtime validators (Zod) inside Nitro handlers.

## 6. Security Guidance
- Distinguish `runtimeConfig.public` from private `runtimeConfig`: never expose API keys, database credentials, or server secrets in `public`.
- Validate and sanitize all parameters in Nitro endpoints to prevent SSRF and injection.
- Configure secure session cookies with `httpOnly`, `sameSite: 'lax'`, and `secure: true`.

## 7. Performance Guidance
- Leverage Nuxt **Route Rules** in `nuxt.config.ts` for hybrid rendering:
  - `prerender: true` for static marketing pages;
  - `swr: 3600` (Stale-While-Revalidate) for cacheable dynamic content;
  - `ssr: false` for client-only dashboard portals.
- Use `@nuxt/image` (`<NuxtImg />`) for automated responsive images and WebP/AVIF compression.
- Lazy-load heavy components using the `Lazy` prefix (e.g. `<LazyModalDialog />`).

## 8. Testing Guidance
- Unit & Component: Vitest with `@nuxt/test-utils/runtime`.
- E2E: Playwright testing against the production-built Nitro server (`npx nuxi build && node .output/server/index.mjs`).

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Access in Nitro Route Handlers
```typescript
// ❌ FORBIDDEN: Direct DB call in server/api handler
// server/api/users.post.ts
export default defineEventHandler(async (event) => {
  const body = await readBody(event);
  const user = await prisma.user.create({ data: body }); // VIOLATION: Service layer bypassed!
  return user;
});
```

- Using `ref()` or `reactive()` at module scope outside `setup()`, leading to cross-request state pollution across users.
- Accessing browser globals (`window`, `document`, `localStorage`) during SSR without checking `import.meta.client` or `<ClientOnly>`.
- Forgetting keys in `useAsyncData()`, causing stale data across route transitions.

## 10. Verification Commands
- Typecheck: `npx nuxi typecheck`
- Lint: `npm run lint` or `npx eslint .`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Test: `npm test` or `npx vitest run`
- Build: `npx nuxi build`

## 11. Standard Layered Code Blueprint

```typescript
// 1. Server Service (server/services/user.service.ts)
import { userRepository } from '../repositories/user.repository';
import type { CreateUserDto } from '~/types/user';

export async function registerUser(dto: CreateUserDto) {
  const existing = await userRepository.findByEmail(dto.email);
  if (existing) throw createError({ statusCode: 409, message: 'Email registered' });
  return userRepository.create(dto);
}

// 2. Nitro API Route (server/api/users.post.ts) - Thin adapter
import { z } from 'zod';
import { registerUser } from '../services/user.service';

const UserSchema = z.object({ email: z.string().email(), name: z.string().min(2) });

export default defineEventHandler(async (event) => {
  const body = await readValidatedBody(event, (b) => UserSchema.parse(b));
  return registerUser(body);
});

// 3. Composable (composables/useUsers.ts)
export function useUsers() {
  const { data: users, pending, error, refresh } = useFetch('/api/users', { key: 'users-list' });
  return { users, pending, error, refresh };
}
```
