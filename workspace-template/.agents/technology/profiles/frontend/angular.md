---
name: Angular
category: frontend
baselineVersion: 21 / 22+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 21.x
supportedVersions:
- 22+
- 21.x
- 20.x
legacyVersions:
- 19.x
prohibitedVersions:
- < 19.x
sources:
- https://angular.dev
---
# Angular Technology Profile

## 1. Scope
Applies to client-side, SSR, and hybrid enterprise applications built with Angular (Angular 22 Active, Angular 21 LTS, Angular 20 LTS, with compatibility for legacy Angular codebases).

## 2. Detection Signals
- Files: `angular.json`
- Dependencies: `"@angular/core"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: Angular 22 (Active), Angular 21 (LTS), and Angular 20 (LTS).
- Greenfield Default: Prefer currently supported Angular major (Angular 22 Active or 21 LTS). Angular 2–19 are unsupported.
- Legacy Codebases: Detect installed major in `package.json`; maintain existing conventions without forcing breaking migrations unless explicitly requested.

## 4. Documentation Sources
- Official: https://angular.dev

## 5. Core Architectural Guidance
- **Mandatory Layered Separation (RULE-ARCH-LAYER-001)**:
  - Enforce the 4-tier separation:
    `Component` ──> `State / Feature Service` ──> `API Service` ──> `HttpClient`
  - **Components (`src/app/**/component.ts`)**: Pure presentation, template control flow, and Signal bindings. Making direct `HttpClient` calls or `fetch()` directly inside component methods is STRICTLY FORBIDDEN.
  - **Feature / Store Services (`@Injectable()`)**: Component/feature state management using Signals (`signal()`, `computed()`).
  - **API Services (`@Injectable({ providedIn: 'root' })`)**: Dedicated typed HTTP communication methods.
- **Standalone Components**: Default exclusively to standalone components, directives, and pipes (`standalone: true` or default in v19+). Avoid introducing `NgModule` for new features.
- **Signals & Reactivity**:
  - Use Angular Signals (`signal()`, `computed()`, `effect()`, `linkedSignal()`) for fine-grained, synchronous reactivity.
  - Enforce `ChangeDetectionStrategy.OnPush` on all components; migrate towards zoneless change detection where supported.
- **Modern Control Flow**:
  - Use built-in control flow blocks (`@if`, `@for`, `@switch`) instead of legacy structural directives (`*ngIf`, `*ngFor`, `*ngSwitch`).
  - Always provide a unique `track` expression in `@for` loops (e.g. `@for (item of items; track item.id)`).
- **Dependency Injection**:
  - Use the `inject()` function for dependency injection in component fields and functional guards/interceptors rather than verbose constructor injection.

## 6. Security Guidance
- Rely on Angular's built-in contextual auto-escaping for HTML, style, and attribute bindings.
- Avoid `DomSanitizer.bypassSecurityTrust*` methods unless rigorously audited with input sanitizers.
- Implement HTTP interceptors via `provideHttpClient(withInterceptors([...]))` to attach CSRF tokens and authorization headers.

## 7. Performance Guidance
- Use the `@angular/common` `NgOptimizedImage` directive (`ngSrc`) for automatic responsive image sizing, priority hints, and CLS elimination.
- Implement functional router guards (`canActivate: [() => inject(AuthService).isAuthenticated()]`) with route-level lazy loading (`loadComponent: () => import(...)`).
- Avoid side-effects inside `computed()` signals.

## 8. Testing Guidance
- Unit & Component: Angular TestBed with modern test runners (Vitest or Karma/Jest).
- E2E: Playwright testing against production builds (`ng build && npx http-server dist/`).

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct HTTP Calls inside Component Classes
```typescript
// ❌ FORBIDDEN: Component calling HttpClient or fetch directly
@Component({ ... })
export class UserComponent implements OnInit {
  private http = inject(HttpClient);
  users = signal<User[]>([]);

  ngOnInit() {
    // VIOLATION: Direct HTTP request bypassing API service layer!
    this.http.get<User[]>('/api/users').subscribe(u => this.users.set(u));
  }
}
```

- Introducing new `NgModule` wrappers for standalone-compatible features.
- Using `*ngFor` without `trackBy` or `@for` without a `track` expression.
- Writing heavy calculations inside template method calls instead of `computed()` signals.
- Performing side effects or HTTP calls inside `effect()`.

## 10. Verification Commands
- Typecheck: `npx tsc --noEmit`
- Lint: `ng lint` or `npm run lint`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Test: `ng test --watch=false` or `npm test`
- Build: `ng build`

## 11. Standard Layered Code Blueprint

```typescript
// 1. DTO Contract (src/app/core/models/user.model.ts)
export interface UserDto {
  id: string;
  name: string;
  email: string;
}

// 2. Dedicated API Service (src/app/core/services/user-api.service.ts)
@Injectable({ providedIn: 'root' })
export class UserApiService {
  private http = inject(HttpClient);

  getUsers(): Observable<UserDto[]> {
    return this.http.get<UserDto[]>('/api/users');
  }
}

// 3. Feature State Store (src/app/features/users/user.store.ts)
@Injectable()
export class UserStore {
  private api = inject(UserApiService);
  users = signal<UserDto[]>([]);
  loading = signal(false);

  loadUsers() {
    this.loading.set(true);
    this.api.getUsers().subscribe({
      next: (data) => this.users.set(data),
      complete: () => this.loading.set(false),
    });
  }
}

// 4. Standalone UI Component (src/app/features/users/user-list.component.ts)
@Component({
  selector: 'app-user-list',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  providers: [UserStore],
  template: `
    @if (store.loading()) {
      <p>Loading...</p>
    } @else {
      <ul>
        @for (user of store.users(); track user.id) {
          <li>{{ user.name }} ({{ user.email }})</li>
        }
      </ul>
    }
  `,
})
export class UserListComponent implements OnInit {
  protected store = inject(UserStore);

  ngOnInit() {
    this.store.loadUsers();
  }
}
```
