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

## 4. Core Architectural Guidance
- **Mandatory Layered Separation (RULE-ARCH-LAYER-001)**:
  - **Page Views (`+page.svelte`)**: UI presentation and user events only. Direct `fetch()` calls or database imports in `.svelte` files are STRICTLY FORBIDDEN.
  - **Server Load & Form Actions (`+page.server.ts`)**: Server-side data loading and mutations. Must validate input with schemas (Zod) and invoke domain services.
  - **API Endpoints (`+server.ts`)**: Thin JSON transport adapters. Must delegate immediately to domain services; direct database querying in `+server.ts` is FORBIDDEN.
  - **Domain Services & Repositories (`src/lib/server/`)**: Pure business logic and database access isolated from transport.
- **Svelte 5 Runes**:
  - Use `$state()` for reactive variables, objects, and arrays.
  - Use `$derived()` for computed reactive expressions.
  - Use `$effect()` only for side-effects synchronizing with external DOM or browser APIs; never use `$effect()` to mutate reactive state.
  - Use `$props()` to declare component inputs with strict TypeScript typing.
- **Form Actions**:
  - Use SvelteKit Form Actions (`export const actions = { ... }`) for progressive enhancement, server-side validation, and native HTML form submissions with automatic client-side invalidation.
- **State Colocation**:
  - Keep state as close to where it is used as possible. For shared cross-component state, create reactive classes using `$state()` in `.svelte.ts` modules.

## 5. Security Guidance
- Secret Management: Access environment variables through `$env/static/private` or `$env/dynamic/private`; never expose private secrets in `$env/static/public`.
- CSRF Defense: SvelteKit includes built-in origin checks for form actions; do not disable `csrf: { checkOrigin: true }`.
- XSS Prevention: Sanitize any untrusted HTML before rendering with `{@html}`.

## 6. Performance Guidance
- Adapter Selection: Choose the appropriate adapter (`@sveltejs/adapter-node`, `@sveltejs/adapter-auto`, `@sveltejs/adapter-static`) for the deployment target.
- Prefetching: Use `data-sveltekit-preload-data="hover"` on navigation links for instant page transitions.
- Image Optimization: Use `@sveltejs/enhanced-img` for automated image transformations and WebP/AVIF generation.

## 7. Testing Guidance
- Unit & Component: Vitest with `@testing-library/svelte`.
- E2E: Playwright testing against the production-built application.

## 8. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Access or Raw Fetch in Svelte Views
```svelte
<!-- ❌ FORBIDDEN: Direct fetch inside UI component script -->
<script lang="ts">
  let items = $state([]);
  async function loadItems() {
    // VIOLATION: Calling raw API directly in UI rather than using page server data or action
    const res = await fetch('/api/items');
    items = await res.json();
  }
</script>
```

- Using legacy Svelte 3/4 syntax (`let count = 0; $: doubled = count * 2;`) in Svelte 5 projects.
- Mutating `$state()` directly inside `$effect()`, creating infinite update loops.
- Accessing browser globals (`window`, `localStorage`) during SSR without checking `browser` from `$app/environment`.

## 9. Verification Commands
- Typecheck: `npx svelte-check`
- Lint: `npm run lint` or `npx eslint .`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Test: `npm test` or `npx vitest run`
- Build: `npm run build`

## 10. Standard Layered Code Blueprint

```typescript
// 1. Domain Service (src/lib/server/services/note.service.ts)
import { noteRepository } from '$lib/server/repositories/note.repository';

export async function createNote(userId: string, content: string) {
  if (!content.trim()) throw new Error('Content cannot be empty');
  return noteRepository.save({ userId, content });
}

// 2. Server Form Action (src/routes/notes/+page.server.ts)
import { fail } from '@sveltejs/kit';
import { z } from 'zod';
import { createNote } from '$lib/server/services/note.service';
import type { Actions, PageServerLoad } from './$types';

const NoteSchema = z.object({ content: z.string().min(1) });

export const actions: Actions = {
  default: async ({ request, locals }) => {
    const data = Object.fromEntries(await request.formData());
    const parsed = NoteSchema.safeParse(data);
    if (!parsed.success) return fail(400, { error: 'Invalid content' });

    await createNote(locals.userId, parsed.data.content);
    return { success: true };
  },
};

// 3. UI Component (src/routes/notes/+page.svelte)
<script lang="ts">
  import { enhance } from '$app/forms';
  let { form } = $props();
</script>

{#if form?.error}
  <p class="error">{form.error}</p>
{/if}

<form method="POST" use:enhance>
  <textarea name="content" required></textarea>
  <button type="submit">Add Note</button>
</form>
```
