# Project External References

Use this document for project-specific external references that materially influence implementation. Prefer official documentation, version-matched APIs, specifications, and authoritative standards.

## Current dependencies

> Populate with the project's primary frameworks, runtimes, database drivers, and libraries.

| Technology | Installed version | Official docs | Bundled / local docs path | Last verified | Notes |
|---|---|---|---|---|---|
| *(e.g. Runtime)* | | | | | |
| *(e.g. Web / API Framework)* | | | | | |
| *(e.g. Database / ORM)* | | | | | |
| *(e.g. Test Runner)* | | | | | |

## Security standards

| Reference | Version | Applicability | URL | Last reviewed |
|---|---|---|---|---|
| OWASP API Security Top 10 | 2023 | API endpoint design and validation | https://owasp.org/API-Security/ | |
| OWASP Top 10 for LLM Applications | 2026 | Agent safety (see `13-agent-safety.md`) | https://genai.owasp.org/ | |
| OWASP Top 10 for Agentic Applications | 2026 | Agentic security (goal hijacking, tool misuse, identity abuse) | https://genai.owasp.org/ | |
| OWASP Session Management Cheat Sheet | | Session/cookie handling | https://cheatsheetseries.owasp.org/ | |
| OWASP Password Storage Cheat Sheet | | Password hashing (Argon2id) | https://cheatsheetseries.owasp.org/ | |
| NIST SSDF | 1.1 | Secure development lifecycle | https://csrc.nist.gov/ | |

## Accessibility and performance

| Reference | Version | Applicability | URL | Last reviewed |
|---|---|---|---|---|
| WCAG | 2.2 | UI accessibility compliance | https://www.w3.org/WAI/WCAG22/ | |
| WAI-ARIA | 1.2 | Component accessibility patterns | https://www.w3.org/WAI/ARIA/ | |
| Core Web Vitals | current | Performance measurement | https://web.dev/vitals/ | |

## Infrastructure and operations
 
| Reference | Applicability | URL | Last reviewed |
|---|---|---|---|
| GitHub Actions security hardening | CI/CD workflow safety | https://docs.github.com/en/actions/security-for-github-actions | |
| OpenTelemetry documentation | Distributed tracing & observability | https://opentelemetry.io/docs/ | |
| 12-Factor App methodology | Cloud-native application design | https://12factor.net/ | |

## Version sensitivity rule

When version-sensitive behavior matters, record the exact source/version used for the decision so future agents can reassess it during upgrades. Always prefer installed/bundled documentation over stale model knowledge.

When upgrading a major dependency:

1. Update the version in this table.
2. Review breaking changes in the release notes.
3. Record any convention changes in `docs/CONVENTIONS.md`.
4. Create an ADR if the upgrade affects architecture.
5. Update relevant rules/skills if behavior has changed.
