---
name: SvelteKit
category: frontend
baselineVersion: 2.x / Svelte 5
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 2.x (Svelte 5 Runes)
supportedVersions:
- SvelteKit 2.x / Svelte 5
- Svelte 4 compatibility
legacyVersions:
- Svelte 4
prohibitedVersions:
- < Svelte 4
sources:
- https://svelte.dev/docs/kit/
---
# Svelte & SvelteKit Technology Profile

## 1. Scope
Applies to reactive web applications, SPAs, and full-stack SSR applications built with Svelte 5 and SvelteKit.

## 2. Detection Signals
- Files: `svelte.config.js`
- Dependencies: `"@sveltejs/kit"`, `"svelte"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: Svelte 5 (Runes architecture) and modern SvelteKit.
- Backward Compatibility: Maintain existing conventions in Svelte 4 codebases without forcing breaking migrations unless explicitly requested.

## 4. Documentation Sources
- Official: https://svelte.dev/docs/kit/

## 5. Core Architectural Guidance
- **Svelte 5 Runes**:
  - Use `$state()` for reactive variables, objects, and arrays.
  - Use `$derived()` for computed reactive expressions.
  - Use `$effect()` only for side-effects synchronizing with external DOM or browser APIs; never use `$effect()` to mutate reactive state.
  - Use `$props()` to declare component inputs with strict TypeScript typing.
- **Routing & Loading**:
  - `+page.svelte` for page UI views.
  - `+page.server.ts` for server-only `load` functions and form actions.
  - `+server.ts` for standalone API endpoints.
  - `+layout.svelte` for shared layout shells.
- **Form Actions**:
  - Use SvelteKit Form Actions (`export const actions = { ... }`) for progressive enhancement, server-side validation, and native HTML form submissions with automatic client-side invalidation.
- **State Colocation**:
  - Keep state as close to where it is used as possible. For shared cross-component state, create reactive classes using `$state()` in `.svelte.ts` modules.

## 6. Security Guidance
- Secret Management: Access environment variables through `$env/static/private` or `$env/dynamic/private`; never expose private secrets in `$env/static/public`.
- CSRF Defense: SvelteKit includes built-in origin checks for form actions; do not disable `csrf: { checkOrigin: true }`.
- XSS Prevention: Sanitize any untrusted HTML before rendering with `{@html}`.

## 7. Performance Guidance
- Adapter Selection: Choose the appropriate adapter (`@sveltejs/adapter-node`, `@sveltejs/adapter-auto`, `@sveltejs/adapter-static`) for the deployment target.
- Prefetching: Use `data-sveltekit-preload-data="hover"` on navigation links for instant page transitions.
- Image Optimization: Use `@sveltejs/enhanced-img` for automated image transformations and WebP/AVIF generation.

## 8. Testing Guidance
- Unit & Component: Vitest with `@testing-library/svelte`.
- E2E: Playwright testing against the production-built application.

## 9. Common Anti-Patterns
- Using legacy Svelte 3/4 syntax (`let count = 0; $: doubled = count * 2;`) in Svelte 5 projects.
- Mutating `$state()` directly inside `$effect()`, creating infinite update loops.
- Accessing browser globals (`window`, `localStorage`) during SSR without checking `browser` from `$app/environment`.
- Calling external mutations via client `fetch` instead of utilizing SvelteKit Form Actions.

## 10. Verification Commands
- Typecheck: `npx svelte-check`
- Lint: `npm run lint` or `npx eslint .`
- Test: `npm test` or `npx vitest run`
- Build: `npm run build`
