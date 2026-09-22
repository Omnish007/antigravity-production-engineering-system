---
name: Rust
category: language
baselineVersion: 2024 Edition / 1.85+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 2024 Edition / 1.85+
supportedVersions:
- 2024 Edition
- 2021 Edition / 1.78+
legacyVersions:
- 2018 Edition
prohibitedVersions:
- < 2018 Edition
sources:
- https://doc.rust-lang.org/book/
- https://doc.rust-lang.org/std/
---
# Rust Language Profile

## 1. Scope
Applies to systems programming, high-performance web services, CLI utilities, and WebAssembly modules built in Rust.

## 2. Detection Signals
- Files: `Cargo.toml`, `Cargo.lock`
- File extensions: `**/*.rs`

## 3. Supported-Version Policy
- Primary Target: Rust 2021 Edition / Rust 1.78+.
- Baseline: Rust 2021 Edition.

## 4. Core Architectural Guidance
- **Ownership & Borrowing**: Structure data flow and lifetimes to minimize unnecessary `.clone()` and heap allocations. Prefer borrowing (`&str`, `&[T]`) for read-only parameters.
- **Error Handling**:
  - Always use `Result<T, E>` with the `?` operator for fallible operations.
  - Use `thiserror` for strongly-typed, domain-specific library errors.
  - Use `anyhow` for application-level error handling with context (`.context(...)`).
- **Traits & Generics**: Define behavior with traits. Use static dispatch (generics with trait bounds) by default; use dynamic dispatch (`&dyn Trait` or `Box<dyn Trait>`) only when heterogeneous collections are required.
- **Concurrency**: Use Tokio for asynchronous I/O; leverage Rayon for data parallelism. Respect Send and Sync bounds.

## 5. Security & Performance Guidance
- **Memory Safety**: Avoid `unsafe` code blocks unless interfacing with FFI or explicitly justified with formal safety proofs.
- **Clippy Enforcement**: Run `cargo clippy -- -D warnings` to treat all linter warnings as errors.
- **Release Optimization**: Configure `[profile.release]` with LTO (`lto = true`) and strip symbols for minimal binary footprint.
- **Dependency Security**: Run `cargo audit` to detect known vulnerabilities in crate dependencies.

## 6. Testing Guidance
- Unit Tests: Co-locate unit tests in `mod tests` within the same file.
- Integration Tests: Place multi-module integration tests in the `tests/` directory.
- Verification: `cargo fmt --check && cargo clippy -- -D warnings && cargo test && cargo build --release`.

## 7. Common Anti-patterns
- Excessive use of `.unwrap()` or `.expect()` in production code paths instead of proper error propagation.
- Overusing `.clone()` to appease the borrow checker rather than restructuring ownership.
- Holding `MutexGuard` across `await` points in asynchronous Tokio code, causing deadlocks.
- Unnecessary `unsafe` blocks for operations that can be accomplished safely via standard library abstractions.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://doc.rust-lang.org/book/
- Standard Library Docs: https://doc.rust-lang.org/std/
- Local Inspection: Run `cargo doc --open` or inspect `Cargo.toml`.
