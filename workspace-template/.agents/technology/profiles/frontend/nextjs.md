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
- **App Router Default**: Organize routes under `app/` using layout hierarchies (`layout.tsx`, `page.tsx`, `loading.tsx`, `error.tsx`, `not-found.tsx`).
- **Server vs. Client Component Boundaries**:
  - Default to React Server Components (RSC) for data fetching, backend access, and SEO.
  - Use `'use client'` only at the leaves of the component tree for interactivity, state (`useState`, `useReducer`), browser APIs, or event handlers.
- **Server Actions**: Use Server Actions (`'use server'`) for mutations, form submissions, and RPCs. Enforce strict server-side validation (e.g. Zod) and authorization within every server action.
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

## 9. Common Anti-Patterns
- Adding `'use client'` at the top of page/layout files instead of isolating interactive components.
- Storing private tokens or secrets in Client Components.
- Swallowing errors in `error.tsx` without logging error digests.
- Assuming `fetch` is automatically cached in Next.js 15+.
- Running `next lint` on Next.js 16 (command removed; use direct linter scripts).

## 10. Verification Commands
- Typecheck: `npx tsc --noEmit` or `npm run typecheck`
- Lint: `npm run lint` or `npx eslint .` / `npx biome check .` (Note: `next lint` was removed in Next.js 16)
- Test: `npm test` or `npx vitest run` / `npx playwright test`
- Build: `npx next build` or `npm run build`
