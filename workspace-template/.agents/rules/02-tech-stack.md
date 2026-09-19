# Technology Stack Rules

Recommended activation: **Always On**

## Baseline stack

Primary default stack for new projects:

- Next.js 16.x baseline for the current major line
- React 19.x baseline for the current major line
- TypeScript
- Tailwind CSS 4.x baseline
- shadcn/ui
- Node.js
- Express 5.x baseline
- MongoDB
- Mongoose when ODM behavior is useful

Use the latest stable patch/minor release compatible with the project's constraints. Do not silently upgrade major versions inside an existing project.

## Version policy

For every version-sensitive change:

1. Inspect `package.json` and lockfile.
2. Inspect the installed version where feasible.
3. Read the matching official documentation.
4. Check breaking changes and migration notes.
5. Update dependent packages coherently.
6. Run targeted and broad verification appropriate to the change.
7. Record a superseding ADR when a major-version upgrade materially changes architecture or behavior.

## Framework policy

- Use Next.js App Router for new applications unless a documented constraint requires otherwise.
- Prefer React Server Components by default in Next.js when the feature does not need browser-only state, effects, event handlers, or client APIs.
- Use Client Components only when the component needs interactivity or client-only capabilities.
- Treat Next.js caching behavior as version-sensitive. Verify against the installed version instead of relying on memory.
- For Next.js work, prefer installed version-matched docs in `node_modules/next/dist/docs/` when available.

## Stack deviations

A project may deviate for a concrete reason. Record the reason in an ADR when it affects architecture, operations, security, cost, or long-term maintenance.
