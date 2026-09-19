# Security Rules

Recommended activation: **Always On**

## Threat model mindset

Treat all client input, headers, query parameters, cookies, uploaded files, webhook payloads, third-party responses, and external URLs as untrusted until validated.

## Authentication

- Use modern password hashing such as Argon2id where passwords are managed directly.
- Never store plaintext passwords.
- Never place long-lived authentication credentials in `localStorage` or `sessionStorage`.
- Prefer secure, HttpOnly, appropriately scoped cookies for browser sessions when that architecture fits the application.
- Use `Secure` in production and a deliberate `SameSite` policy; use `__Host-` when applicable.
- Rotate/revoke refresh credentials and sessions on security-sensitive events.
- Rate-limit authentication and recovery endpoints.

## Authorization

Authenticate the actor, then authorize the action on the **specific object and properties involved**. Never treat the presence of a valid user ID or object ID as proof of ownership.

Check authorization server-side on every sensitive operation. Do not rely on UI visibility or route guards as the security boundary.

## Input validation

- Validate every external input server-side.
- Prefer allowlists and explicit schemas over denylist filtering.
- Enforce type, length, range, enum, and structural limits.
- Reject malformed input early.
- Validate uploads by size, type/content expectations, storage location, and processing requirements.

## Injection and output safety

Use parameterized/structured APIs. Do not build shell commands, database queries, HTML, or URLs by unsafe concatenation. Encode output according to its destination/context.

## Web security

Use HTTPS in production, security headers, appropriate CSP, strict CORS allowlists, safe cookies, CSRF defenses where cookie-authenticated state changes require them, and clickjacking protections.

## Secrets

- Never commit secrets.
- Keep real credentials out of source-controlled `.env` files.
- Use secret stores or deployment environment configuration in production.
- Provide `.env.example` with placeholders and no live credentials.
- Redact secrets from logs and verification artifacts.

## API security

Explicitly review for OWASP API Security Top 10 concerns, especially broken object-level authorization, broken authentication, property-level authorization, unrestricted resource consumption, SSRF, and unsafe API consumption.

## SSRF / outbound calls

Outbound URLs derived from user input must use an allowlist or a strong trusted-destination design. Disable access to internal/private address ranges where applicable. Apply DNS, redirect, scheme, and port controls appropriate to the use case.

## Dependency/security maintenance

Run dependency/security checks appropriate to the repository and review advisories before upgrades. Security patches should be prioritized according to actual exposure and exploitability.

## Incident-safe logging

Log enough context to investigate failures without collecting secrets or unnecessary personal data. Prefer stable IDs, request IDs, and event types over raw payloads.
