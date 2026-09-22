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
- **Mandatory Frontend Layer Separation (RULE-ARCH-LAYER-001)**:
  - All React frontends must strictly adhere to the unidirectional flow:
    `Components/` ──> `hooks/` ──> `services/api/` ──> `lib/api-client.ts`
  - **Components (`src/components/`)**: Pure UI rendering and layout. Must NOT contain direct `fetch()`, `axios()`, or direct state store mutations. Delegates state management and side effects to custom hooks.
  - **Custom Hooks (`src/hooks/`)**: Encapsulate component-level view state, caching (e.g. TanStack Query), lifecycle, and mutations.
  - **API Services (`src/services/api/`)**: Pure TypeScript functions wrapping backend API endpoints with typed request and response DTOs.
  - **HTTP Client (`src/lib/api-client.ts`)**: Centralized instance with base URL, timeout, authorization headers, and error interceptors.
- **Functional Components & Hooks**: Pure functional components with explicit, predictable state hooks.
- **State Locality**: Keep state as close to where it is used as possible. Lift state only when multiple components need to synchronize.
- **React 19 Actions & Transitions**:
  - Use `useTransition` and `useActionState` for pending states and error handling during async operations.
  - Use `useOptimistic` for instant UI feedback with automatic rollback on mutation failure.
  - Direct ref forwarding: pass `ref` directly as a component prop in React 19 without `forwardRef`.
  - Use the `use()` hook for reading promises and context conditionally in render.
- **Effect Discipline**: Avoid using `useEffect` for data fetching or synchronizing state with props. Use effects only for external synchronization (DOM manipulation, event listeners, external subscriptions).

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

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Network Fetching inside JSX Component Bodies
```tsx
// ❌ FORBIDDEN: Calling fetch/axios directly inside useEffect or click handlers
export function UserList() {
  const [users, setUsers] = useState([]);
  useEffect(() => {
    // VIOLATION: Ad-hoc fetch directly inside component rendering body!
    fetch('http://localhost:5000/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);
  return <div>{users.length}</div>;
}
```

### FORBIDDEN: Inline Axios Calls in Event Handlers
```tsx
// ❌ FORBIDDEN: Calling axios inside button onClick
<button onClick={async () => {
  await axios.post('/api/logout'); // VIOLATION: Bypasses API service and custom hook!
}}>Logout</button>
```

- Using `useEffect` to fetch data without handling cancellation / cleanup, leading to race conditions.
- Mutating state directly instead of using functional state setters or immutable data patterns.
- Prop drilling through >3 layers when composition or context is more appropriate.

## 10. Verification Commands
- Typecheck: `npx tsc --noEmit`
- Lint: `npm run lint` or `npx eslint .`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Tests: `npm test` or `npx vitest`

## 11. Standard Layered Code Blueprint

```typescript
// 1. Centralized HTTP Client (src/lib/api-client.ts)
import axios from 'axios';

export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// 2. Typed API Service (src/services/api/user.api.ts)
import { apiClient } from '@/lib/api-client';

export interface UserDto {
  id: string;
  name: string;
  email: string;
}

export const userApi = {
  getUsers: async (): Promise<UserDto[]> => {
    const response = await apiClient.get<UserDto[]>('/users');
    return response.data;
  },
};

// 3. Custom Hook (src/hooks/use-users.ts)
import { useQuery } from '@tanstack/react-query';
import { userApi, UserDto } from '@/services/api/user.api';

export function useUsers() {
  return useQuery<UserDto[], Error>({
    queryKey: ['users'],
    queryFn: userApi.getUsers,
    staleTime: 60 * 1000,
  });
}

// 4. UI Component (src/components/user-list.tsx) - Pure UI rendering
import { useUsers } from '@/hooks/use-users';

export function UserList() {
  const { data: users, isLoading, error } = useUsers();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error loading users: {error.message}</div>;

  return (
    <ul>
      {users?.map(u => (
        <li key={u.id}>{u.name} ({u.email})</li>
      ))}
    </ul>
  );
}
```
