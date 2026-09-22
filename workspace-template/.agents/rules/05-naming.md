<!-- ID: RULE-NAMING-001 -->
# Naming Rules

<ROLE>
Operate as a Language and API Design Specialist ensuring consistent, self-documenting, and idiomatic naming conventions across code, APIs, and databases.
</ROLE>

<MISSION>
Enforce consistent casing, intent-revealing identifiers, and ecosystem-idiomatic naming conventions across all project files, APIs, and database schemas.
</MISSION>

<NON_NEGOTIABLES>
- **NAM-01 (Consistent Casing Conventions)**: Follow the established casing conventions of the repository: PascalCase for components/classes, camelCase for functions/methods, UPPER_CASE for constants.
- **NAM-02 (Descriptive Identifiers)**: Single-letter variable names are strictly forbidden outside of trivial loop counters (`i`, `j`). Names must describe intent and type.
</NON_NEGOTIABLES>

<DECISION_RULES>
### Language and Ecosystem Conventions
- **TypeScript / JavaScript**:
  * Types / Classes: `PascalCase`
  * Functions / Methods / Variables: `camelCase`
  * Constants: `UPPER_SNAKE_CASE`
  * Files: `kebab-case` or `camelCase`
- **Python**:
  * Types / Classes: `PascalCase`
  * Functions / Methods / Variables: `snake_case`
  * Constants: `UPPER_SNAKE_CASE`
  * Files: `snake_case`
- **Go**:
  * Exported: `PascalCase`
  * Unexported: `camelCase`
  * Files: `snake_case`
- **Rust**:
  * Types / Traits: `PascalCase`
  * Functions / Methods / Variables: `snake_case`
  * Constants: `UPPER_SNAKE_CASE`
  * Files: `snake_case`
- **Booleans**:
  * Prefix boolean identifiers with auxiliary verbs: `isActive`, `hasPermission`, `canExecute`, `shouldRetry`.
- **REST APIs**:
  * Use plural nouns for resources (`/api/v1/users`, `/api/v1/orders/{id}`).
  * Use standard HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`).
- **Database**:
  * SQL Tables: `snake_case` plural (`users`, `order_items`).
  * SQL Columns: `snake_case` singular (`id`, `user_id`, `created_at`).
  * NoSQL Collections: `camelCase` or `snake_case` plural (`users`, `orders`).
</DECISION_RULES>

<ANTI_PATTERNS>
- Using ambiguous abbreviations (`usr`, `ctx_mgr_fn`, `tmp_val`).
- Inconsistent casing within the same file or package.
- Action verbs in REST collection endpoints (e.g. `/api/v1/getUsers`).
- Single-letter identifiers for domain entities or callback parameters.
</ANTI_PATTERNS>
