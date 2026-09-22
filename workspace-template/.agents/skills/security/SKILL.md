---
name: security
id: SKILL-SEC-001
description: Perform security-focused design and code review using OWASP API/security guidance, secure session practices, validation controls, and NIST SSDF principles.
---

# Security Skill

<MISSION>
Perform security-focused design and code review using OWASP API/security guidance, secure session practices, validation controls, and NIST SSDF principles.
</MISSION>

<WHEN_TO_USE>
Activate this skill when executing tasks requiring security capabilities, workflows, or architectural guidance.
</WHEN_TO_USE>

<PRECONDITIONS>
### Prerequisites
- Active task in .agents/state/tasks.json must be IN_PROGRESS.
    - TASK_STARTED event must be recorded in .agents/state/events.jsonl.

### Pre-flight Checklist
- [ ] Zero secrets in code audited
    - [ ] SSRF protection active on outbound calls
    - [ ] Constant-time crypto verified
    - [ ] Server-side authorization verified
</PRECONDITIONS>

<NON_NEGOTIABLES>
- Zero secrets, API keys, or private certificates in version control.
- Enforce SSRF prevention on all outbound network requests.
- Use constant-time comparisons for HMAC signatures and auth tokens.
- Enforce server-side authorization appropriate to the request context: authenticated application requests must validate user identity and resource permissions (BOLA/BPLA/RBAC); public endpoints must enforce abuse controls and rate limits; incoming webhooks must cryptographically verify signatures; internal services must validate service tokens, IAM credentials, or mTLS.
- Sensitive data at rest MUST use an approved encryption-at-rest mechanism appropriate to the deployment environment and threat model (e.g. provider-managed storage encryption or application-level encryption such as AES-256-GCM / ChaCha20-Poly1305 where tenant isolation or host zero-trust is required); cryptographic keys MUST be stored separately from ciphertext.
</NON_NEGOTIABLES>

<PROCEDURE>
## Threat-driven review

Identify assets, actors, trust boundaries, abuse cases, and failure impact before choosing controls.

## Required review areas

- authentication and authorization boundaries;
- session/token storage and rotation;
- authorization at object and action level (BOLA/BPLA);
- input validation;
- injection;
- XSS/output encoding;
- CSRF where relevant;
- CORS;
- SSRF;
- file uploads;
- rate/resource limiting;
- secrets;
- security headers/CSP;
- dependency vulnerabilities;
- sensitive logging;
- data exposure/privacy;
- auditability for sensitive actions.

## Passwords

Use Argon2id where passwords are managed directly. Never store plaintext passwords or reversible password encryption.

## Authentication & Session Management

- **Browser Sessions**: When implementing cookie-based browser sessions, never place session tokens in web storage (localStorage/sessionStorage). Prefer secure `HttpOnly` cookies with deliberate `Secure` and `SameSite` (`Lax` or `Strict`) attributes.
- **APIs & Service-to-Service**: For stateless APIs, mobile clients, or microservices, use short-lived bearer tokens (JWT/OAuth2), API keys passed via `Authorization` headers, or mTLS.
- **Webhooks**: Verify webhook signatures (HMAC-SHA256) using a shared secret and constant-time comparison before processing payloads.

## API authorization

Check authorization at the exact resource/property/action boundary. Test unauthorized, forbidden, object-ID tampering, and mass-assignment scenarios.

## Validation

Server-side validation must be strict and explicit. Prefer allowlists and length/range constraints. Client validation improves UX but is not a security control by itself.

## Output

Record concrete risks, affected paths, severity, remediation, and verification. Avoid speculative vulnerabilities that cannot be tied to a reachable data/control flow.

## Supply chain security

- Audit `package.json` and lockfile for unexpected dependency changes.
- Check for known vulnerabilities in direct and transitive dependencies.
- Verify that new dependencies have active maintenance and no unresolved security advisories.
- Be aware of typosquat and phantom dependency attacks.
- Consider generating SBOM (Software Bill of Materials) for production releases.

## Container and image security

When the project uses containers:

- scan images for known CVEs before deployment;
- use minimal base images to reduce attack surface;
- ensure no secrets are baked into images;
- enforce non-root execution.

## Secret scanning

- Verify no secrets, API keys, or credentials exist in source code or configuration.
- Use `.env.example` with placeholder values, never real credentials.
- Integrate secret detection into CI/CD (e.g., TruffleHog, gitleaks).
- Rotate any secrets that were accidentally committed, even if the commit was reverted.

## Security headers checklist

Verify that production responses include:

- `Strict-Transport-Security` (HSTS) with appropriate `max-age`;
- `Content-Security-Policy` with nonce-based or hash-based script allowlisting;
- `X-Content-Type-Options: nosniff`;
- `X-Frame-Options` or CSP `frame-ancestors`;
- `Referrer-Policy` with a privacy-preserving value;
- `Permissions-Policy` restricting unused browser features;
- appropriate `Cache-Control` headers for sensitive responses.
</PROCEDURE>

<VERIFICATION_POLICY>
### Exit Criteria
Security controls implemented and verified via automated security tests.
</VERIFICATION_POLICY>

<DELIVERABLES>
- Threat modeling findings, security audit report, vulnerability remediations.
- Secrets scanning and dependency vulnerability check evidence.
</DELIVERABLES>
