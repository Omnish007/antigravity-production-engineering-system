---
name: JavaScript
category: language
baselineVersion: ES2024+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: ES2024+
supportedVersions:
- ES2024+
- ES2023
- ES2022
legacyVersions:
- ES2020
prohibitedVersions:
- < ES2020
sources:
- https://developer.mozilla.org/en-US/docs/Web/JavaScript
---
# JavaScript Language Profile

## 1. Scope
Applies to modern JavaScript projects across Node.js, browsers, and edge runtimes (ES2022+ / ESM).

## 2. Detection Signals
- Files: `package.json`, `.js`, `.mjs`, `.cjs` without `tsconfig.json`
- `"type": "module"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: Modern ECMAScript (ES2022+) with native ES Modules.
- Use native ESM (`import`/`export`) by declaring `"type": "module"` in `package.json`.
- Avoid legacy CommonJS (`require`/`module.exports`) in new codebases unless interfacing with legacy dependencies.

## 4. Documentation Sources
- Official: https://developer.mozilla.org/en-US/docs/Web/JavaScript

## 5. Core Architectural Guidance
- **Native ES Modules**: Use `import` and `export` exclusively. Ensure relative imports include file extensions when required by the runtime.
- **Async Programming**: Prefer `async`/`await` over Promise chaining (`.then().catch()`). Always handle rejections or allow them to propagate to top-level handlers.
- **Defensive Operations**:
  - Use optional chaining (`?.`) and nullish coalescing (`??`) for safe property access.
  - Use `structuredClone()` for deep object copying rather than JSON serialization hacks.
- **Immutable State Patterns**:
  - Use object/array spread (`...`) and non-mutating array methods (`map`, `filter`, `toSorted`, `toReversed`, `toSpliced`).
  - Use `Object.freeze()` for immutable configuration objects.

## 6. Security Guidance
- **Prototype Pollution Defense**: Use `Object.create(null)` or native `Map` for user-keyed dictionaries; avoid recursive deep merges into plain objects without key sanitization (`__proto__`, `constructor`).
- **Code Injection Prevention**: Prohibit `eval()`, `new Function()`, and string arguments in `setTimeout`/`setInterval`.
- **Constant-Time Comparison**: Use `crypto.timingSafeEqual()` for comparing cryptographic hashes, signatures, and tokens.

## 7. Performance Guidance
- Clean up resources: remove event listeners, cancel timers, and abort ongoing fetches using `AbortController`.
- Prefer `Set` and `Map` for $O(1)$ lookups instead of repeated array `includes()` or `find()` on large datasets.
- Use streams (`ReadableStream`, `node:stream/promises`) for large data payloads to keep memory usage bounded.

## 8. Testing Guidance
- Unit Tests: Node.js built-in test runner (`node --test`) or Vitest.
- Coverage: Native Node test coverage (`node --test --experimental-test-coverage`) or `c8`.

## 9. Common Anti-Patterns
- Inconsistently mixing CommonJS (`require`) and ESM (`import`) in the same project.
- Using loose equality (`==`) instead of strict equality (`===`).
- Mutating arrays in place (`sort()`, `splice()`) when pure transformations were intended.
- Leaving unhandled promise rejections that crash Node.js processes.

## 10. Verification Commands
- Lint: `npm run lint` or `npx eslint .` / `npx biome check .`
- Test: `npm test` or `node --test`
