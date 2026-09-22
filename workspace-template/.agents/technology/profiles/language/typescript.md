---
name: TypeScript
category: language
baselineVersion: 6.0 compatibility (5.7+ LTS)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 5.7+ LTS
supportedVersions:
- 6.0 compatibility
- 5.7+ LTS
- 5.6+
legacyVersions:
- '5.4'
- '5.5'
prohibitedVersions:
- < 5.0
sources:
- https://www.typescriptlang.org/docs
---
# TypeScript Language Profile

## 1. Scope
Applies to TypeScript projects across frontend, backend, full-stack, and library packages.

## 2. Detection Signals
- Files: `tsconfig.json`
- Dependencies: `"typescript"` in `package.json`
- File extensions: `.ts`, `.tsx`

## 3. Supported-Version Policy
- Primary Target: TypeScript 6.0 compatibility (with 5.7+ LTS baseline).
- Enforce strict compilation flags in `tsconfig.json`: `"strict": true`, `"noImplicitAny": true`, `"strictNullChecks": true`.
- Use the compiler version declared in `package.json`.

## 4. Documentation Sources
- Official: https://www.typescriptlang.org/docs

## 5. Core Architectural Guidance
- **Strict Mode Discipline**: Prohibit `any` in application code. Use `unknown` for unvalidated inputs and narrow with type guards or runtime schema validators.
- **Type vs. Value Boundaries**:
  - Types disappear at runtime. Always validate external runtime data (HTTP request bodies, query params, environment variables, external API responses) with schema libraries (Zod, ArkType, Valibot).
  - Use `type` for unions, intersections, primitives, and utility types; use `interface` for extensible object contracts and public API surfaces.
- **Generics & Type Constraints**:
  - Constrain generics explicitly (`<T extends Record<string, unknown>>`) rather than using bare `<T>`.
  - Use utility types (`Pick`, `Omit`, `Partial`, `Readonly`, `ReturnType`) instead of duplicating type declarations.
- **Type-Safe Error Handling**: Use structured Result types (`Result<T, E>`) or strongly typed error envelopes rather than throwing untyped errors.
- **Immutability**: Use `readonly` properties and `as const` assertions for fixed lookup tables and configuration dictionaries.

## 6. Security Guidance
- Never cast untrusted external data using `as Type` (type assertion bypasses compiler safety). Validate with schemas first.
- Use branded types / nominal typing for sensitive primitives (e.g. `UserId`, `EmailAddress`, `HashedPassword`) to prevent accidental argument transposition.
- Keep compiler options `noUncheckedIndexedAccess: true` to prevent undefined property access bugs.

## 7. Performance Guidance
- Enable `incremental: true` and define `tsBuildInfoFile` in `tsconfig.json` for fast rebuilds.
- Use `import type` for type-only imports to allow compilers (Babel, SWC, esbuild) to cleanly erase types and prevent circular module dependency issues.
- Avoid deeply nested conditional recursive types that slow down compiler type checking.

## 8. Testing Guidance
- Unit Tests: Vitest or Jest with `@swc/jest` or `ts-jest`.
- Type-Level Testing: Use `expect-type` or `tsd` when authoring reusable utility types or public library contracts.

## 9. Common Anti-Patterns
- Using `any` or `// @ts-ignore` to suppress type errors instead of resolving the underlying type mismatch.
- Asserting types on untrusted input (`req.body as User`) without runtime validation.
- Overusing non-null assertions (`!`) on optional or nullable values.
- Duplicating interface properties instead of composing or picking from existing types.

## 10. Verification Commands
- Typecheck: `npx tsc --noEmit` or `npm run typecheck`
- Lint: `npm run lint` or `npx eslint .`
