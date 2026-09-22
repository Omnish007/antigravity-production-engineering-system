---
name: Vue
category: frontend
baselineVersion: 3.5+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 3.5+
supportedVersions:
- 3.5+
- 3.4+
legacyVersions:
- '2.7'
prohibitedVersions:
- < 2.7
sources:
- https://vuejs.org/guide/introduction.html
- https://pinia.vuejs.org
---
# Vue.js Technology Profile

## 1. Scope
Applies to client-side single-page applications, components, and full-stack frontends built with Vue.js (primarily Vue 3.x with Composition API and `<script setup>`).

## 2. Detection Signals
- Dependencies: `"vue"` in `package.json`
- Configuration files: `vite.config.js`, `vite.config.ts`, `vue.config.js`
- File extensions: `**/*.vue`

## 3. Supported-Version Policy
- Primary Target: Vue 3.x (Composition API and `<script setup>` default).
- For legacy Vue 2.x projects, recognize Options API and Vuex patterns, but recommend migration to Vue 3 and Pinia.

## 4. Core Architectural Guidance
- **Composition API & `<script setup>`**: Author components using `<script setup lang="ts">`.
- **Reactivity Model**:
  - Use `ref()` for primitive values and object references.
  - Use `reactive()` only for tightly coupled state objects; prefer `ref()` for consistency across composables.
  - Use `computed()` for derived state; computed getters must be pure and side-effect free.
  - Use `watchEffect()` or `watch()` with explicit dependencies for side effects.
- **Composables**: Extract reusable stateful logic into composable functions (`useFeature()`) with explicit parameter and return types.
- **State Management**: Use Pinia for cross-component shared state with typed actions and getters.

## 5. Security & Performance Guidance
- **XSS Prevention**: Avoid `v-html` with untrusted user input; sanitize with DOMPurify if HTML rendering is required.
- **Shallow Reactivity**: Use `shallowRef()` or `shallowReactive()` for large read-only data structures or external third-party instances (e.g., Chart.js, Leaflet, Three.js).
- **Async Components**: Use `defineAsyncComponent()` for route-level or heavy dialog components to optimize bundle splitting.

## 6. Testing Guidance
- Unit and Component Testing: Vitest with `@vue/test-utils` and `@testing-library/vue`.
- Type Checking: `vue-tsc --noEmit`.
- Linting: `eslint --ext .vue,.js,.ts src`.

## 7. Common Anti-patterns
- Using Options API in greenfield Vue 3 projects without explicit project convention.
- Mutating props directly inside child components instead of emitting events (`defineEmits`).
- Triggering side effects or asynchronous mutations inside `computed()` properties.
- Passing deeply reactive objects to external non-reactive libraries, causing memory leaks and performance degradation.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://vuejs.org/guide/introduction.html
- Pinia Documentation: https://pinia.vuejs.org
- Local Inspection: Inspect `node_modules/vue/package.json` and `node_modules/vue/dist/`.
