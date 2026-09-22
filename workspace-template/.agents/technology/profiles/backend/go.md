---
name: Go Backend
category: backend
baselineVersion: 1.26.8 (1.25+ compatibility)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 1.26.8
supportedVersions:
- 1.26.x
- 1.25.x
legacyVersions:
- 1.24.x
prohibitedVersions:
- < 1.24
sources:
- https://go.dev/doc/
- https://pkg.go.dev/std
---
# Go Backend Technology Profile

## 1. Scope
Applies to backend microservices, high-concurrency HTTP servers, gRPC services, and CLI tools built in Go.

## 2. Detection Signals
- Files: `go.mod`, `go.sum`
- Packages: `net/http`, `github.com/gin-gonic/gin`, `github.com/go-chi/chi`

## 3. Supported-Version Policy
- Primary Target: Go 1.26.8 (with 1.25+ compatibility).
- Baseline: Go 1.21+.

## 4. Core Architectural Guidance
- **Standard Go Clean Architecture (RULE-ARCH-LAYER-001)**:
  - **Transport / Handlers (`internal/transport/http/handler.go`)**: Decode JSON/URL payloads, invoke domain services, and encode JSON responses. Executing raw SQL, calling database connection pools, or direct query building in handlers is STRICTLY FORBIDDEN.
  - **Domain Services (`internal/domain/service.go`)**: Pure business logic, invariants, workflow orchestration, and domain error definitions. Takes `context.Context` and repository interfaces. Must have ZERO references to `net/http` or HTTP status codes.
  - **Repositories (`internal/repository/postgres.go`)**: Database queries, SQL scanning, transaction management, and persistence mapping.
  - **Domain Models / DTOs (`internal/domain/user.go`)**: Core data structures and validation methods.
- **Context Propagation**: Always pass `context.Context` as the first argument to functions performing I/O, database queries, or external calls. Respect cancellation and deadlines.
- **Error Handling**:
  - Explicit error returns `(result, error)`.
  - Wrap errors with context (`fmt.Errorf("reading config: %w", err)`).
  - Use `errors.Is` and `errors.As` for error inspection. Never ignore returned errors with `_`.
- **Concurrency & Goroutines**:
  - Prevent goroutine leaks by binding goroutine lifetimes to context cancellation or `sync.WaitGroup`.
  - Protect shared memory with `sync.Mutex` or `sync.RWMutex`, or communicate via channels.

## 5. Security & Performance Guidance
- **Timeout Configuration**: Always configure `ReadTimeout`, `WriteTimeout`, and `IdleTimeout` on `http.Server` to prevent Slowloris attacks.
- **Memory Allocation**: Minimize heap allocations in hot paths; use `sync.Pool` for reusable buffers.
- **SQL Parameterization**: Use `database/sql` query parameterization (`$1`, `?`); never concatenate SQL strings.
- **Structured Logging**: Use `log/slog` for structured, leveled JSON logging with correlation IDs.

## 6. Testing Guidance
- Unit & Race Testing: `go test -v -race ./...`
- Static Analysis: `go vet ./...` and `golangci-lint run`.
- Benchmarking: `go test -bench=. -benchmem ./...`
- Verification: `go build ./...`

## 7. Common Anti-patterns & FORBIDDEN Practices

### FORBIDDEN: Direct SQL Execution inside HTTP Handlers
```go
// ❌ FORBIDDEN: Raw SQL query executed directly inside HTTP handler
func (h *Handler) CreateUser(w http.ResponseWriter, r *http.Request) {
    // VIOLATION: Database interaction directly inside HTTP transport layer!
    _, err := h.db.ExecContext(r.Context(), "INSERT INTO users (email) VALUES ($1)", email)
    if err != nil {
        http.Error(w, err.Error(), 500)
    }
}
```

### FORBIDDEN: Passing HTTP Types to Domain Services
```go
// ❌ FORBIDDEN: Service method taking http.ResponseWriter or http.Request
type UserService struct{}
func (s *UserService) Register(w http.ResponseWriter, r *http.Request) { // VIOLATION!
}
```

- Spawning unbounded goroutines without concurrency limits or context cancellation, leading to resource exhaustion.
- Ignoring errors or shadowing error variables in nested blocks.
- Using `panic()` in production code instead of returning structured errors.
- Passing `context.TODO()` or `context.Background()` deep into call chains instead of propagating the parent context.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://go.dev/doc/
- Standard Library Reference: https://pkg.go.dev/std
- Local Inspection: Run `go doc <package>` or inspect `go.mod`.

## 9. Standard Layered Code Blueprint

```go
// 1. Domain Entities & Interfaces (internal/domain/user.go)
package domain

import "context"

type User struct {
    ID    string `json:"id"`
    Email string `json:"email"`
}

type UserRepository interface {
    GetByEmail(ctx context.Context, email string) (*User, error)
    Create(ctx context.Context, email string) (*User, error)
}

type UserService interface {
    Register(ctx context.Context, email string) (*User, error)
}

// 2. Domain Service Implementation (internal/domain/service.go) - Transport-agnostic
type userService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) UserService {
    return &userService{repo: repo}
}

func (s *userService) Register(ctx context.Context, email string) (*User, error) {
    existing, err := s.repo.GetByEmail(ctx, email)
    if err == nil && existing != nil {
        return nil, ErrDuplicateEmail
    }
    return s.repo.Create(ctx, email)
}

// 3. Repository Layer (internal/repository/postgres/user.go) - Database only
type PostgresUserRepository struct {
    db *sql.DB
}

func (r *PostgresUserRepository) Create(ctx context.Context, email string) (*domain.User, error) {
    var u domain.User
    err := r.db.QueryRowContext(ctx, "INSERT INTO users (email) VALUES ($1) RETURNING id, email", email).
        Scan(&u.ID, &u.Email)
    return &u, err
}

// 4. HTTP Transport Handler (internal/transport/http/user.go) - Thin adapter
type UserHandler struct {
    service domain.UserService
}

func (h *UserHandler) Register(w http.ResponseWriter, r *http.Request) {
    var req struct{ Email string `json:"email"` }
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "invalid request body", http.StatusBadRequest)
        return
    }
    user, err := h.service.Register(r.Context(), req.Email)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    w.WriteHeader(http.StatusCreated)
    json.NewEncoder(w).Encode(user)
}
```
