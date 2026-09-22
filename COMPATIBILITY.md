# Compatibility Matrix

This document defines the platform, runtime, toolchain, and standards compatibility boundaries for the Antigravity Production Engineering System (P1-67).

## 1. Core Platform & Runtime Compatibility

| Component | Minimum Supported | Recommended / Validated | Notes |
|---|---|---|---|
| **Antigravity Native Runtime** | Antigravity 2.0.0 | Antigravity 2.2.x+ | Validated against 2.x native hook protocols (`PreToolUse`, `PostToolUse`, `Stop`) and subagent orchestration. |
| **Operating System** | Linux (kernel 5.15+), macOS 13+ | Linux (Ubuntu 22.04/24.04, Debian 12), macOS 14/15 | Standard POSIX filesystem permissions, `realpath` traversal guards, atomic file operations. |
| **Python Runtime** | Python 3.10 | Python 3.11 – 3.13 | Required for governance validators, lifecycle hooks, verification policies, and state reconciler. |
| **Git Version Control** | Git 2.38.0 | Git 2.45+ | Required for worktree isolation, safe recovery checks, and atomic state tracking. |
| **YAML / JSON Engine** | PyYAML 6.0+ / Standard `json` | PyYAML 6.0.2+ | Strict schema parsing, frontmatter validation, and canonical sorted JSON hashing. |
| **Continuous Integration** | GitHub Actions runner | `ubuntu-latest` / `macos-latest` | Deterministic toolchain with pinned action SHAs and automated framework-integrity CI. |

## 2. Framework & Schema Versioning Matrix (P1-65)

| Framework Release | Canonical State Schema | Gate Registry Version | Antigravity Compatibility | Status |
|---|---|---|---|---|
| `4.0.0` | `1.0.0` | `1.0.0` (16 Task Types) | Antigravity 2.x | Active / Production Certified |
| `3.x` | Legacy unversioned | Fixed 5 gates | Antigravity 1.x / early 2.x | Deprecated |

## 3. Standards & Guidance Alignment (P1-68, P1-69, P1-70)

The system aligns with, is informed by, and maps to industry standards without claiming unassessed formal certification:

| Body | Standard / Document | Alignment & Implementation |
|---|---|---|
| **OWASP** | OWASP Top 10 for Agentic Applications (2026) | **Aligned**: Least-privilege agent definitions, tool mutation isolation, telemetry error redaction. |
| **OWASP** | OWASP Top 10 for LLM Applications | **Informed by**: Injection resistance in prompt wrappers, sensitive data protection, secret hygiene. |
| **OWASP** | OWASP Agent Control Standard (Sept 2026) | **Mapped to**: Authoritative Stop condition enforcement, pre-tool path canonicalization, runtime boundary middleware. |
| **NIST** | NIST SSDF SP 800-218 | **Informed by**: Machine-verifiable quality gates, control-plane integrity manifests (`CONTROL_PLANE_MANIFEST.json`), CODEOWNERS branch protection. |
