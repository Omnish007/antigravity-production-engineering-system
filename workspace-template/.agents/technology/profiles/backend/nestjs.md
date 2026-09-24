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

The structure below is the profile's preferred boundary pattern. Follow the project's accepted architecture and ADRs when they intentionally use a different valid structure.
- **Preferred Boundary Structure (RULE-ARCH-LAYER-001)**:
  - **Controllers**: Thin HTTP adapters. Handle ONLY `@Body()`, `@Param()`, `@Query()`, and return values or invoke response formatters. Direct database access or Prisma/TypeORM queries are STRICTLY FORBIDDEN.
  - **Services (`@Injectable()`)**: Contain all business logic, authorization rules, domain validations, and transaction boundaries. Must remain completely transport-agnostic (never inject `@Res()` or Express `Response`).
  - **Repositories / Providers**: Isolated persistence layer using dedicated repository classes or abstract providers wrapping TypeORM, Prisma, or Mongoose.
  - **DTOs & Validation**: Input data validated using `class-validator` decorators and global `ValidationPipe` (`whitelist: true`, `forbidNonWhitelisted: true`).
- **Modular Structure**: Organize features into distinct modules (`@Module`) with clear encapsulation between controllers, providers, and exported services.
- **Dependency Injection**: Leverage Nest's IoC container; use constructor injection with typed interfaces or tokens (`@Inject()`).

## 5. Security & Performance Guidance
- **Security Headers & CORS**: Integrate `@nestjs/helmet` and configure CORS at the application bootstrap.
- **Rate Limiting**: Use `@nestjs/throttler` for distributed rate limiting.
- **Asynchronous Execution**: Ensure all service methods performing I/O return Promises and handle cancellations.
- **Configuration Management**: Use `@nestjs/config` with validated Joi or Zod environment schemas.

## 6. Testing Guidance
- Unit Testing: Use `@nestjs/testing` `Test.createTestingModule()` to mock dependencies and test providers in isolation.
- E2E Testing: Use Supertest against the Nest application instance in `test/` directory.
- Verification: `npm run test` and `npm run test:e2e`.

## 7. Common Anti-patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Queries in Controllers
```typescript
// ❌ FORBIDDEN: Controller executing database queries directly
@Controller('users')
export class UserController {
  constructor(private readonly prisma: PrismaService) {} // VIOLATION: Direct ORM injection in controller!

  @Post()
  async create(@Body() dto: CreateUserDto) {
    return this.prisma.user.create({ data: dto }); // VIOLATION: DB query in controller!
  }
}
```

### FORBIDDEN: Transport Coupling in Services
```typescript
// ❌ FORBIDDEN: Injecting Express response into Service
@Injectable()
export class UserService {
  async processPayment(@Res() res: Response) { // VIOLATION: Transport leak into service!
    res.status(200).send('ok');
  }
}
```

- Creating circular module dependencies instead of using `forwardRef()` or refactoring to a shared domain module.
- Bypassing DTO validation by using `any` or untyped request bodies.
- Using request-scoped providers (`Scope.REQUEST`) unnecessarily, causing severe performance degradation.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.nestjs.com
- Local Inspection: Inspect `node_modules/@nestjs/core/package.json` and `nest-cli.json`.

## 9. Standard Layered Code Blueprint

```typescript
// 1. DTO with class-validator (src/users/dto/create-user.dto.ts)
import { IsEmail, IsString, MinLength } from 'class-validator';

export class CreateUserDto {
  @IsEmail()
  email!: string;

  @IsString()
  @MinLength(2)
  name!: string;
}

// 2. Repository Interface & Implementation (src/users/repositories/user.repository.ts)
export interface IUserRepository {
  findByEmail(email: string): Promise<UserEntity | null>;
  create(data: CreateUserDto): Promise<UserEntity>;
}

@Injectable()
export class UserRepository implements IUserRepository {
  constructor(private readonly prisma: PrismaService) {}

  async findByEmail(email: string): Promise<UserEntity | null> {
    return this.prisma.user.findUnique({ where: { email } });
  }

  async create(data: CreateUserDto): Promise<UserEntity> {
    return this.prisma.user.create({ data });
  }
}

// 3. Domain Service (src/users/services/user.service.ts)
@Injectable()
export class UserService {
  constructor(@Inject('IUserRepository') private readonly userRepo: IUserRepository) {}

  async register(dto: CreateUserDto): Promise<UserResponseDto> {
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) throw new ConflictException('Email already registered');
    return this.userRepo.create(dto);
  }
}

// 4. Controller (src/users/controllers/user.controller.ts)
@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post('register')
  @HttpCode(HttpStatus.CREATED)
  async register(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.userService.register(dto);
  }
}
```
