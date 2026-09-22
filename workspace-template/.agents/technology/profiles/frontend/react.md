---
name: React
category: frontend
baselineVersion: 19.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 19.x
supportedVersions:
- 19.x
- '18.3'
legacyVersions:
- '18.2'
prohibitedVersions:
- < 18.0
sources:
- https://react.dev
---
# React Technology Profile

```yaml
technology: react
supported_versions:
  - "19.x"
  - "18.x"
preferred_version: "19.x"
verified_at: "2026-09-22"
sources:
  - url: https://react.dev
    verified_at: "2026-09-22"
review_policy:
  max_age_days: 30
```

## 1. Scope
Applies to applications and libraries built with React (primarily React 18.x and 19.x).

## 2. Detection Signals
- Dependencies: `"react"`, `"react-dom"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: React 19.x (Current stable line).
- Backward Compatibility: React 18.x (transition and suspense features).
- Note on Framework APIs: Underlying React Server Components (RSC) and bundler integration layers do not follow standard semver expectations; adhere strictly to the hosting framework's version-pinned specifications.
- Use the version declared in `package.json`.

## 4. Documentation Sources
- Official: https://react.dev

## 5. Core Architectural Guidance
- **Functional Components & Hooks**: Pure functional components with explicit, predictable state hooks.
- **State Locality**: Keep state as close to where it is used as possible. Lift state only when multiple components need to synchronize.
- **React 19 Actions & Transitions**:
  - Use `useTransition` and `useActionState` for pending states and error handling during async operations.
  - Use `useOptimistic` for instant UI feedback with automatic rollback on mutation failure.
  - Direct ref forwarding: pass `ref` directly as a component prop in React 19 without `forwardRef`.
  - Use the `use()` hook for reading promises and context conditionally in render.
- **Server Components & Server Functions**:
  - Distinguish Server Components (rendered on server, zero client bundle footprint) from Client Components (`'use client'`).
  - Use Server Functions / Server Actions for secure data mutations without custom API route scaffolding.
- **Effect Discipline**: Avoid using `useEffect` for data transformation or synchronizing state with props. Use effects only for external synchronization (DOM manipulation, event listeners, external subscriptions).

## 6. Security Guidance
- Prevent XSS: Avoid `dangerouslySetInnerHTML`. If necessary, sanitize with a trusted library (DOMPurify).
- Validate all user-supplied URLs passed to `href` or `src` attributes to block `javascript:` pseudo-protocols.

## 7. Performance Guidance
- Prefer compiler-driven optimization when enabled; avoid speculative memoization; use manual memoization (`useMemo`, `useCallback`) only when profiling or framework constraints justify it.
- Keep component renders pure and side-effect free.
- Split code at route or feature boundaries using `React.lazy` and `Suspense`.

## 8. Testing Guidance
- Test user-visible behavior using `@testing-library/react`.
- Avoid testing internal component state, private variables, or hook implementation details.

## 9. Common Anti-Patterns
- Using `useEffect` to fetch data without handling cancellation / cleanup, leading to race conditions.
- Mutating state directly instead of using functional state setters or immutable data patterns.
- Prop drilling through >3 layers when composition or context is more appropriate.

## 10. Verification Commands
- Typecheck: `npx tsc --noEmit`
- Tests: `npm test` or `npx vitest`
