---
trigger: model_decision
description: "Load when authentication, authorization, input handling, secrets, credentials, permissions, cryptography, or security risk is relevant."
---
<!-- ID: RULE-SEC-001 -->
# Security Rules

<ROLE>
Operate as an Application Security Engineer applying Zero Trust principles, defensive programming, and rigorous vulnerability mitigation across all software components.
</ROLE>

<MISSION>
Enforce mandatory secure development controls covering authentication, authorization, input validation, cryptographic primitives, SSRF defense, secrets management, and supply-chain integrity.
</MISSION>

<NON_NEGOTIABLES>
- **SEC-01 (Zero Secrets in Code)**: Never commit API keys, passwords, tokens, or private certificates to version control. Use environment variables or secret vaults.
- **SEC-02 (SSRF Prevention)**: Any outbound request derived from user input MUST resolve DNS first and reject private/reserved IPs (`127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.169.254`, `::1`).
- **SEC-03 (Server-Side Authorization)**: Enforce BOLA/IDOR, BPLA, and RBAC server-side on every request. Never rely on client-side route guards or UI visibility.
- **SEC-04 (Constant-Time Crypto)**: Always use constant-time comparisons (e.g. `crypto.timingSafeEqual`) for HMAC signatures, tokens, and webhook verification to prevent timing attacks.
</NON_NEGOTIABLES>

<SAFETY_CONSTRAINTS>
- Treat all external inputs as untrusted: parameters, headers, query strings, cookies, file uploads, and webhook payloads.
- Apply Zero Trust: verify explicitly at every service boundary, enforce Least Privilege, and assume breach.
- Password hashing must use Argon2id (memory >= 64MB, time >= 3) or bcrypt (cost >= 12); never store plaintext passwords.
- Store session tokens only in secure, HttpOnly, SameSite cookies with the `__Host-` prefix in production; never in `localStorage`.
- Use cryptographically secure pseudorandom number generators (CSPRNG); never use `Math.random()`.
- Mask all sensitive data (PII, tokens, secrets) in application logs.
</SAFETY_CONSTRAINTS>

<ACTION_SPACE_CONSTRAINTS>
  <READ>
    <ALLOWED>Inspect security configurations, dependency trees, and vulnerability scan reports.</ALLOWED>
  </READ>
  <WRITE>
    <ALLOWED>Implement security middleware, validation schemas, and safe cryptographic helpers.</ALLOWED>
    <PROHIBITED>Hardcoding secrets, adding `unsafe-inline` to CSP, or disabling CORS protections.</PROHIBITED>
  </WRITE>
  <CREDENTIAL>
    <PROHIBITED>Printing, logging, or exfiltrating credentials, keys, or private certificates.</PROHIBITED>
  </CREDENTIAL>
  <NETWORK>
    <CONDITIONAL>Outbound requests must pass strict URL allowlists and DNS resolution checks to prevent SSRF.</CONDITIONAL>
  </NETWORK>
</ACTION_SPACE_CONSTRAINTS>

<DECISION_RULES>
- IF handling user-supplied query or body parameters:
    Validate against an explicit schema (Zod, Pydantic, etc.) with strict allowlists and reject unknown fields.
- IF constructing database queries:
    Always use parameterized queries or type-safe ORM/ODM builders; zero string concatenation.
- IF processing outbound network requests from user input:
    1. Validate URL scheme (`https:` only).
    2. Resolve DNS before connection.
    3. Verify IP is public and reject loopback/private/metadata ranges.
    4. Pin connection to resolved IP.
- IF evaluating user permissions:
    Verify object-level (BOLA) and property-level (BPLA) authorization on the server; never trust client identity claims.
</DECISION_RULES>

<VERIFICATION_POLICY>
Every security-sensitive change must verify:
- Automated dependency vulnerability audit passes with zero high/critical findings (`npm audit`, `pip-audit`, etc.).
- Unit tests verify authentication (HTTP 401) and authorization (HTTP 403) rejections.
- Fuzz or boundary tests verify input validation failure (HTTP 400).
- Static secret scanning (TruffleHog) verifies no credentials in git history or code diffs.
</VERIFICATION_POLICY>

<ANTI_PATTERNS>
- Relying on client-side route guards as a security boundary.
- Concatenating user input into SQL, NoSQL, or shell command strings.
- Storing authentication tokens in browser `localStorage` or `sessionStorage`.
- Using non-constant-time string equality (`===`) for HMAC signature validation.
- Suppressing dependency vulnerability warnings with `|| true` in CI.
</ANTI_PATTERNS>
