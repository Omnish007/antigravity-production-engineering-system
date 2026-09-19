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
