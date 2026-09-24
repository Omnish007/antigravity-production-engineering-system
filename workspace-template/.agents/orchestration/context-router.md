# Context Router

<MISSION>
Route the minimum sufficient context—combining mandatory universal rules, active technology profiles, and atomic skill bundles—for every engineering task without overloading the context window.
</MISSION>

<NON_NEGOTIABLES>
- **ROUTER-01 (Four-Tier Context Structure)**: Every task domain MUST resolve context into four explicit tiers: `REQUIRED`, `RECOMMENDED`, `OPTIONAL`, and `EXCLUDED`.
- **ROUTER-02 (Calibrated Context Routing & Governed Task Boundary)**: "Not every action is a governed task; every governed task is governed completely." Read-only inquiries, direct questions, and ephemeral inspections use Inquiry mode and do not require a governed task record or mutation skills. However, for any governed task modifying application code, configuration, or repository state, the agent MUST route to and load BOTH the mandatory rule(s) (`.agents/rules/*.md`) AND the primary `REQUIRED` domain skill (`.agents/skills/*/SKILL.md`) for every domain touched before modifying code, and must satisfy full governance completion.
- **ROUTER-03 (Strict Exclusion Enforcement)**: Files, profiles, and skills listed in the `EXCLUDED` tier MUST NOT be loaded into context, preventing context bloat and hallucinated constraints.
- **ROUTER-04 (Active Profile Binding)**: Whenever a task touches a language, framework, database, or deployment domain, the matching profile from `.agents/technology/profiles/` MUST be loaded.
</NON_NEGOTIABLES>

<INSTRUCTION_HIERARCHY>
1. Platform safety constraints override all routing.
2. The user's explicit task scope determines which domain bundles are activated.
3. This router governs which context files are loaded and in what order.
</INSTRUCTION_HIERARCHY>

<CONTEXT_POLICY>
### Lane-Aware Progressive Preflight

Context loading is calibrated to the execution lane to prevent context window bloat:

#### Lane A (Fast Low-Risk Governed Mutation) Preflight
For localized low-risk edits, typos, small isolated bugfixes, single-file doc fixes, or syntax corrections:
1. User prompt & target files.
2. Core coding principles (`.agents/rules/00-core.md`).
3. Lightweight task registration in `.agents/state/tasks/<id>.json`.
4. Targeted context budget (<= 4000 tokens).
5. Minimal verification gate (`lint`) and lightweight completion record in `.agents/state/governance/<id>.json`.
*Fast does not mean unguided; it means lower ceremony.*

#### Lane B (Standard) Preflight
For features, standard bug fixes, API updates, UI components, and non-critical refactoring:
1. `AGENTS.md`
2. `docs/CURRENT_STATE.md` (current progress and baseline)
3. Domain rule (`.agents/rules/<domain>.md`) and primary domain skill (`.agents/skills/<skill>/SKILL.md`)
4. Active technology profile from `.agents/technology/profiles/`
5. Affected source and test files.

#### Lane C (High Assurance) Preflight
For auth, security, migrations, infra, production deployments, financial logic, destructive ops, or major architecture:
1. `AGENTS.md` and `.agents/orchestration/context-router.md`
2. `.agents/state/stack.json`
3. `docs/INDEX.md`, `docs/PROJECT_CONTEXT.md`, `docs/CURRENT_STATE.md`, `docs/decisions/INDEX.md`
4. `.agents/rules/00-core.md`, `.agents/rules/13-agent-safety.md`, `.agents/rules/07-security.md`
5. Active technology profiles and domain skills
6. `.agents/orchestration/governance-enforcement-policy.md` and the current task-scoped `.agents/state/governance/TASK-ID.json`
7. Domain Context Tiers mapped below.

---

### Four-Tier Context Routing Matrix by Task Domain

#### 1. Architecture & Design Decisions
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-ARCH-001`
  * Skills: `SKILL-ARCH-001`, `SKILL-GOV-001`
  * Docs: `docs/decisions/INDEX.md`, `docs/ARCHITECTURE.md`, `decision-policy.md`
- **RECOMMENDED**:
  * Skills: `SKILL-PLAN-001`, `SKILL-DOC-001`
- **OPTIONAL**:
  * Rules: `RULE-OBS-001`
- **EXCLUDED**:
  * Implementation code, CSS/UI tokens, vendor lockfiles, third-party libraries.

#### 2. Requirements & PRD Analysis
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-REQ-001`
  * Skills: `SKILL-REQ-ANALYSIS-001`, `SKILL-AC-001`
  * Docs: `docs/PROJECT_CONTEXT.md`, `docs/CURRENT_STATE.md`, `docs/requirements/`
- **RECOMMENDED**:
  * Skills: `SKILL-REQ-DISC-001`, `SKILL-PLAN-001`, `SKILL-PRD-001`
- **OPTIONAL**:
  * Rules: `RULE-MEM-001`
- **EXCLUDED**:
  * Deep backend implementation, database migration scripts, test runner internals.

#### 3. Frontend, Pages & UI Components
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-STACK-001`, `RULE-CODE-001`, `RULE-UI-001`
  * Skills: `SKILL-FRONTEND-001`, `SKILL-UIUX-001`
  * Profiles: `.agents/technology/profiles/frontend/<framework>.md`
  * Source: Target component and page files, design tokens.
- **RECOMMENDED**:
  * Skills: `SKILL-TEST-001`, `SKILL-VERIFY-001`
- **OPTIONAL**:
  * Rules: `RULE-NAMING-001`
  * Skills: `SKILL-PERF-001`
- **EXCLUDED**:
  * Database schema migrations, backend server routes, server-side infrastructure.

#### 4. Backend, APIs & Server Handlers
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-STACK-001`, `RULE-CODE-001`, `RULE-SEC-001`
  * Skills: `SKILL-BACKEND-001`, `SKILL-API-001`, `SKILL-VERIFY-001`
  * Profiles: `.agents/technology/profiles/backend/<framework>.md`, language profile
  * Source: Route handlers, controller files, API schemas.
- **RECOMMENDED**:
  * Skills: `SKILL-SEC-001`, `SKILL-TEST-001`
  * Rules: `RULE-OBS-001`, `RULE-NAMING-001`
- **OPTIONAL**:
  * Skills: `SKILL-PERF-001`
- **EXCLUDED**:
  * Client-side UI components, frontend CSS styling, browser bundle configs.

#### 5. Background Workers, Daemons & Queues
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-CODE-001`, `RULE-SEC-001`, `RULE-OBS-001`
  * Skills: `SKILL-BACKEND-001`, `SKILL-VERIFY-001`
  * Profiles: Backend runtime and language profiles
  * Source: Worker implementations, queue configurations.
- **RECOMMENDED**:
  * Skills: `SKILL-PERF-001`, `SKILL-TEST-001`
- **OPTIONAL**:
  * Skills: `SKILL-SEC-001`
- **EXCLUDED**:
  * Frontend components, HTML templates, client-side routing.

#### 6. Database, Schemas & Migrations
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-STACK-001`, `RULE-ARCH-001`, `RULE-SEC-001`
  * Skills: `SKILL-DB-001`, `SKILL-VERIFY-001`, `SKILL-GOV-001`
  * Profiles: `.agents/technology/profiles/database/<engine>.md`
  * Docs: `docs/ARCHITECTURE.md`, relevant data-model ADRs, migration files.
- **RECOMMENDED**:
  * Skills: `SKILL-BACKEND-001`, `SKILL-PERF-001`, `SKILL-TEST-001`
- **OPTIONAL**:
  * Rules: `RULE-OBS-001`
- **EXCLUDED**:
  * Client-side UI state, frontend CSS, presentation components, Vercel edge configs.

#### 7. Testing, Verification & Quality Gates
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-TEST-001`, `RULE-VERIFY-001`
  * Skills: `SKILL-TEST-001`, `SKILL-VERIFY-001`, `SKILL-GOV-001`
  * Profiles: Language and test runner profiles
  * Source: Test files, test fixtures, CI workflow scripts.
- **RECOMMENDED**:
  * Skills: `SKILL-QUALITY-001`
- **OPTIONAL**:
  * Rules: `RULE-OBS-001`
- **EXCLUDED**:
  * Unrelated feature source code outside the test scope, mock generation tooling.

#### 8. Bug Fixing & Root Cause Diagnostics
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-CODE-001`, `RULE-TEST-001`
  * Skills: `SKILL-DEBUG-001`, `SKILL-BUG-001`, `SKILL-VERIFY-001`
  * Source & Evidence: Failing test output, error logs, reproduction scripts.
- **RECOMMENDED**:
  * Skills: `SKILL-TEST-001`, `SKILL-QUALITY-001`
- **OPTIONAL**:
  * Rules: `RULE-OBS-001`
- **EXCLUDED**:
  * Unrelated application modules, speculative refactorings.

#### 9. Production Release & Deployment
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-SEC-001`, `RULE-VERIFY-001`
  * Skills: `SKILL-DEPLOY-001`, `SKILL-VERIFY-001`, `SKILL-GOV-001`
  * Profiles: `.agents/technology/profiles/deployment/<platform>.md`
  * Docs: CI/CD configuration, deployment manifests, environment templates.
- **RECOMMENDED**:
  * Skills: `SKILL-QUALITY-001`, `SKILL-SEC-001`
- **OPTIONAL**:
  * Rules: `RULE-OBS-001`
- **EXCLUDED**:
  * Local development mocks, test fixtures, documentation drafts.

#### 10. Refactoring & Technical Debt
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-ARCH-001`, `RULE-CODE-001`, `RULE-TEST-001`
  * Skills: `SKILL-REFACTOR-001`, `SKILL-TEST-001`, `SKILL-VERIFY-001`
  * Source: Target refactoring files, characterization tests, existing ADRs.
- **RECOMMENDED**:
  * Skills: `SKILL-QUALITY-001`
- **OPTIONAL**:
  * Rules: `RULE-NAMING-001`
#### 11. Security & Vulnerability Remediation
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-SEC-001`, `RULE-SAFETY-001`
  * Skills: `SKILL-SEC-001`, `SKILL-VERIFY-001`, `SKILL-GOV-001`
  * Source: Security assessment findings, vulnerable dependency specs, auth module code.
- **RECOMMENDED**:
  * Skills: `SKILL-TEST-001`, `SKILL-QUALITY-001`
- **OPTIONAL**:
  * Rules: `RULE-OBS-001`
- **DEFERRED**:
  * UI layout changes, non-security features.
- **EXCLUDED**:
  * Plaintext secrets, live production credentials.

#### 12. Git & Version Control Operations
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-SAFETY-001`
  * Skills: `SKILL-GIT-001`
  * Docs: `worktree-policy.md`, branch conventions.
- **RECOMMENDED**:
  * Skills: `SKILL-VERIFY-001`
- **OPTIONAL**:
  * Docs: `docs/CHANGELOG.md`
- **EXCLUDED**:
  * Destructive git commands (`git push --force`, `git reset --hard origin/main`).

#### 13. Agent & Control-Plane Governance
- **REQUIRED**:
  * Rules: `RULE-CORE-001`, `RULE-SAFETY-001`
  * Skills: `SKILL-GOV-001`, `SKILL-QUALITY-001`
  * Docs: `.agents/hooks.json`, `policy-registry.yaml`, `lane-policy.yaml`, `verification-policy.yaml`
- **RECOMMENDED**:
  * Docs: `.github/CODEOWNERS`
- **EXCLUDED**:
  * Application business logic, presentation assets.
</CONTEXT_POLICY>

<DECISION_RULES>
### Deterministic Merge Precedence (P1-16)
When tasks span multiple domains, context tiers merge according to this strict hierarchy:
`REQUIRED > RECOMMENDED > OPTIONAL > DEFERRED > EXCLUDED`
1. **REQUIRED Wins Over All**: If a file, rule, or skill is `REQUIRED` by any touched domain, it MUST be loaded. No domain's `EXCLUDED` tier can cancel a `REQUIRED` dependency.
2. **RECOMMENDED Union**: Union recommended items across domains, loaded if context budget permits.
3. **OPTIONAL**: Loaded strictly on demand for targeted lookups.
4. **DEFERRED**: Explicitly postponed to specialist subagents or subsequent phases.
5. **EXCLUDED**: Excluded from context to prevent bloat and hallucinated constraints, provided it is not `REQUIRED` by another active domain.

### Operational Rules
- IF an accepted ADR is relevant to the task:
    Load only the specific ADR file from `docs/decisions/`; never load all ADRs at once.
- IF a skill bundle is broader than the task scope:
    Apply progressive disclosure: load only the specific sub-procedure necessary for the task.
</DECISION_RULES>

<ANTI_PATTERNS>
- Bulk-loading the entire `docs/` or `.agents/` directory into context.
- Loading lockfiles (`package-lock.json`, `yarn.lock`), build artifacts, or minified bundles.
- Loading technology profiles that contradict the detected stack in `stack.json`.
- Loading entire inactive skill libraries when only targeted procedures are relevant.
</ANTI_PATTERNS>
