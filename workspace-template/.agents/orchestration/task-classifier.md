# Task Classifier

## Purpose

Classify incoming work so the agent loads the smallest sufficient set of context and capabilities.

## Categories

| Type | Typical signal | Normal skills |
|---|---|---|
| `requirements` | idea, scope discovery, unclear request | requirements-discovery, requirements-analysis |
| `prd-analysis` | PRD/specification submitted | prd-analysis, acceptance-criteria, planning |
| `planning` | architecture or implementation plan requested | planning, architecture via relevant skill/context |
| `simple-fix` | isolated low-risk change, no behavior boundary change | relevant implementation + verification |
| `bug-fix` | defect, error, failing test, regression | debugging, bug-fix, testing, verification |
| `feature` | new localized product behavior | feature-development + relevant frontend/backend/api/database skills |
| `complex-feature` | cross-layer feature, new auth/data architecture, material risk | planning + feature-development + relevant layer skills + review/security |
| `refactor` | internal restructuring with intended behavior preserved | refactoring via code-review/feature-development path + testing |
| `database-change` | schema/index/query/migration work | database + backend + testing |
| `security-change` | auth, authorization, secrets, security control | security + affected layer + testing + review |
| `review` | code review/audit | code-review + verification + relevant specialty |
| `documentation` | docs/ADR/project-memory work | documentation + project-memory |
| `deployment` | CI/CD, release, environment, runtime | deployment + verification + security when applicable |

## Classification rules

- A bug report outranks a generic feature classification.
- Security-sensitive work always activates security guidance.
- Cross-layer changes should not be treated as a simple fix.
- PRD analysis precedes coding unless the user explicitly requests implementation of an already-resolved plan.
- A change affecting auth, data integrity, payment, secrets, destructive operations, or public compatibility should be treated as high-risk.

## Output

For each task, derive:

- task type;
- affected layers;
- relevant skills;
- required context files;
- approval requirements;
- verification scope;
- whether memory synchronization is expected.
