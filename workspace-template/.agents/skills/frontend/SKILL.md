---
name: frontend
id: SKILL-FRONTEND-001
description: Implement modern, accessible, high-performance frontend interfaces across any framework (React, Next.js, Vue, Nuxt, SvelteKit, Angular, Mobile, or SSR) with strict component boundaries, resilient data flow, and performance optimization.
---

# Frontend Development Skill

<MISSION>
Implement modern, accessible, high-performance frontend interfaces across any framework (React, Next.js, Vue, Nuxt, SvelteKit, Angular, Mobile, or SSR) with strict component boundaries, resilient data flow, and performance optimization.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring frontend capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- For governed execution, the canonical task record `.agents/state/tasks/TASK-ID.json` must exist.
- Use the lifecycle state defined in `.agents/orchestration/task-lifecycle.md` for the current phase; do not require `IN_PROGRESS` merely because the skill is available during execution.
- Implementation-phase mutations require a `TASK_STARTED` event before code/configuration changes. Planning, requirements, analysis, review, verification, and memory-sync phases may legitimately run in their own lifecycle states.
    - Must consult `.agents/state/stack.json` and load the matching profile from `.agents/technology/profiles/frontend/` (e.g. `react.md`, `nextjs.md`, `vue.md`, `nuxt.md`, `angular.md`, `sveltekit.md`).
    - Must be loaded as part of the Atomic Frontend Bundle alongside `.agents/skills/uiux/SKILL.md` and `.agents/rules/06-uiux.md`.

### Pre-flight Checklist
- [ ] Active frontend profile loaded from `.agents/technology/profiles/frontend/`
    - [ ] Loading and error boundaries active
    - [ ] Client bundle audited for secrets
    - [ ] Responsive design verified
    - [ ] Accessibility landmarks present
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Strict adherence to RULE-ARCH-LAYER-001 (15-layered-architecture.md). Frontend code MUST follow: `UI Component -> Custom Hook / Composable / State -> API Service -> HTTP Client`.
- Direct `fetch()` or `axios()` calls inside UI component rendering bodies, lifecycle hooks, or button handlers are STRICTLY FORBIDDEN. Always route requests through dedicated API services and custom hooks.
- Provide explicit UI states for loading, error, empty, and data on every async view.
- Never expose API keys, database secrets, or private tokens in client bundles.
- Ensure responsive layout supporting desktop, tablet, and mobile viewports.
</NON_NEGOTIABLES>

<PROCEDURE>
## Component architecture

- **Component separation**: Separate presentational components (pure, reusable UI primitives) from container/view components (stateful, data-fetching, orchestrating).
- **Composition**: Prefer composition over deep inheritance or monolithic components. Break large views into small, focused child components.
- **Props contract**: Define explicit, strongly-typed props/interfaces for every component. Props should specify what data or callbacks the component needs, not implementation trivia.

## Client-server boundaries

- **Server rendering (SSR / SSG / Server Components)**:
  - Default to server-rendered components for data-fetching, SEO-critical content, and non-interactive views where supported by the framework (e.g., Next.js, Nuxt, SvelteKit).
  - Keep sensitive operations, backend secrets, and heavy data transformations on the server.
- **Client rendering**:
  - Confine client components to sub-trees that require browser events, local state, interactive animations, or browser-only APIs (e.g., `localStorage`, WebSockets, Canvas).
  - Keep the boundary between server and client as narrow and deep in the component tree as possible.

## Data flow and state management

Prefer the standard data flow:
```text
UI Component -> Typed API Client -> HTTP/gRPC Endpoint -> Server
```

- **Server state vs Client state**: Use dedicated query/cache libraries (e.g., TanStack Query, SWR, Apollo) for server-derived state rather than storing server data in global client stores.
- **State colocation**: Keep state as close to where it is used as possible. Lift state only when multiple siblings or parents genuinely require it.
- **Centralized endpoint registry**: Maintain an explicit, centralized API client/registry module. Do not hardcode endpoint URLs directly inside UI components.

## Forms and user input

- **Schema validation**: Use runtime schema validators (Zod, Yup, Valibot, or framework equivalents) to validate inputs on the client for immediate user feedback.
- **Dual validation**: Always validate again on the server; never rely on client validation for security or data integrity.
- **UX states**: Explicitly manage `idle`, `submitting`, `success`, and `error` states.
- **Error display**: Place field-specific error messages adjacent to the relevant input; associate inputs with error text via `aria-describedby`.
- **Submission safety**: Disable submission buttons while a request is in flight to prevent duplicate submissions; re-enable on failure.

## Performance and Web Vitals

Target Core Web Vitals at the 75th percentile (LCP ≤ 2.5s, INP ≤ 200ms, CLS ≤ 0.1):

### Bundle optimization
- Implement route-based code splitting and dynamic imports for heavy, infrequently used components.
- Tree-shake unused exports and audit bundle sizes before major releases.

### Assets & images
- Serve modern image formats (WebP, AVIF) with appropriate fallback formats.
- Specify explicit `width` and `height` or aspect ratios on image elements to eliminate Cumulative Layout Shift (CLS).
- Lazy-load below-the-fold images by default.
- Preload only the single confirmed Largest Contentful Paint (LCP) candidate using `<link rel="preload">` or high-priority resource hints.

### Fonts
- Self-host web fonts to prevent third-party network blocking.
- Apply `font-display: swap` or `optional` to prevent invisible text during load.
- Subset fonts to the specific character sets required.

### Prefetching
- Prefetch assets and data for high-probability navigation routes.
- Avoid aggressive over-fetching that consumes mobile data budgets.

## Resilience and error handling

- **Error boundaries**: Wrap major UI sections, layouts, and route segments in error boundaries.
- **Fallback UI**: Provide actionable, user-friendly fallback interfaces with retry capabilities rather than leaving blank screens or unhandled white-screen crashes.
- **Optimistic UI**: When implementing optimistic updates, ensure safe rollback and clear user notification if the server mutation fails.

## Accessibility (a11y)

- Target WCAG 2.2 AA compliance across all views.
- Use semantic HTML elements (`<nav>`, `<main>`, `<button>`, `<dialog>`) before introducing ARIA attributes.
- Ensure all interactive controls are fully operable via keyboard with visible focus indicators.
- Provide accessible labels (`aria-label`, `aria-labelledby`) for icon-only buttons.
- Manage focus correctly when opening and closing dialogs, drawers, and menus.
</PROCEDURE>

<VERIFICATION_POLICY>
## Verification

Before considering frontend work complete:
- Verify type correctness (`tsc`, `vue-tsc`, etc.);
- Run unit/integration tests for components with complex state or interactions;
- Perform automated accessibility scanning (axe-core or equivalent);
- Test responsive layouts at mobile (<640px), tablet (640-1024px), and desktop (>1024px) viewports;
- Verify keyboard navigation and screen-reader compatibility for interactive controls.

### Exit Criteria
Frontend builds cleanly and passes component/UI tests.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Implemented and verified UI components with responsive layouts, error boundaries, and accessibility compliance.
- Passing frontend test suite and clean production build.
</DELIVERABLES>
