---
name: security
description: Perform security-focused design and code review using OWASP API/security guidance, secure session practices, validation controls, and NIST SSDF principles.
---

# Security Skill

## Threat-driven review

Identify assets, actors, trust boundaries, abuse cases, and failure impact before choosing controls.

## Required review areas

- authentication;
- session/token storage and rotation;
- authorization at object and action level;
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

## Browser sessions

Do not place authentication tokens or session IDs in web storage. Prefer secure HttpOnly cookies with deliberate `Secure` and `SameSite` attributes when using cookie-based browser sessions.

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
