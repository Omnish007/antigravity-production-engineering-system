---
name: NestJS
category: backend
baselineVersion: 11.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 11.x
supportedVersions:
- 11.x
- 10.x
legacyVersions:
- 9.x
prohibitedVersions:
- < 9.x
sources:
- https://docs.nestjs.com
---
# NestJS Technology Profile

## 1. Scope
Applies to enterprise-grade Node.js and TypeScript server applications built with the NestJS framework.

## 2. Detection Signals
- Configuration files: `nest-cli.json`, `tsconfig.build.json`
- Dependencies: `"@nestjs/core"`, `"@nestjs/common"` in `package.json`

## 3. Supported-Version Policy
- Primary Target: NestJS 10.x / 11.x.
- Language & Runtime: TypeScript 5.x, Node.js 20+ LTS.

## 4. Core Architectural Guidance
- **Modular Structure**: Organize features into distinct modules (`@Module`) with clear encapsulation between controllers, providers, and exported services.
- **Dependency Injection**: Leverage Nest's IoC container; use constructor injection with typed interfaces or tokens (`@Inject()`).
- **Pipes, Guards & Interceptors**:
  - Use `ValidationPipe` with `class-validator` and `class-transformer` for strict DTO input validation (`whitelist: true`, `forbidNonWhitelisted: true`).
  - Use Guards (`canActivate`) for authentication and role-based authorization.
  - Use Interceptors for response transformation and logging.
  - Use Exception Filters for centralized error mapping to RFC 7807 problem details.

## 5. Security & Performance Guidance
- **Security Headers & CORS**: Integrate `@nestjs/helmet` and configure CORS at the application bootstrap.
- **Rate Limiting**: Use `@nestjs/throttler` for distributed rate limiting.
- **Asynchronous Execution**: Ensure all service methods performing I/O return Promises and handle cancellations.
- **Configuration Management**: Use `@nestjs/config` with validated Joi or Zod environment schemas.

## 6. Testing Guidance
- Unit Testing: Use `@nestjs/testing` `Test.createTestingModule()` to mock dependencies and test providers in isolation.
- E2E Testing: Use Supertest against the Nest application instance in `test/` directory.
- Verification: `npm run test` and `npm run test:e2e`.

## 7. Common Anti-patterns
- Creating circular module dependencies instead of using `forwardRef()` or refactoring to a shared domain module.
- Putting business logic inside Controllers rather than Injectable Services.
- Bypassing DTO validation by using `any` or untyped request bodies.
- Using request-scoped providers (`Scope.REQUEST`) unnecessarily, causing severe performance degradation.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.nestjs.com
- Local Inspection: Inspect `node_modules/@nestjs/core/package.json` and `nest-cli.json`.
