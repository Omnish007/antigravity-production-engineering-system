---
name: architecture
id: SKILL-ARCH-001
description: Design decoupled, modular system architectures, evaluate architectural pattern trade-offs, establish domain boundaries, and author canonical Architecture Decision Records (ADRs).
---

# Architecture Design & Decision Skill

<MISSION>
Design decoupled, modular system architectures, evaluate architectural pattern trade-offs, establish domain boundaries, and author canonical Architecture Decision Records (ADRs).
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring architecture capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- The current governed task record `.agents/state/tasks/TASK-ID.json` must be `IN_PROGRESS`.
    - A `TASK_STARTED` event must be recorded in `.agents/state/events/TASK-ID.jsonl`.

### Pre-flight Checklist
- [ ] Evaluated against 4-Dimension Decision Significance Rubric (D1-D4)
- [ ] Type 1 vs Type 2 reversibility determined
- [ ] Trade-off options identified with pros and cons
- [ ] ADR file drafted in `docs/decisions/ADR-NNN-<slug>.md`
- [ ] ADR registered in `docs/decisions/INDEX.md`
- [ ] Domain boundaries and dependency directions verified
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Any technical decision meeting the Canonical Significance Criteria (Type 1 Reversibility OR any TWO of: D1 Blast Radius, D3 Trade-offs, D4 Non-Functional Impact) MUST be documented in a formal ADR before code is modified.
- ADRs must be written to `docs/decisions/ADR-NNN-<slug>.md` following the canonical ADR template (Title, Status, Context, Decision Drivers, Considered Options with pros/cons, Decision Outcome).
- Every new ADR must be registered in `docs/decisions/INDEX.md`.
- Preserve Clean / Hexagonal architecture boundaries: domain entities and business rules MUST remain completely decoupled from transport controllers and database drivers.
- Circular dependencies across modules or layers are strictly forbidden.
</NON_NEGOTIABLES>

<PROCEDURE>
## Architecture Patterns & Decision Framework

### 1. When to Author an ADR (Dynamic Decision Significance Rubric)

Author a new Architecture Decision Record in `docs/decisions/ADR-NNN-<slug>.md` whenever a choice meets the **Decision Significance Rubric**:

#### The 4 Significance Dimensions
- **D1: Blast Radius**: Does the choice affect more than one module, service boundary, or client contract?
- **D2: Reversibility (Type 1 vs Type 2)**:
  - *Type 2 (Two-Way Door)*: Easily reversible within a single module in under 2 hours without data migration. **No ADR needed.**
  - *Type 1 (One-Way Door)*: Costly or disruptive to reverse; requires database migrations, API breaking changes, or cross-cutting rewrites. **MANDATORY ADR.**
- **D3: Trade-offs**: Were 2 or more viable alternatives evaluated with divergent pros/cons (e.g., latency vs durability, simplicity vs scale)?
- **D4: Non-Functional Impact**: Does the choice alter durability guarantees (in-memory vs persistent), consistency models (ACID vs eventual), security trust boundaries, or introduce new external infrastructure/runtimes?

> **The Canonical ADR Trigger Formula**:  
> **If YES to D2 (Type 1 Reversibility) OR YES to any TWO of (D1: Blast Radius, D3: Evaluated Trade-offs, D4: Non-Functional Impact) -> A formal ADR in `docs/decisions/` is MANDATORY before writing implementation code.**

#### The 5 Architectural Planes
Evaluate every technical choice against these planes:
1. **Data & Persistence Plane**: Storage engines (SQL, NoSQL, Vector, KV), consistency models (ACID, Eventual, Outbox), schema evolution and partitioning.
2. **Communication & Transport Plane**: Interaction models (REST, GraphQL, gRPC, SSE, WebSockets, Webhooks, Message Queues), serialization formats.
3. **State & Concurrency Plane**: Process models (in-memory, Redis, distributed locks), worker architectures (in-process, daemons, serverless).
4. **Security & Trust Boundary Plane**: Auth models (sessions, JWTs, OAuth2/OIDC), authorization schemes (RBAC, ABAC, multi-tenant data isolation).
5. **Integration & Infrastructure Plane**: External service adapters, queue brokers, caching tiers, third-party framework selections.

### 2. Standard ADR Template
```markdown
# [NNNN]. [Short Title of Decision]

Date: [YYYY-MM-DD]
Status: [proposed | accepted | superseded | deprecated]
Deciders: [Roles / Stakeholders]

## Context and Problem Statement
[What is the architectural challenge? What constraints exist?]

## Decision Drivers
- [Driver 1, e.g. Crash resilience, SQLite single-writer concurrency]
- [Driver 2, e.g. Zero message loss SLA]

## Considered Options
1. [Option 1: In-Memory In-Process Queue]
2. [Option 2: Database-Backed Transactional Outbox Table]

## Pros and Cons of the Options

### Option 1: [In-Memory Queue]
- Good, because [low latency, zero database overhead]
- Bad, because [messages lost on worker crash/restart, no durability]

### Option 2: [Transactional Outbox]
- Good, because [atomic with business transactions, crash-resilient, at-least-once delivery guarantee]
- Bad, because [requires background polling worker, periodic cleanup of delivered rows]

## Decision Outcome
Chosen option: [Option 2: Transactional Outbox], because [it guarantees zero alert loss during service restarts while SQLite WAL mode prevents read contention].

### Positive Consequences
- Guarantees message delivery even if the node crashes.
- Simplifies debugging via an audit trail of outbox deliveries.

### Negative Consequences
- Requires background polling worker and periodic table pruning.
```

### 3. Layered Boundary Rules
- **Domain Layer**: Pure entities and business invariants. Zero dependencies on HTTP, database, or external SDKs.
- **Application Layer**: Use cases, orchestrators, and interface ports.
- **Infrastructure Layer**: Concrete adapters implementing ports (SQLite repositories, HTTP fetch clients, HMAC signers).
- **Presentation Layer**: HTTP route handlers, Next.js page components, CLI entrypoints.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Formal ADR committed to docs/decisions/ with clear rationale, options considered, and architectural boundaries preserved.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Architecture Decision Records (ADRs) or architecture documentation updates in docs/.
- Validated component boundary designs and module interface definitions.
</DELIVERABLES>
