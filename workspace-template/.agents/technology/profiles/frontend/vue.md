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
- **Mandatory Layered Separation (RULE-ARCH-LAYER-001)**:
  - Enforce the 4-tier flow:
    `Components (.vue)` ──> `Composables (useFeature.ts)` ──> `API Services (api/feature.ts)` ──> `HTTP Client (apiClient.ts)`
  - **Components (`src/components/`, `src/views/`)**: Render UI layout, bindings, and template control flow. Calling `fetch()` or `axios` directly inside `<script setup>` or template handlers is STRICTLY FORBIDDEN.
  - **Composables (`src/composables/`)**: Encapsulate reactive state, computed values, side-effects, and mutations.
  - **API Services (`src/services/api/`)**: Centralized typed API functions returning DTOs.
  - **HTTP Client (`src/lib/apiClient.ts`)**: Centralized Axios/fetch client instance with interceptors.
- **Composition API & `<script setup>`**: Author components using `<script setup lang="ts">`.
- **Reactivity Model**:
  - Use `ref()` for primitive values and object references.
  - Use `reactive()` only for tightly coupled state objects; prefer `ref()` for consistency across composables.
  - Use `computed()` for derived state; computed getters must be pure and side-effect free.
  - Use `watchEffect()` or `watch()` with explicit dependencies for side effects.
- **State Management**: Use Pinia for cross-component shared state with typed actions and getters.

## 5. Security & Performance Guidance
- **XSS Prevention**: Avoid `v-html` with untrusted user input; sanitize with DOMPurify if HTML rendering is required.
- **Shallow Reactivity**: Use `shallowRef()` or `shallowReactive()` for large read-only data structures or external third-party instances (e.g., Chart.js, Leaflet, Three.js).
- **Async Components**: Use `defineAsyncComponent()` for route-level or heavy dialog components to optimize bundle splitting.

## 6. Testing Guidance
- Unit and Component Testing: Vitest with `@vue/test-utils` and `@testing-library/vue`.
- Type Checking: `vue-tsc --noEmit`.
- Linting: `eslint --ext .vue,.js,.ts src`.

## 7. Common Anti-patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Network Fetch inside `<script setup>`
```vue
<!-- ❌ FORBIDDEN: Direct fetch/axios call inside component -->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
const users = ref([]);
onMounted(async () => {
  // VIOLATION: Ad-hoc fetch directly in component script!
  const res = await fetch('/api/users');
  users.value = await res.json();
});
</script>
```

- Using Options API in greenfield Vue 3 projects without explicit project convention.
- Mutating props directly inside child components instead of emitting events (`defineEmits`).
- Triggering side effects or asynchronous mutations inside `computed()` properties.
- Passing deeply reactive objects to external non-reactive libraries, causing memory leaks and performance degradation.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://vuejs.org/guide/introduction.html
- Pinia Documentation: https://pinia.vuejs.org
- Local Inspection: Inspect `node_modules/vue/package.json` and `node_modules/vue/dist/`.

## 9. Standard Layered Code Blueprint

```typescript
// 1. API Service (src/services/api/product.api.ts)
import { apiClient } from '@/lib/apiClient';

export interface ProductDto {
  id: string;
  name: string;
  price: number;
}

export const productApi = {
  list: async (): Promise<ProductDto[]> => {
    const res = await apiClient.get<ProductDto[]>('/products');
    return res.data;
  },
};

// 2. Composable (src/composables/useProducts.ts)
import { ref } from 'vue';
import { productApi, ProductDto } from '@/services/api/product.api';

export function useProducts() {
  const products = ref<ProductDto[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  const fetchProducts = async () => {
    loading.value = true;
    error.value = null;
    try {
      products.value = await productApi.list();
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch products';
    } finally {
      loading.value = false;
    }
  };

  return { products, loading, error, fetchProducts };
}

// 3. UI Component (src/components/ProductList.vue)
<script setup lang="ts">
import { onMounted } from 'vue';
import { useProducts } from '@/composables/useProducts';

const { products, loading, error, fetchProducts } = useProducts();
onMounted(fetchProducts);
</script>

<template>
  <div v-if="loading">Loading...</div>
  <div v-else-if="error">{{ error }}</div>
  <ul v-else>
    <li v-for="p in products" :key="p.id">{{ p.name }} - ${{ p.price }}</li>
  </ul>
</template>
```
