# Technology Profile System

This directory contains modular, technology-specific knowledge profiles for the engineering operating system.

## Architecture

```text
               Universal Engineering Core
                           │
                           ↓
             .agents/technology/registry.json
                           │
       ┌───────────────────┼───────────────────┐
       ↓                   ↓                   ↓
  profiles/frontend/  profiles/backend/  profiles/database/
       │                   │                   │
       └───────────────────┼───────────────────┘
                           ↓
                 Context Router Loading
```

The universal engineering core (in `.agents/rules/` and `.agents/skills/`) remains strictly technology-neutral. When an agent works on a project, it detects the active technologies from repository evidence (or `.agents/state/stack.json`) and composes only the relevant technology profiles.

---

## Profile Directories

- `profiles/frontend/`: Frontend frameworks and UI libraries (`nextjs.md`, `react.md`, `vue.md`, `nuxt.md`, `angular.md`, `sveltekit.md`).
- `profiles/backend/`: Backend runtimes and web frameworks (`node.md`, `express.md`, `fastify.md`, `nestjs.md`, `fastapi.md`, `django.md`, `spring-boot.md`, `go.md`).
- `profiles/database/`: Database paradigms, ORMs, and query optimization (`mongodb.md`, `postgresql.md`, `mysql.md`, `sqlite.md`, `redis.md`, `dynamodb.md`).
- `profiles/language/`: Language-level idioms, type systems, and concurrency (`typescript.md`, `javascript.md`, `python.md`, `go.md`, `rust.md`, `java.md`).
- `profiles/deployment/`: Infrastructure and deployment targets (`docker.md`, `vercel.md`, `aws.md`, `k8s.md`).

---

## Adding a New Technology Profile

To add support for a new technology:

1. **Create the Profile**: Add a new markdown file under the appropriate subdirectory (e.g. `profiles/backend/phoenix.md`).
2. **Follow the Profile Standard**: Every profile must contain:
   - Scope & Detection Signals
   - Supported Version Policy
   - Core Architectural Guidance
   - Security & Performance Guidance
   - Testing Guidance
   - Common Anti-patterns
   - Official & Local Documentation Discovery
3. **Register in `registry.json`**: Add an entry with `id`, `family`, `category`, `detect` criteria, `profile` path, and documentation URLs.
4. **Zero Core Modifications**: Adding a profile must **never** require altering universal rules (`00-core.md`, `07-security.md`, `09-testing.md`).
