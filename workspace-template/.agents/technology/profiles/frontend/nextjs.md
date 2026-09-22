---
name: Next.js
category: frontend
baselineVersion: 16.3+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 16.3+
supportedVersions:
- 16.x
- 15.x
legacyVersions:
- 14.x
prohibitedVersions:
- < 14.x
sources:
- https://nextjs.org/docs
---
# Next.js Technology Profile

## 1. Scope
Applies to applications built with Next.js (primarily Next.js 15.x and 16.x App Router architecture).

## 2. Detection Signals
- Files: `next.config.js`, `next.config.mjs`, `next.config.ts`
- Dependencies: `"next"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: Next.js 16.x (Active LTS line; requires Node.js 20.9+).
- Backward Compatibility: Next.js 15.x App Router (requires Node.js 18.18+ or 20+).
- Use the version actually installed or declared in `package.json`.
- Inspect version-matched documentation shipped with the package: `node_modules/next/dist/docs/` when available before remote search.
- Never silently upgrade major versions without an explicit migration plan.

## 4. Documentation Sources
- **Local Documentation Primacy**: Inspect version-matched documentation shipped with the package: `node_modules/next/dist/docs/` when available.
- Official: https://nextjs.org/docs

## 5. Core Architectural Guidance
- **Next.js App Router Layering (RULE-ARCH-LAYER-001)**:
  - **Route Handlers (`app/api/.../route.ts`)**: Thin HTTP transport handlers. Must validate request body using Zod schemas and delegate immediately to domain services. Direct database queries, Prisma calls, or Mongoose operations inside route files are STRICTLY FORBIDDEN.
  - **Server Actions (`actions/`)**: RPC endpoints for client mutations (`'use server'`). Validate input using Zod, enforce authorization, invoke domain services, and return serializable DTOs. Direct database queries or raw SQL inside Server Actions without service encapsulation are FORBIDDEN.
  - **Server Components (`app/**/page.tsx`, `layout.tsx`)**: Read-only rendering shells. Fetch data via dedicated data access services (`services/data/`), never embed ad-hoc fetch strings or raw queries directly in JSX.
  - **Client Components (`'use client'`)**: Presentation and interaction only. Must NOT access databases, ORM models, or private secrets. Delegate server mutations and data fetching to custom hooks (`useFeature()`) and typed API services.
- **Server vs. Client Component Boundaries**:
  - Default to React Server Components (RSC) for data fetching, backend access, and SEO.
  - Use `'use client'` only at the leaves of the component tree for interactivity, state (`useState`, `useReducer`), browser APIs, or event handlers.
- **Data Fetching & Caching**:
  - Leverage `fetch` cache semantics or React `cache()` for deduplication.
  - In Next.js 15/16, `fetch` requests are no longer cached by default (`no-store` default); explicitly specify cache options where caching is desired.
  - Dynamically accessed headers (`cookies()`, `headers()`) opt the route into dynamic rendering.

## 6. Security Guidance
- Treat Server Actions as public HTTP endpoints: always authenticate the caller and sanitize inputs.
- Keep environment secrets out of client bundles: never prefix private keys with `NEXT_PUBLIC_`.
- Validate URLs passed to redirects or external probers to prevent SSRF.

## 7. Performance Guidance
- Use `next/image` (`<Image />`) for automated responsive sizing, WebP/AVIF formatting, and CLS prevention.
- Use `next/font` for zero-layout-shift local font hosting.
- Optimize client bundle size with dynamic imports (`next/dynamic`) for heavy interactive components.

## 8. Testing Guidance
- Unit/Component: Vitest or Jest with `@testing-library/react`.
- E2E: Playwright testing against production builds (`next build && next start`).

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Queries in Route Handlers or Client Components
```typescript
// ❌ FORBIDDEN: Direct Prisma/DB call inside route handler
// app/api/users/route.ts
export async function POST(req: Request) {
  const body = await req.json();
  const user = await prisma.user.create({ data: body }); // VIOLATION!
  return NextResponse.json(user);
}
```

### FORBIDDEN: Direct Network Fetch inside JSX Component Bodies
```typescript
// ❌ FORBIDDEN: Ad-hoc fetch directly inside component rendering logic
'use client';
export function UserProfile({ id }: { id: string }) {
  useEffect(() => {
    fetch(`/api/users/${id}`).then(r => r.json()); // VIOLATION: Use custom hook + API service!
  }, [id]);
}
```

- Adding `'use client'` at the top of page/layout files instead of isolating interactive components.
- Storing private tokens or secrets in Client Components.
- Swallowing errors in `error.tsx` without logging error digests.
- Assuming `fetch` is automatically cached in Next.js 15+.

## 10. Verification Commands
- Typecheck: `npx tsc --noEmit` or `npm run typecheck`
- Lint: `npm run lint` or `npx eslint .` / `npx biome check .`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Test: `npm test` or `npx vitest run` / `npx playwright test`
- Build: `npx next build` or `npm run build`

## 11. Standard Layered Code Blueprint

```typescript
// 1. DTO / Schema (dtos/project.dto.ts)
import { z } from 'zod';
export const CreateProjectSchema = z.object({
  title: z.string().min(3),
  description: z.string().optional(),
});
export type CreateProjectDto = z.infer<typeof CreateProjectSchema>;

// 2. Data Service Layer (services/project.service.ts) - Encapsulates persistence
import { projectRepository } from '@/repositories/project.repository';

export async function createProject(userId: string, dto: CreateProjectDto) {
  return projectRepository.create({ ...dto, ownerId: userId });
}

// 3. Server Action (actions/project.actions.ts) - Validates and invokes service
'use server';
import { CreateProjectSchema } from '@/dtos/project.dto';
import { createProject } from '@/services/project.service';
import { getSession } from '@/lib/auth';

export async function createProjectAction(rawInput: unknown) {
  const session = await getSession();
  if (!session) throw new Error('Unauthorized');
  const validated = CreateProjectSchema.parse(rawInput);
  return createProject(session.user.id, validated);
}

// 4. Client Hook & UI Component (components/project-form.tsx)
'use client';
import { useTransition } from 'react';
import { createProjectAction } from '@/actions/project.actions';

export function ProjectForm() {
  const [isPending, startTransition] = useTransition();

  const handleSubmit = (formData: FormData) => {
    startTransition(async () => {
      await createProjectAction({ title: formData.get('title') });
    });
  };

  return (
    <form action={handleSubmit}>
      <input name="title" required disabled={isPending} />
      <button type="submit" disabled={isPending}>Create</button>
    </form>
  );
}
```
