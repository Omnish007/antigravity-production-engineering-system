# Antigravity 2.0 Production Engineering System

A reusable engineering system for building software with **Antigravity 2.0 and other AI coding agents**.

The goal is simple:

> **You describe what you want to build. The project files tell the AI how the project should be understood, planned, implemented, tested, verified, and remembered.**

Instead of keeping important decisions inside chat history, this system stores them in the repository so that a **new AI chat, a new developer, or another coding agent can pick up the project with the same context**.

---

## Quick start

```bash
# 1. Copy global rules (once per machine)
cp global/GEMINI.md ~/.gemini/GEMINI.md

# 2. Copy workspace template into your project
cp -r workspace-template/* /path/to/your-project/

# 3. Open your project in your AI coding tool and start working
```

The system works immediately with any AI coding tool that reads `AGENTS.md` at the repository root.

---

## What this package gives you

This system has eight main parts:

| Part | What it does |
|---|---|
| `global/GEMINI.md` | Your personal, machine-wide engineering rules. Install once. |
| `.agents/rules/` | Project rules the AI should consistently follow. |
| `.agents/skills/` | Reusable procedures for tasks such as planning, features, bugs, APIs, UI, testing, security, and documentation. |
| `.agents/orchestration/` | Decides how a task should be classified, what context to load, when approval is needed, and how work moves through its lifecycle. |
| `.agents/state/` | Machine-readable project/task execution state. |
| `.agents/templates/` | Standard templates for PRDs, features, bugs, APIs, tests, reviews, ADRs, and verification. |
| `docs/` | Human-readable project memory: what the project is, how it works, its conventions, and its current state. |
| `docs/decisions/` | One-file-per-decision ADRs that preserve important technical and architectural decisions. |

### The core idea

```text
Global behavior
      ↓
Project rules
      ↓
Task classification + context routing
      ↓
Relevant Skills
      ↓
Plan → Implement → Test → Verify
      ↓
Project-memory synchronization
```

---

# Your default technology stack

The system is designed around your usual stack:

- **Next.js**
- **React**
- **TypeScript**
- **Tailwind CSS**
- **shadcn/ui**
- **Node.js**
- **Express.js**
- **MongoDB**

The files do **not** permanently force one exact patch version. The intended approach is to use the version already declared by the project and consult version-matched official documentation when technical behavior depends on the installed version.

A project can intentionally use a different technology or architecture. That change should be documented as a deliberate project decision rather than silently changing the system's assumptions.

**This system is stack-agnostic by design.** The engineering discipline (testing, security, verification, memory) applies to any stack. See `.agents/rules/02-tech-stack.md` for alternative stack profiles.

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
├── RESEARCH_BASIS.md
├── VALIDATION.md
└── README.md
```

For a one-line explanation of **every file**, see:

```text
FILE_MANIFEST.md
```

For the external standards and official documentation used as reference material, see:

```text
RESEARCH_BASIS.md
```

For the structural/content checks performed on the package, see:

```text
VALIDATION.md
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

## What's new in v2.0

| Addition | Purpose |
|---|---|
| `13-agent-safety.md` | OWASP LLM-aligned agent safety guardrails |
| `14-observability.md` | Agent tracing, context budget, drift detection |
| `context-budget-policy.md` | Context window management and token optimization |
| `error-recovery-policy.md` | Graduated failure recovery with anti-doom-loop |
| `multi-agent-policy.md` | Sub-agent delegation and handoff protocol |
| `quality-gates/SKILL.md` | Self-evaluation and CI/CD gating |
| `refactoring/SKILL.md` | Behavior-preserving transformation discipline |
| `performance/SKILL.md` | Evidence-driven performance engineering |
| `incident-template.md` | Structured incident post-mortem |
| `migration-template.md` | Safe data/schema/API migration planning |
| `.github/workflows/` | CI/CD template for AI-generated changes |
| Stack-agnostic design | Rules work with any technology stack |
| Cross-tool interop | Works with Cursor, Claude, Copilot, and others |
| Risk classification | Tasks classified by risk level |
| Supply chain security | Lockfile integrity, SBOM, phantom dependency defense |
| Structured logging | Correlation IDs, consistent log levels, observability |
| Circuit breakers | Resilience patterns for external dependencies |
| Feature flags | Safe rollout discipline |
| Enhanced deployment | Blue/green, canary, SLO/SLI monitoring |
