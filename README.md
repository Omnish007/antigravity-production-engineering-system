# Antigravity Production Engineering System — Legacy-Hardened Runtime Edition

A reusable engineering system for building software with **Antigravity 2.0 and other AI coding agents**.

The goal is simple:

> **You describe what you want to build. The project files tell the AI how the project should be understood, planned, implemented, tested, verified, and remembered.**

Instead of keeping important decisions inside chat history, this system stores them in the repository so that a **new AI chat, a new developer, or another coding agent can pick up the project with the same context**.

---

## Quick start

```bash
# 1. Install the optional Antigravity global adapter without overwriting an existing file
if [ -f ~/.gemini/GEMINI.md ]; then
  cp ~/.gemini/GEMINI.md ~/.gemini/GEMINI.md.bak
  cp global/GEMINI.md ~/.gemini/GEMINI.md.new
  echo "Merge global/GEMINI.md.new into ~/.gemini/GEMINI.md, preserving existing unrelated instructions."
else
  cp global/GEMINI.md ~/.gemini/GEMINI.md
fi

# 2. Copy workspace template into your project (includes hidden dirs .agents/ and .github/)
cp -a workspace-template/. /path/to/your-project/

# 3. Open your project in your AI coding tool and initialize:
#    The AI will detect your tech stack, configure memory, and start working.
```

The repository root `AGENTS.md` is the single project bootstrap/router. Platform adapters may add runtime-specific configuration, but they must not create a competing project governance contract.

### Post-setup: verify the runtime adapter

After copying the workspace template, keep the repository governance model as the canonical contract. The workspace already contains the Antigravity-native rule frontmatter and `.agents/hooks.json` runtime adapter. In Antigravity, verify the workspace hooks are enabled in **Settings → Customizations → Hooks** (or with `/hooks` in CLI) before relying on runtime enforcement.

The adapter provides these runtime guarantees when hooks are enabled:

| Mode | When to use | Example rules |
|---|---|---|
| **Always On** | Rules that should apply to every task | `00-core.md`, `01-project-context.md`, `11-project-memory.md`, `13-agent-safety.md` |
| **Glob** | Rules that apply only to specific file types | `04-coding.md` (→ `**/*.{ts,tsx,js,jsx}`), `06-uiux.md` (→ `**/*.{tsx,jsx,css}`) |
| **Model Decision** | Rules the AI loads when it judges them relevant | `07-security.md`, `08-git.md`, `14-observability.md` |

**Important:** rule files now carry their own native activation metadata. The table above is an audit summary, not the execution mechanism. The execution mechanism is the rule frontmatter plus `.agents/hooks.json`.

Each rule file is cataloged with its recommended activation mode in `.agents/rules/RULE_ACTIVATION.md` and `.agents/rules/rule-activation.yaml`. Each modular rule now carries the platform-native activation trigger in YAML frontmatter; `.agents/rules/rule-activation.yaml` remains the auditable routing registry. This removes a critical failure mode where a custom registry claimed activation but the host runtime could not discover the rule behavior.

Skills (`.agents/skills/`) are task-specific procedures. The host agent may load them automatically when supported; otherwise the bootstrap/router identifies the exact skill path to load. Do not load the entire skill library into context.

---

## What this package gives you

This system has ten main parts:

| Part | What it does |
|---|---|
| `global/GEMINI.md` | Thin Antigravity global adapter; repository `AGENTS.md` remains project authority. |
| `.agents/rules/` | Project rules the AI should consistently follow. |
| `.agents/technology/` | Modular technology profiles (30 profiles across frontend, backend, database, language, deployment) and machine-readable registry. |
| `.agents/preferences/` | Developer defaults with strict precedence: `Project Reality > Personal Preference`. |
| `.agents/skills/` | Reusable procedures for tasks such as planning, stack detection, features, bugs, APIs, UI, testing, security, governance enforcement, and documentation (28 skills). |
| `.agents/orchestration/` | Decides how a task should be classified, what context to load, when approval is needed, how governance is enforced, and how work moves through its lifecycle. |
| `.agents/state/` | Machine-readable project/task/governance execution state (8 state schemas, 7 populated state files + 1 JSONL, plus 1 verification schema = 9 formal schemas). |
| `.agents/templates/` | Standard templates for PRDs, features, bugs, APIs, tests, reviews, ADRs, and verification. |
| `docs/` | Human-readable project memory: what the project is, how it works, its conventions, and its current state. |
| `docs/decisions/` | One-file-per-decision ADRs that preserve important technical and architectural decisions. |

### The core idea

```text
AGENTS.md (single project bootstrap)
      ↓
Project rules + Developer preferences
      ↓
Stack detection (.agents/state/stack.json)
      ↓
Task classification + context routing (Universal core + active technology profiles)
      ↓
Relevant Skills
      ↓
Plan → Implement → Test → Verify
      ↓
Project-memory synchronization
```

---

### 2.2.2 PreInvocation capability policy

The bootstrap defaults to **safe deferred-read mode**. It does not guess whether the host can execute injected `toolCall` steps. Native injection is selected only by an explicit capability signal or explicit operator verification.

Supported controls:

```bash
# Recommended: let the system negotiate safely; unknown => deferred-read
export ANTIGRAVITY_PREINVOCATION_MODE=auto

# Force the safe path
export ANTIGRAVITY_PREINVOCATION_MODE=deferred

# Enable native injection only after verifying the runtime
export ANTIGRAVITY_PREINVOCATION_MODE=native
```

An operator-verified capability file can also be supplied through `ANTIGRAVITY_CAPABILITIES_FILE`, with this shape:

```json
{
  "preInvocation": {
    "toolCallSupport": "verified"
  }
}
```

Unknown capability is deliberately treated as unsupported.

# Universal technology stack baseline

**This system is stack-agnostic by design.** The core engineering discipline—validation, security, architecture, testing, verification, observability, and durable project memory—applies to any technology stack.

The runtime execution path is now explicit:

```text
PreInvocation bootstrap
      ↓
Capability negotiation (native toolCall vs safe deferred-read)
      ↓
Session + context plan + provisional task (governed work)
      ↓
Capability-gated bootstrap context
      ↓
Inspect → classify → load rules/skills → plan
      ↓
PreToolUse mutation gate
      ↓
Implement → test → verify → review
      ↓
State/memory sync
      ↓
Stop completion gate
```


## What changed in 2.2.0/2.2.1/2.2.2 — Legacy-Hardened + Runtime-Compatible + Capability-Gated

Version 2.2.0 was compared against the older production-engineering system that had previously been used in a real project. The merge preserves its strongest proven behaviors—root-cause-first debugging, risk-based verification, minimum-sufficient context, explicit decision/research/escalation paths, structured recovery, parallel reconciliation, and durable memory sync—without restoring its duplicate control-plane structure.

The runtime bootstrap now prioritizes task-specific rules and skills ahead of generic project-memory files. Every governed task has baseline planning, verification, testing, quality-gates, and governance-enforcement skills available, while security/testing/observability rules are promoted when directly implicated by the prompt.

See [`LEGACY_SYSTEM_REVIEW.md`](LEGACY_SYSTEM_REVIEW.md) for the full comparison and [`RESEARCH_BASIS.md`](RESEARCH_BASIS.md) for current Antigravity platform assumptions.

The system features a **modular technology layer**:

```text
.agents/technology/
├── registry.json             # Machine-readable catalog of all supported technologies
├── README.md                 # Extension guide for adding new profiles
└── profiles/
    ├── frontend/             # nextjs, react, vue, nuxt, angular, sveltekit
    ├── backend/              # node, express, fastify, nestjs, fastapi, django, spring-boot, go
    ├── database/             # postgresql, mongodb, mysql, sqlite, redis, dynamodb
    ├── language/             # typescript, javascript, python, go, rust, java
    └── deployment/           # docker, vercel, aws, k8s
```

### Stack detection and precedence

1. **Stack Detection**: On startup, `.agents/skills/stack-detection/SKILL.md` inspects project manifests (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc.) and writes active technologies to `.agents/state/stack.json`.
2. **Context Routing**: The context router (`.agents/orchestration/context-router.md`) loads only the universal rules plus the *active* technology profiles for the touched domain, keeping context clean and high-signal.
3. **Precedence Contract**:
   ```text
   Project Reality (existing manifests & code)
          >
   Personal Preference (.agents/preferences/developer-defaults.md)
          >
   Agent Default
   ```

### Keeping technology context focused

This system ships with **30 technology profiles** covering a wide range of stacks. When you clone this system into your project, **delete the profiles you do not use** to reduce context size and keep the AI focused on your actual stack.

For example, if your project uses Next.js, React, TypeScript, Express, and MongoDB, you would keep only:
- `profiles/frontend/nextjs.md`, `profiles/frontend/react.md`
- `profiles/backend/express.md`, `profiles/backend/node.md`
- `profiles/database/mongodb.md`
- `profiles/language/typescript.md`, `profiles/language/javascript.md`
- `profiles/deployment/` — keep whichever matches your deployment target

Delete all other profile files. Also update `registry.json` to remove the entries for deleted profiles.

Any deliberate architectural deviation is documented as an ADR (`docs/decisions/ADR-*.md`) rather than silently changing the system's assumptions.

---

# The most important concept: project memory

AI chat history is temporary. Your repository is the durable source of truth.

The project memory lives in:

```text
docs/
├── INDEX.md
├── PROJECT_CONTEXT.md
├── ARCHITECTURE.md
├── CONVENTIONS.md
├── CURRENT_STATE.md
├── REFERENCES.md
├── requirements/
└── decisions/
```

### What each file means

| File | Human meaning |
|---|---|
| `PROJECT_CONTEXT.md` | **What are we building and why?** |
| `ARCHITECTURE.md` | **How is the system built?** |
| `CONVENTIONS.md` | **How have we agreed to build things in this project?** |
| `CURRENT_STATE.md` | **Where are we right now?** |
| `REFERENCES.md` | **Which important external documentation and references should be used?** |
| `requirements/PRD.md` | **What does the product need to do?** |
| `requirements/ACCEPTANCE_CRITERIA.md` | **How do we know a requirement is actually satisfied?** |
| `decisions/ADR-*.md` | **What important decisions did we make, and why?** |

---

# Why ADRs are separate files

Whenever you make an important technical or architectural decision, create an ADR:

```text
docs/decisions/
├── ADR-001-centralized-api-endpoints.md
├── ADR-002-authentication-strategy.md
├── ADR-003-state-management.md
└── ADR-004-database-indexing.md
```

For example, if you decide:

> All frontend API endpoints must be defined in one shared endpoint file.

That decision should become an ADR rather than remain buried in chat history.

A future AI can then discover the decision and follow it consistently.

### Important rule

**Do not create an ADR for every tiny implementation detail.** Create one when the decision is durable, important, reusable, or likely to affect future work.

---

# How to install this system

## 1. Install the global layer once

The global file should be installed at:

```text
~/.gemini/GEMINI.md
```

Copy:

```text
global/GEMINI.md
```

to that location.

### Important

If you already have a `~/.gemini/GEMINI.md`, **merge the new content instead of blindly replacing your existing file**.

You normally do this only once per machine.

---

## 2. Add the project layer to each repository

For every project, copy the contents of:

```text
workspace-template/
```

into the root of that project.

You should end up with something similar to:

```text
my-project/
├── .agents/
│   ├── rules/
│   ├── skills/
│   ├── orchestration/
│   ├── state/
│   └── templates/
│
├── docs/
│   ├── PROJECT_CONTEXT.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── CURRENT_STATE.md
│   ├── REFERENCES.md
│   ├── requirements/
│   └── decisions/
│
└── AGENTS.md
```

Commit these project files to Git so the project's AI knowledge travels with the repository.

---

# New project workflow

For a brand-new project, use this order:

```text
1. Create repository
2. Copy workspace-template
3. Open project in Antigravity
4. Run project initialization
5. Discover and document requirements
6. Create / refine the PRD
7. Define acceptance criteria
8. Establish architecture
9. Record important decisions as ADRs
10. Plan implementation
11. Build features
12. Test
13. Verify
14. Synchronize project memory
```

The project should become progressively smarter as development continues.

---

# Existing project workflow

For an existing codebase, do **not** rebuild the application just to fit this template.

Instead:

```text
1. Add or merge .agents/
2. Add or merge docs/
3. Keep AGENTS.md
4. Run project initialization
5. Inspect the real repository
6. Document the current architecture and conventions
7. Record important existing decisions
8. Continue development using the system
```

The first initialization pass should describe the **actual repository**, not invent an idealized architecture.

---

# What happens when you start a new AI chat?

You should not need to explain the entire project again.

For a request such as:

> "Add profile editing."

The intended process is:

```text
New chat
   ↓
Read project context
   ↓
Read relevant rules
   ↓
Read relevant conventions / ADRs
   ↓
Classify the task
   ↓
Load relevant Skills
   ↓
Plan
   ↓
Implement
   ↓
Test
   ↓
Verify
   ↓
Update project memory if needed
```

This is the main reason the system is repository-native: **the project remembers the decisions made before the current conversation existed.**

---

# How the AI should remember decisions

After meaningful work, the AI should ask itself:

### Did we make a durable decision?

→ Create or update an ADR.

### Did we establish a reusable project convention?

→ Update `CONVENTIONS.md`.

### Did the system architecture change?

→ Update `ARCHITECTURE.md`.

### Did the project's current status change?

→ Update `CURRENT_STATE.md`.

### Did requirements change?

→ Update the appropriate files under `docs/requirements/`.

### Did machine-readable execution state change?

→ Update `.agents/state/`.

The important rule is:

> **Never leave significant project knowledge only in chat.**

---

# Rules vs Skills vs Memory

These are intentionally different.

| Layer | Question it answers |
|---|---|
| **Rules** | What must always be true? |
| **Skills** | How should this kind of work be performed? |
| **Orchestration** | Which process and context should be used for this task? |
| **State** | What is happening in the execution right now? |
| **Project docs** | What does this project currently know? |
| **ADR** | Why did we make this important decision? |
| **Templates** | What structure should recurring work products use? |

This separation is deliberate. It keeps the system understandable and prevents one huge instruction file from becoming a dumping ground for everything.

---

# Requirements and PRD workflow

The package includes a reusable requirements flow because most software problems begin before coding.

```text
Idea / Request
     ↓
Requirements Discovery
     ↓
Requirements Analysis
     ↓
PRD / Specification
     ↓
Acceptance Criteria
     ↓
Architecture + Planning
     ↓
Implementation
     ↓
Testing + Verification
```

Use the requirements Skills when the request is incomplete, ambiguous, large, or product-oriented.

For very small changes, the AI should use judgment and avoid creating unnecessary documentation overhead.

---

# Completion standard

"The code was written" is **not** the definition of done.

A task should be treated as complete only when the applicable checks have passed and the evidence is available.

The completion contract is:

```text
Requirements understood
        ↓
Acceptance criteria satisfied
        ↓
Relevant tests/checks executed
        ↓
Diff reviewed
        ↓
Security + regression risks considered
        ↓
Verification evidence recorded
        ↓
Project memory synchronized when needed
        ↓
State updated
        ↓
Task complete
```

When something is blocked or intentionally deferred, the state should say so explicitly rather than pretending the work is complete.

---

# Safety and human approval

The system is designed to allow useful autonomy without giving the AI unlimited authority.

Human approval is expected before high-risk actions such as:

- destructive or irreversible operations
- deleting important data
- production-affecting changes
- credential or secret handling
- financial actions
- major infrastructure changes
- security-sensitive actions with meaningful impact
- actions that could cause significant external side effects

The exact approval rules are defined in `.agents/orchestration/checkpoint-policy.md` and related policies.

---

# Source-of-truth order

When project information conflicts, use this order:

1. Safety and platform constraints
2. The user's current explicit requirement
3. Accepted project decisions / ADRs
4. Project conventions and architecture documentation
5. Existing code patterns
6. Version-matched framework/vendor documentation
7. General engineering practice
8. Agent preference

If an accepted decision must change, **supersede it deliberately**. Do not silently rewrite the old decision.

---

# Keeping the system clean

Do not turn the project memory into a diary.

Store information that is likely to remain useful:

- important architectural decisions
- durable project conventions
- significant requirements
- major constraints
- meaningful security decisions
- important workarounds
- current project status

Do not create permanent documentation for every:

- one-line bug fix
- temporary debugging step
- tiny CSS adjustment
- routine implementation detail

The objective is **high-signal memory**, not maximum documentation volume.

---

# Using the package with other AI coding tools

The project layer is intentionally repository-native.

The root:

```text
AGENTS.md
```

provides a common entry point for AI coding tools that recognize agent instructions, while the detailed Antigravity-specific controls remain under `.agents/`.

The project memory under `docs/` is ordinary repository documentation, so humans and other tools can also use it.

---

# What's inside the package

```text
antigravity-engineering-system/
│
├── global/
│   └── GEMINI.md
│
├── workspace-template/
│   ├── AGENTS.md
│   ├── .agents/
│   │   ├── preferences/
│   │   │   └── developer-defaults.md
│   │   ├── technology/
│   │   │   ├── registry.json
│   │   │   ├── README.md
│   │   │   └── profiles/
│   │   │       ├── frontend/
│   │   │       ├── backend/
│   │   │       ├── database/
│   │   │       ├── language/
│   │   │       └── deployment/
│   │   ├── rules/
│   │   ├── skills/
│   │   ├── orchestration/
│   │   ├── state/
│   │   └── templates/
│   │
│   ├── .github/
│   │   └── workflows/
│   │       └── ai-validation.yml
│   │
│   └── docs/
│       ├── project memory
│       ├── requirements
│       └── decisions / ADRs
│
├── FILE_MANIFEST.md
└── README.md
```

For a one-line explanation of **every file**, see:

```text
FILE_MANIFEST.md
```

---

# Recommended everyday usage

Once a project has been initialized, your normal interaction can stay simple:

```text
You:
"Add user profile editing with avatar upload."

AI:
→ understands project context
→ checks existing decisions
→ plans the change
→ uses the relevant Skills
→ implements
→ tests
→ verifies
→ updates project memory when needed
```

You should **not** have to remember every architectural detail yourself. The repository should increasingly carry that knowledge for you.

---

# The end goal

The system is built around one principle:

> **The longer a project lives, the more useful its repository should become as a source of engineering knowledge.**

A new chat should not mean starting from zero.

A new developer should not mean explaining the entire architecture again.

A major technical decision should not disappear into old chat messages.

The code, rules, Skills, state, requirements, conventions, and ADRs should work together as a **living engineering memory for the project**.

---

## Further reading inside this package

- `FILE_MANIFEST.md` — one-line purpose of every file
- `.agents/rules/` — project-wide constraints
- `.agents/technology/` — modular technology profiles and registry
- `.agents/preferences/` — developer defaults and precedence rules
- `.agents/skills/` — reusable procedures
- `.agents/orchestration/` — task routing and lifecycle policies
- `docs/` — persistent project memory
- `docs/decisions/` — architectural and technical decisions

---

## Cross-tool compatibility

This system works with any AI coding tool:

| Tool | How it integrates |
|---|---|
| **Gemini / Antigravity** | Reads `AGENTS.md` and `.agents/` natively |
| **Cursor** | Symlink or copy relevant content to `.cursor/rules/` |
| **Claude Code** | Symlink: `ln -s AGENTS.md CLAUDE.md` |
| **GitHub Copilot** | Reference in `.github/copilot-instructions.md` |
| **Other agents** | Most tools read `AGENTS.md` at the repository root |

The detailed rules, skills, and orchestration under `.agents/` provide depth. `AGENTS.md` provides the universal entry point.

---

## What's new in v2.1

| Addition | Purpose |
|---|---|
| Literal Instruction Wrapper Language | Canonical XML-style semantic delimiters across global instructions, bridge, rules, orchestration, and skills |
| Instruction Tag Standard & Validator | Centralized tag standard (`instruction-tag-standard.md`) and zero-tolerance validator (`validate-instruction-tags.py`) |
| Semantic Task DAG Validator | Automated DAG validation (`validate-task-dag.py`) checking acyclicity, dependency integrity, and status progression |
| Manifest Parity Checker | Automated manifest generator and validator (`generate-manifest.py`) preventing repository drift |
| Modular Technology Layer | 30 profiles across frontend, backend, database, language, and deployment + `registry.json` |
| Machine-Readable Stack Detection | `stack-detection` skill and validated `stack.json` state |
| Developer Preferences | `developer-defaults.md` with strict precedence: `Project Reality > Personal Preference` |
| Complete State Schemas | All 8 state files paired with strict JSON schemas (plus verification schema = 9 formal schemas) |
| Hardened CI/CD Quality Gates | Polyglot `ai-validation.yml` with dynamic Node, Python, and JVM toolchain support |
| `13-agent-safety.md` | OWASP LLM-aligned agent safety guardrails |
| `14-observability.md` | Agent execution tracing, context budget, drift detection |
| `context-budget-policy.md` | Context window management and token optimization |
| `error-recovery-policy.md` | Graduated failure recovery with anti-doom-loop |
| `multi-agent-policy.md` | Sub-agent delegation and handoff protocol |
| `agent-operating-contract.md` | Canonical 15-stage High-Assurance Lifecycle sequence |
| `policy-ownership.md` | Single authoritative index mapping every engineering policy domain to its canonical owner |
| `quality-gates/SKILL.md` | Self-evaluation and CI/CD gating |
| `refactoring/SKILL.md` | Behavior-preserving transformation discipline |
| `performance/SKILL.md` | Evidence-driven performance engineering |
| `incident-template.md` | Structured incident post-mortem |
| `migration-template.md` | Safe data/schema/API migration planning |
| Supply chain security | Lockfile integrity, SBOM, phantom dependency defense |
| Structured logging | Correlation IDs, consistent log levels, observability |
| Circuit breakers | Resilience patterns for external dependencies |
| Feature flags | Safe rollout discipline |
| Enhanced deployment | Blue/green, canary, SLO/SLI monitoring |
| **Runtime Bootstrap Hook** | `PreInvocation` session bootstrap that records prompt intent, prepares context loading, and creates provisional governed task state before the model acts |
| **Native Rule Activation** | Platform-native YAML frontmatter on every modular rule, replacing registry-only activation assumptions |
| **Mutation State Gate** | `PreToolUse` blocks application mutation until a governed task enters an execution state |
| **Inquiry Completion Fix** | Read-only sessions can terminate without fabricated task completion state |
| **Hook Deduplication** | One deterministic handler per lifecycle event instead of repeated identical registrations |
| **Path-Aware Policy Linting** | Policy linter works correctly from workspace root and package root |
| **Deterministic Regression Suite** | Standard pytest discovery and runtime/bootstrap regression coverage |

---

## Packaging for distribution

When creating a distributable archive of this engineering system, **exclude `.git/`, compiled bytecode, and temporary caches**:

```bash
# From the repository root:
zip -r production-engineering-system.zip . -x ".git/*" -x "*.pyc" -x "*/__pycache__/*" -x "*.DS_Store*"

# Or with tar:
tar --exclude='.git' --exclude='__pycache__' --exclude='*.pyc' -czf production-engineering-system.tar.gz .
```

The distributable archive should contain only the tracked engineering system files (verified via `FILE_MANIFEST.md`), not Git history or compiled Python bytecode.

Verify the archive is clean:

```bash
# Should show 0 results:
unzip -l production-engineering-system.zip | grep -E "(\.git/|__pycache__|\.pyc)"
```


## Runtime compatibility

Some Antigravity runtimes have been observed to reject `PreInvocation.injectSteps` entries containing native `toolCall` objects with `unknown injected step type: <nil>`. This package therefore defaults to a deferred-read `ephemeralMessage` bootstrap. Native tool-call injection is available only when explicitly enabled with `ANTIGRAVITY_ENABLE_PREINVOCATION_TOOLCALLS=1` on a verified runtime.
