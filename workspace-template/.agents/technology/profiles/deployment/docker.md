---
name: Docker
category: deployment
baselineVersion: 29.8.1 (28.x compatibility)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 29.8.1
supportedVersions:
- 29.x
- 28.x
- 27.x
legacyVersions:
- 26.x
prohibitedVersions:
- < 26.x
sources:
- https://docs.docker.com/
- https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
---
# Docker Deployment Profile

## 1. Scope
Applies to containerized applications using Docker, Dockerfile definitions, and Docker Compose development environments.

## 2. Detection Signals
- Files: `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `.dockerignore`

## 3. Supported-Version Policy
- Target: Docker Engine 29.8.1 (with 28.x compatibility) with BuildKit enabled by default.

## 4. Core Architectural Guidance
- **Multi-Stage Builds**: Separate build-time dependencies (compilers, devDependencies, SDKs) from the final runtime image using multi-stage `Dockerfile` definitions.
- **Least Privilege Execution**: Never run container processes as `root`. Create and switch to a dedicated non-root user (`USER node` or `USER appuser`).
- **Minimal Base Images**: Use minimal base images (Alpine, Distroless, or slim Debian/Ubuntu variants) to minimize attack surface and image size.
- **Layer Caching Optimization**: Order `Dockerfile` instructions from least frequently changed to most frequently changed (e.g., copy package manifests before source code).

## 5. Security & Performance Guidance
- **Secret Hygiene**: Never copy `.env` files or hard-code secrets into image layers. Inject secrets at runtime via environment variables or secret mounts.
- **Signal Handling**: Ensure the main container process responds to `SIGTERM` for graceful shutdown (use `tini` or `dumb-init` if process does not forward signals).
- **Vulnerability Scanning**: Scan container images for vulnerabilities using Trivy or Docker Scout.

## 6. Testing Guidance
- Local Verification: Test container build and run locally: `docker build -t test-app . && docker run --rm test-app`.
- Healthcheck Verification: Define `HEALTHCHECK` instructions in `Dockerfile` or compose files.
- Verification: `docker compose config` to validate compose syntax.

## 7. Common Anti-patterns
- Running containers as root UID 0 in production environments.
- Copying the entire repository into the build context without a comprehensive `.dockerignore` file.
- Embedding production secrets or API keys into Docker image layers or build args.
- Using the `:latest` tag for base images in production Dockerfiles instead of pinned version tags or sha256 digests.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.docker.com/
- Dockerfile Best Practices: https://docs.docker.com/develop/develop-images/dockerfile_best-practices/
- Local Inspection: Inspect `Dockerfile` and `docker-compose.yml` in repository root.
