# Rule Activation Reference

<MISSION>
Provide an authoritative catalog of all project rules, their stable IDs, activation criteria, precedence levels, and domain bindings.
</MISSION>

## Activation Tiers

1. **ALWAYS**: Universal foundational rules loaded on every execution.
2. **CODE_TOUCH**: Activated whenever application source code is inspected or modified.
3. **GOVERNED_TASK**: Activated whenever a task enters formal governance (Lane B or Lane C).
4. **DOMAIN_MATCH**: Dynamically activated based on the task domain identified by `.agents/orchestration/context-router.md`.
5. **TASK_INIT / STATE_SYNC**: Activated during specific task lifecycle phases.

## Rule Activation Matrix

| Rule ID | Name | File | Activation | Precedence | Domain / Purpose |
|---|---|---|---|---|---|
| `RULE-CORE-001` | Core Engineering Principles | `00-core.md` | ALWAYS | 100 | Universal engineering constraints |
| `RULE-SAFETY-001` | Agent Safety Invariants | `13-agent-safety.md` | ALWAYS | 95 | Sandboxing, credentials, prompt safety |
| `RULE-CODE-001` | Coding Discipline | `04-coding.md` | CODE_TOUCH | 90 | Language/code style and cleanliness |
| `RULE-VERIFY-001` | Verification Rules | `10-verification.md` | GOVERNED_TASK | 85 | Mandatory verification & exit codes |
| `RULE-ARCH-001` | Architecture & Design | `03-architecture.md` | DOMAIN_MATCH | 80 | System boundaries, ADR triggers |
| `RULE-SEC-001` | Security Engineering | `07-security.md` | DOMAIN_MATCH | 80 | Security, auth, SAST scanning |
| `RULE-TEST-001` | Testing Standards | `09-testing.md` | DOMAIN_MATCH | 75 | Unit, integration, e2e testing |
| `RULE-STACK-001` | Technology Stack Conventions | `02-tech-stack.md` | DOMAIN_MATCH | 75 | Detected stack conventions |
| `RULE-CTX-001` | Project Context & Architecture | `01-project-context.md` | TASK_INIT | 70 | Architecture & domain understanding |
| `RULE-REQ-001` | Requirements & Acceptance Criteria | `12-requirements.md` | DOMAIN_MATCH | 70 | PRD & acceptance criteria |
| `RULE-UI-001` | UI/UX & Frontend Conventions | `06-uiux.md` | DOMAIN_MATCH | 65 | Accessibility, components, styling |
| `RULE-NAMING-001` | Naming Conventions | `05-naming.md` | CODE_TOUCH | 60 | Consistent identifier naming |
| `RULE-GIT-001` | Git & Version Control | `08-git.md` | DOMAIN_MATCH | 60 | Commits, branches, PR discipline |
| `RULE-MEM-001` | Project Memory Discipline | `11-project-memory.md` | STATE_SYNC | 55 | Durable memory synchronization |
| `RULE-OBS-001` | Observability & Telemetry | `14-observability.md` | DOMAIN_MATCH | 50 | Logging, metrics, tracing |

See `rule-activation.yaml` for the machine-readable version.
