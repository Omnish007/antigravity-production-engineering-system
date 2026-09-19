---
name: frontend
description: Implement Next.js 16 and React 19 frontend behavior using Server Components by default, strong TypeScript, Tailwind CSS, and shadcn/ui.
---

# Frontend Development Skill

## Next.js / React model

- Use App Router for new work unless the project says otherwise.
- Prefer Server Components by default for static/data-oriented UI.
- Use Client Components only where browser interactivity, state, event handlers, effects, or browser APIs require them.
- Keep client boundaries as small as practical.
- Treat caching, revalidation, params/searchParams APIs, and rendering behavior as version-sensitive; read installed Next.js docs before consequential changes.

## Data flow

Prefer:

```text
UI -> typed client/service boundary -> API -> application/service -> persistence
```

When a Next.js Server Component can safely fetch server-side data without unnecessary browser round trips, prefer the server path. For highly interactive client-side server state, use the project's chosen query/data library if one exists; do not introduce a new state library casually.

## Components

Use feature-oriented composition. Keep reusable primitives separate from domain-specific components. Props should describe behavior, not implementation details.

## Forms

- schema-validate user input;
- provide client-side UX validation;
- always enforce the contract again on the server;
- expose field-level and form-level errors;
- handle pending, disabled, success, and failure states.

## API endpoints

Centralize frontend endpoint paths in the project-adopted endpoint registry/module. Do not scatter URL strings through components. Keep the base URL/environment configuration separate from endpoint path definitions.

## Accessibility

Prefer semantic HTML and shadcn primitives. Verify keyboard behavior, focus management, accessible names, error association, and dialog/menu behavior.

## Performance

Minimize client JavaScript, avoid unnecessary re-renders, optimize images/fonts, defer non-critical work, and investigate Core Web Vitals when performance matters.

### Error boundaries

Wrap major UI sections in error boundaries to prevent a single component failure from crashing the entire page. Provide user-friendly fallback UI that explains the error and offers recovery actions.

### Streaming and Suspense

Use React Suspense boundaries with streaming SSR where the framework supports it. Show meaningful loading states for deferred content rather than blank areas.

### Image optimization

- Use `next/image` or equivalent framework-provided image component.
- Serve modern formats (WebP, AVIF) with fallbacks.
- Set explicit `width` and `height` or use `fill` with proper aspect ratios to prevent CLS.
- Lazy-load below-the-fold images.
- Preload hero/LCP images.

### Font optimization

- Use `next/font` or equivalent to self-host fonts and eliminate render-blocking requests.
- Apply `font-display: swap` or `optional` to prevent invisible text.
- Subset fonts to include only the character sets needed.

### Prefetching

- Use framework-provided link prefetching for likely navigation targets.
- Avoid prefetching everything; prioritize high-probability user paths.
- Use `priority` hints for critical resources.

## Verification

Run type-check, lint, relevant unit/integration tests, and E2E for critical changed flows where configured. Validate loading/error/empty states, responsive layouts, and keyboard operation.
