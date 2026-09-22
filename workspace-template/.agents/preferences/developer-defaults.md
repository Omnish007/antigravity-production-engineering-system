# Developer Personal Preference Profile

<MISSION>
Record the developer's preferred technology baseline for new projects when no existing repository conventions, architecture, or requirements dictate otherwise.
</MISSION>

<NON_NEGOTIABLES>
- Personal preferences must NEVER silently override project reality. If a repository contains Vue, Nuxt, Angular, FastAPI, Go, PostgreSQL, or any other stack, the agent must adhere strictly to the project's actual stack.
</NON_NEGOTIABLES>

<INSTRUCTION_HIERARCHY>
## Precedence Order

When determining the technology stack, conventions, or tooling for any repository:

```text
Project Explicit Decision (ADR / PRD)
          ↓
Project Detected Stack (repository evidence / stack.json)
          ↓
Project Convention (docs/CONVENTIONS.md)
          ↓
Personal Preference (this document)
          ↓
Generic Recommendation
```
</INSTRUCTION_HIERARCHY>

<DECISION_RULES>
## Preferred Personal Stack Baseline

### Frontend
- **Framework**: Next.js (App Router, Server/Client Component architecture)
- **UI Library**: React 19
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS v4
- **Component Primitives**: shadcn/ui (composable, open-code primitives)

### Backend
- **Runtime**: Node.js (Active LTS)
- **Framework**: Express.js 5 (async error handling, structured middleware)
- **Language**: TypeScript

### Database & Storage
- **Primary Database**: MongoDB (access-pattern-driven document modeling)
- **ODM**: Mongoose (where schema validation and middleware are beneficial)
- **Caching**: Redis (where sub-millisecond caching or rate-limiting is needed)

### Testing & Verification
- **Unit & Integration**: Vitest or Jest with Testing Library
- **End-to-End**: Playwright (isolated, deterministic user-flow verification)
- **Verification**: Typecheck (`tsc --noEmit`), Lint (`eslint`), Test, Build

---

## Local Documentation Primacy

For Next.js projects specifically, the agent must inspect version-matched documentation shipped with the installed package when available:
`node_modules/next/dist/docs/`
before relying on general knowledge or remote search.
</DECISION_RULES>
