# Research Basis & House Engineering Standards

This document establishes the empirical, official, and architectural research foundation for the **Antigravity Multi-Stack Production Engineering System**. Every rule, skill, profile, and policy in this repository is derived from authoritative vendor documentation, current long-term support (LTS) schedules, and battle-tested industry engineering practices.

---

## 1. External Standards & Guidance

The system is informed by, aligned with, and mapped to internationally recognized engineering, security, and schema specifications (P1-68, P1-69, P1-70):

1. **OWASP Top 10 for LLM Applications (2025)**:
   - Defenses against Prompt Injection (LLM01), Sensitive Information Disclosure (LLM02), Supply Chain Vulnerabilities (LLM03), Data and Model Poisoning (LLM04), Improper Output Handling (LLM05), Excessive Agency (LLM06), System Prompt Leakage (LLM07), Vector and Embedding Weaknesses (LLM08), Misinformation (LLM09), and Unbounded Consumption (LLM10).
   - Enforced by rules: `13-agent-safety.md`, `00-core.md`, `07-security.md`.
2. **OWASP Top 10 for Agentic Applications (2026)**:
   - Defenses against Agent Goal Hijack (ASI01), Tool Misuse & Excessive Agency (ASI02), Identity & Privilege Escalation (ASI03), Supply Chain Vulnerabilities (ASI04), Insecure Multi-Agent Handoff (ASI05), Untrusted Memory & Context Corruption (ASI06), Cascading Failure & Containment Breach (ASI07), Sandboxing Failures (ASI08), Audit & Telemetry Gaps (ASI09), and Missing Human Oversight (ASI10).
   - Strict action-space boundaries (`READ`, `WRITE`, `EXECUTE`, `DELETE`, `NETWORK`, `CREDENTIAL`, `PRODUCTION`).
   - Requiring human approval for destructive operations, schema drops, and production deployments.
3. **OWASP Agent Control Standard (September 2026)**:
   - Principles of inspectability, traceability, auditability, telemetry classification, and deterministic runtime control via middleware/hooks (`PreToolUse`, `PostToolUse`, `Stop`).
   - Guaranteed task-scoped completion evaluation and non-bypassable governance barriers.
4. **NIST Secure Software Development Framework (SSDF SP 800-218) & AI RMF 1.0**:
   - Core functions: Govern, Map, Measure, and Manage with verifiable quality gates and cryptographic control-plane manifests.
5. **Semantic Versioning 2.0.0 (SemVer)**:
   - Predictable backward compatibility and migration discipline across all managed libraries and APIs.
6. **JSON Schema Draft 2020-12**:
   - Formal, machine-readable validation of all repository state files.

---

## 2. Vendor-Documented Capabilities

### 2.1 Antigravity 2.0 & Native Runtime Authority
The system recognizes Google Antigravity 2.0 native primitives as the primary execution authority:
- **Planning Mode & Implementation Plans**: High-assurance reasoning artifact (`implementation_plan.md`) presented to the user for explicit approval before code changes.
- **Task Groups & Subtasks**: Native task breakdown and execution tracking.
- **Structured Artifacts**: `walkthrough.md` for verifiable completion reporting; mermaid diagrams and rich diffs for legibility.
- **Interactive Permissions & Sandboxing**: Terminal sandbox mode (fail-closed, read/write workspace without network) and explicit bypass authorization.
- **Agent Skills Progressive Disclosure**: Directory-based skills (`SKILL.md`) with YAML frontmatter for discovery and progressive loading.

### 2.2 Active Production Release Lines (2026 Baselines)

#### Frontend Frameworks
| Ecosystem | Baseline Version | Official Documentation | Key Architectural Invariants |
|---|---|---|---|
| **Next.js** | 16.3+ (Node 20.9+ baseline) | [Next.js Documentation](https://nextjs.org/docs) | App Router default, Server Components (`RSC`) default, explicit `'use client'`, Server Actions, Turbopack. |
| **React** | 19.x | [React Documentation](https://react.dev) | React Server Components, Server Actions (`useActionState`, `useOptimistic`), React Compiler optimization; prefer compiler-driven optimization over speculative manual memoization. |
| **Vue** | 3.5+ | [Vue.js Guide](https://vuejs.org/guide) | Composition API with `<script setup>`, reactive primitives (`ref`, `computed`), Pinia, Vite. |
| **Nuxt** | 4.x | [Nuxt Documentation](https://nuxt.com/docs) | Nitro server engine, v4 folder structure (`app/`), auto-imports, universal fetch (`useFetch`). |
| **Angular** | 21 / 22+ | [Angular Documentation](https://angular.dev) | Standalone Components default, Signals reactivity, built-in control flow (`@if`, `@for`). |
| **SvelteKit** | 2.x / Svelte 5 | [SvelteKit Documentation](https://kit.svelte.dev/docs) | Svelte 5 Runes (`$state`, `$derived`, `$effect`), server-side load functions (`+page.server.ts`). |

#### Backend Runtimes & Frameworks
| Ecosystem | Baseline Version | Official Documentation | Key Architectural Invariants |
|---|---|---|---|
| **Node.js** | 22 / 24 LTS, 26 Current | [Node.js Documentation](https://nodejs.org/docs) | Native ESM, native test runner (`node:test`), structured logging, async local storage. |
| **Express** | 5.x | [Express Documentation](https://expressjs.com) | Promise rejection handling in middleware, router modularization, standardized error middleware. |
| **Fastify** | 4.x / 5.x | [Fastify Documentation](https://fastify.dev) | Schema-driven serialization via `fast-json-stringify`, encapsulated plugins, async pipelines. |
| **NestJS** | 10.x / 11.x | [NestJS Documentation](https://docs.nestjs.com) | Modular architecture, TypeScript dependency injection, validation pipes with `class-validator`. |
| **FastAPI** | 0.110+ | [FastAPI Documentation](https://fastapi.tiangolo.com) | Pydantic v2 validation models, Starlette ASGI foundation, async route handlers. |
| **Django** | 5.x / 6.x | [Django Documentation](https://docs.djangoproject.com) | Async ORM querysets, generated columns, modular settings split, transactional migrations. |
| **Spring Boot** | 3.x / 4.x | [Spring Boot Reference](https://docs.spring.io/spring-boot/docs) | Java 17-26 baseline, Virtual Threads, Spring Data JPA, GraalVM AOT compilation. |
| **Go** | 1.22+ | [Go Documentation](https://go.dev/doc) | Standard library `net/http` routing with method matching, context propagation, explicit error returns. |

#### Databases & Caches
| System | Baseline Version | Official Documentation | Key Architectural Invariants |
|---|---|---|---|
| **PostgreSQL** | 18 / 17 / 16 | [PostgreSQL Documentation](https://www.postgresql.org/docs) | ACID compliance, explicit transaction isolation levels, B-Tree/GIN/GiST indexes, connection pooling, zero-downtime expand/contract migrations. |
| **MongoDB** | 8.3 / 8.0 / 7.0 | [MongoDB Manual](https://www.mongodb.com/docs/manual) | Access-pattern-driven modeling (embedding vs referencing), ESR compound indexes, multi-document transactions when needed. |
| **MySQL** | 8.x / 9.x | [MySQL Reference Manual](https://dev.mysql.com/doc) | InnoDB engine, MVCC concurrency, transactional DDL, strict SQL mode. |
| **SQLite** | 3.45+ | [SQLite Documentation](https://www.sqlite.org/docs.html) | WAL (Write-Ahead Logging) mode, `PRAGMA foreign_keys = ON`, single-writer multi-reader concurrency. |
| **Redis** | 7.2 / 7.4 | [Redis Documentation](https://redis.io/docs) | RESP3 protocol, TTL on cache keys, distributed locking, cache-aside pattern. |
| **DynamoDB** | Current AWS API | [AWS DynamoDB Guide](https://docs.aws.amazon.com/amazondynamodb) | Single-table design, PK/SK modeling, GSIs, item size < 400 KB, optimistic concurrency. |

#### Programming Languages
| Language | Baseline Version | Official Documentation | Key Architectural Invariants |
|---|---|---|---|
| **TypeScript** | 5.5 / 5.6+ | [TypeScript Handbook](https://www.typescriptlang.org/docs) | Strict mode (`"strict": true`), no implicit `any`, discriminated unions. |
| **JavaScript** | ES2024+ | [ECMA-262 Specification](https://tc39.es/ecma262) | Native ESM, `Object.groupBy`, `Promise.withResolvers`, top-level `await`. |
| **Python** | 3.12 / 3.13 | [Python Documentation](https://docs.python.org/3) | Type hinting (PEP 695), `typing.Self`, `asyncio` task groups, pattern matching. |
| **Go** | 1.22+ | [Go Documentation](https://go.dev) | Composition over inheritance, interface segregation, goroutine lifecycle with `sync.WaitGroup`. |
| **Rust** | 2024 Edition / 1.80+ | [The Rust Reference](https://doc.rust-lang.org/reference) | Ownership and borrow checker safety, `Result<T, E>` error handling, explicit lifetimes. |
| **Java** | 21 / 25 LTS | [OpenJDK Specifications](https://openjdk.org) | Records, pattern matching for `switch`, Sealed classes, Virtual Threads. |

---

## 3. Security Standards

1. **Supply Chain Security**:
   - All third-party GitHub Actions in `.github/workflows/ai-validation.yml` are pinned to immutable 40-character commit SHAs.
2. **Fail-Closed CI**:
   - Zero tolerance for `|| true` suppressions in CI pipelines. If a quality gate fails, the pipeline fails.
3. **7-Point Security Check Evidence**:
   - Passed security checks must record: `tool`, `toolVersion`, `command`, `exitCode: 0`, `scope`, `timestamp`, and substantive non-dummy `evidence`.
4. **Prompt Injection & Agency Defense**:
   - Untrusted repository content (fixtures, comments, issues, PRs) is treated strictly as data, never as executable instructions.
   - Operating constraints restrict modifying code outside the active task scope.

---

## 4. Engineering House Policies

### 4.1 Adaptive 3-Lane Execution Model
The engineering system replaces rigid uniform lifecycles with 3 calibrated execution lanes:
- **Lane A (Fast)**: Typo fixes, symbol renames, formatting, localized doc corrections, obvious 1-file fixes $\to$ Antigravity Native Fast Mode.
- **Lane B (Standard)**: New features, bug fixes, API updates, UI components, non-critical refactoring $\to$ Native Implementation Plan / Task Groups.
- **Lane C (High Assurance)**: Auth, security changes, migrations, infra, production deployments, financial logic, destructive ops, or major architecture $\to$ Full High-Assurance Governed Lifecycle.

### 4.2 Canonical ADR Trigger Formula
Architectural Decision Records (ADRs) are governed by an objective mathematical trigger:
$$\text{Trigger ADR} \iff (\text{D2} = \text{Type 1}) \lor (\text{Count}(D1, D3, D4) \ge 2)$$
Where:
- **D1 (Blast Radius)**: Decision impacts more than one architectural boundary, subsystem, public API contract, or external integration.
- **D2 (Reversibility)**: Type 1 decisions are irreversible or prohibitively costly to undo (e.g., framework, database engine, protocol changes). Type 2 decisions are reversible two-way doors.
- **D3 (Trade-offs)**: Decision involves explicit, mutually exclusive architectural trade-offs (e.g., consistency vs availability, latency vs memory, build-time vs runtime).
- **D4 (Non-Functional Impact)**: Decision impacts security, compliance, data persistence, durability, performance SLAs, or scalability.

### 4.3 Single Authoritative Hierarchy
- **Execution Authority**: Antigravity Native Runtime (Planning Mode, Task Groups, Artifacts, Permissions, Terminal Sandbox).
- **Governance Metadata Layer**: `.agents/rules/`, `.agents/skills/`, `.agents/agents/`, `.agents/technology/`, `.agents/state/`.
- **Policy Ownership**: `.agents/orchestration/policy-ownership.md`.
- **Context Routing**: `.agents/orchestration/context-router.md` (Lane-aware progressive disclosure).

### 4.4 Stable Identifiers
To decouple governance tracking from filesystem paths:
- Rules: `RULE-CORE-001` through `RULE-OBS-001` (15 rules).
- Skills: `SKILL-AC-001` through `SKILL-VERIFY-001` (28 skills).
- Specialized Agents: 8 defined roles in `.agents/agents/`.

### 4.5 5-Layer Governance Validation
Automated semantic validation via `validate-governance.py`:
- Layer 1: JSON Parsing.
- Layer 2: JSON Schema Validation (Draft 2020-12).
- Layer 3: Semantic & Physical Reference Validation (Disk existence of rules, skills, profiles, ADRs).
- Layer 4: Task, Event, Lifecycle & Blocker Consistency.
- Layer 5: Completion Eligibility (Grouped Completion Invariants, Groups A–J).

---

## 5. Project-Specific Policies

All project-specific architectures, conventions, and requirements are defined in:
- `docs/ARCHITECTURE.md`
- `docs/CONVENTIONS.md`
- `docs/requirements/PRD.md`
- `docs/decisions/` (Accepted ADRs)
- `docs/CURRENT_STATE.md`
