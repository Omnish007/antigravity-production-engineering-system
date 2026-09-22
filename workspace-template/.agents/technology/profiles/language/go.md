---
name: Go
category: language
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
- https://go.dev/doc/effective_go
---
# Go Language Profile

## 1. Scope
Applies to Go services, CLI tools, and distributed applications (Go 1.22+).

## 2. Detection Signals
- Files: `go.mod`, `go.sum`, `*.go`

## 3. Supported-Version Policy
- Primary Target: Go 1.26.8 (with 1.25+ compatibility).
- Keep toolchain directives synchronized: `go mod tidy` after any dependency changes.

## 4. Documentation Sources
- Official: https://go.dev/doc/
- Effective Go: https://go.dev/doc/effective_go

## 5. Core Architectural Guidance
- **Package Organization**: Follow standard Go project layout. Keep packages focused and flat; avoid generic `util`, `common`, or `helpers` packages. Name packages by the capability they provide.
- **Explicit Error Handling**: Errors are values, not exceptions. Return errors explicitly and wrap them with context: `fmt.Errorf("operation failed: %w", err)`. Never use `panic` for standard error flows.
- **Interface Discipline**:
  - Accept interfaces, return structs.
  - Define interfaces at the consumer site, not the producer site.
  - Keep interfaces small (1-2 methods, like `io.Reader`, `io.Closer`).
- **Concurrency & Goroutines**:
  - Share memory by communicating (channels), not communicating by sharing memory.
  - Always manage goroutine lifecycles: pass `context.Context` as the first argument to all blocking, I/O, or network functions.
  - Use `sync.WaitGroup` or `golang.org/x/sync/errgroup` to wait for concurrent tasks.

## 6. Security Guidance
- Prevent SQL Injection: Use parameterized queries with `database/sql` (`db.QueryContext(ctx, "SELECT ... WHERE id = ?", id)`).
- Prevent Command Injection: Avoid executing shell commands via `exec.Command("sh", "-c", ...)`; pass arguments as discrete slices.
- Handle Panics in HTTP Handlers: Use recovery middleware (`net/http` recovery) to prevent a single panicked request from crashing the server.

## 7. Performance Guidance
- Minimize allocations in hot paths: use `sync.Pool` for reusable byte buffers and object instances.
- Use `strings.Builder` or `bytes.Buffer` for string concatenation; avoid `+` in loops.
- Use Go profiling tools (`go tool pprof`) for empirical performance analysis before optimizing.

## 8. Testing Guidance
- Unit Tests: Standard `testing` package with table-driven test patterns.
- Race Detector: Always run tests with race detection enabled: `go test -race ./...`.
- Integration Tests: Use Testcontainers-Go or build tags (`//go:build integration`).

## 9. Common Anti-Patterns
- Ignoring returned errors (`_ = doSomething()`).
- Leaking goroutines by failing to listen for `ctx.Done()`.
- Using package-level global mutable state across HTTP handlers.
- Over-abstracting with deep interface hierarchies mimicking other OOP languages.

## 10. Verification Commands
- Format: `gofmt -s -l .`
- Vet: `go vet ./...`
- Test: `go test -v -race ./...`
- Build: `go build ./...`
