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
- **Standard Library First**: Prefer `net/http` with lightweight routing (`chi` or standard library multiplexer in Go 1.22+).
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

## 7. Common Anti-patterns
- Spawning unbounded goroutines without concurrency limits or context cancellation, leading to resource exhaustion.
- Ignoring errors or shadowing error variables in nested blocks.
- Using `panic()` in production code instead of returning structured errors.
- Passing `context.TODO()` or `context.Background()` deep into call chains instead of propagating the parent context.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://go.dev/doc/
- Standard Library Reference: https://pkg.go.dev/std
- Local Inspection: Run `go doc <package>` or inspect `go.mod`.
