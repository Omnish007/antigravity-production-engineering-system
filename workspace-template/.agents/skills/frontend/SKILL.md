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

- Use `next/image` or the framework-provided image component.
- Serve modern formats (WebP, AVIF) with fallbacks.
- Set explicit `width` and `height` or use `fill` with proper aspect ratios to prevent CLS.
- Lazy-load below-the-fold images (the default behavior for `next/image`).
- For the LCP image, use `<Image preload />` (Next.js 16+) to inject a `<link rel="preload">` and set `fetchPriority="high"` automatically. The older `priority` prop is deprecated in Next.js 16.
- Do not preload multiple images on the same page; only the confirmed LCP candidate should be preloaded.
- Use `loading="eager"` when an above-the-fold image must render immediately but is not the LCP element.

### Font optimization

- Use `next/font` or equivalent to self-host fonts and eliminate render-blocking requests.
- Apply `font-display: swap` or `optional` to prevent invisible text.
- Subset fonts to include only the character sets needed.

### Prefetching and resource hints

- Use framework-provided link prefetching for likely navigation targets.
- Avoid prefetching everything; prioritize high-probability user paths.
- Use `fetchPriority="high"` on critical resources and `fetchPriority="low"` on deferrable ones where the browser API supports it.
- Always verify resource hint behavior against the installed framework version; these APIs evolve across major releases.

### State management

- Prefer Server Components for data that does not require client interactivity.
- Use the project's chosen client-state library consistently; do not introduce competing solutions.
- Colocate state with the component that owns it; lift only when siblings or parents genuinely need the value.
- Avoid global client state for server-derivable data.

### Responsive design

- Design mobile-first using the project's responsive utilities.
- Test layouts at standard breakpoints and between breakpoints.
- Use relative units and fluid typography where appropriate.
- Ensure touch targets meet minimum size requirements (48x48 CSS pixels).

## Verification

Run type-check, lint, relevant unit/integration tests, and E2E for critical changed flows where configured. Validate loading/error/empty states, responsive layouts, and keyboard operation.

## Version sensitivity

Next.js APIs (image props, caching, routing, metadata, server actions) change across major versions. Always verify behavior against the installed version's documentation before making consequential changes. Record version-specific conventions in `docs/CONVENTIONS.md` when they differ from defaults.
