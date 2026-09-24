<!-- ID: RULE-ARCH-LAYER-001 -->
# Layered Architecture & Boundary Rules

<ROLE>
Provide technology-aware boundary guidance and prevent responsibility leakage. This rule is a **default architecture pattern**, not a universal folder mandate.
</ROLE>

<MISSION>
Keep transport, application/domain logic, persistence/infrastructure, and presentation concerns separated where the active project architecture calls for those boundaries.
</MISSION>

<NON_NEGOTIABLES>
- **LAY-01 (Project Architecture Wins)**: Follow `docs/ARCHITECTURE.md`, accepted ADRs, and the active technology profile. This rule must not force a four-layer layout onto a project whose chosen architecture uses different boundaries.
- **LAY-02 (No Unjustified Boundary Bypass)**: Route/transport code must not directly access persistence when an application/domain boundary exists and is part of the project architecture.
- **LAY-03 (Core Transport Independence)**: Domain/application services must not depend on HTTP request/response objects when the project architecture defines them as transport-agnostic.
- **LAY-04 (Frontend Data Boundary)**: UI components should consume the project's API/client/state boundary rather than issuing arbitrary network/database calls directly, unless the framework's native architecture explicitly defines another safe pattern.
- **LAY-05 (Evidence-Based Exceptions)**: A deliberate deviation is acceptable when documented in the active architecture/technology profile and supported by tests.
</NON_NEGOTIABLES>

## Default Reference Pattern

For applications that actually use a classic layered backend, this pattern is recommended:

```text
Transport / Routes
        ↓
Controllers / Handlers
        ↓
Application / Domain Services
        ↓
Repositories / Infrastructure Adapters
        ↓
Persistence / External Systems
```

This diagram is a **reference pattern**, not a mandatory directory structure.

## Frontend Reference Pattern

```text
UI / Pages
   ↓
View Hooks / State
   ↓
API / Client Services
   ↓
External API
```

Framework-native server components, server actions, loaders, RPC, GraphQL, or other patterns may alter this flow when documented and validated.
