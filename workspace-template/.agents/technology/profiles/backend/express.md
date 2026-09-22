---
name: Express
category: backend
baselineVersion: 5.x
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 5.x
supportedVersions:
- 5.x
- 4.x
legacyVersions:
- 4.x
prohibitedVersions:
- < 4.x
sources:
- https://expressjs.com/en/5x/api.html
---
# Express.js Technology Profile

## 1. Scope
Applies to HTTP services, REST APIs, and backend microservices built with Express.js (Express 5.x and Express 4.x).

## 2. Detection Signals
- Dependencies: `"express"` in `package.json`
- Entrypoints: `app.listen`, `express()`, `routes/`, `controllers/`

## 3. Supported-Version Policy
- Primary Target: Express 5.x (native Promise handling in route handlers and middleware).
- Compatibility Target: Express 4.x (wrap async route handlers with an async boundary/error wrapper to catch unhandled rejections).

## 4. Core Architectural Guidance
- **Mandatory 4-Layer Separation (RULE-ARCH-LAYER-001)**:
  - **Routes (`src/routes/`)**: Declarative HTTP route definitions, URL paths, HTTP verb bindings, and middleware attachment only. Handler logic exceeding 5 lines is FORBIDDEN.
  - **Controllers (`src/controllers/`)**: Thin adapters. Extract HTTP params/query/body, call domain services, and return HTTP status codes and JSON envelopes. Direct DB or ORM calls are FORBIDDEN.
  - **Services (`src/services/`)**: Pure business logic, calculations, domain workflows, and transactions. Zero HTTP knowledge; accepting `req`, `res`, `next`, or returning HTTP status codes is FORBIDDEN.
  - **Repositories (`src/repositories/`)**: Database query abstractions, persistence operations, and data mapper logic. Only Repositories may access ORM/ODM models or SQL clients.
- **Middleware Ordering**:
  1. Security headers (`helmet`)
  2. CORS configuration (`cors`)
  3. Body parsing (`express.json({ limit: '1mb' })`)
  4. Request logging & correlation IDs
  5. Authentication & rate limiting
  6. Domain routes
  7. 404 Not Found handler
  8. Centralized error handling middleware `(err, req, res, next)` with exactly 4 parameters.

## 5. Security & Performance Guidance
- **Security Headers**: Always configure `helmet` for secure HTTP headers (HSTS, CSP, X-Frame-Options).
- **Abuse Controls**: Apply rate limiting (`express-rate-limit`) to authentication and mutating endpoints.
- **Input Validation**: Validate `req.body`, `req.query`, and `req.params` with Zod or Joi schemas before processing.
- **Process Protection**: Handle `uncaughtException` and `unhandledRejection` with graceful process termination.

## 6. Testing Guidance
- Integration Testing: Use `supertest` against the Express `app` instance without binding to a live network port.
- Unit Testing: Test service and domain functions in isolation with mocked repositories.
- Verification: `npm test` and `npm run lint`.

## 7. Common Anti-patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Queries in Route Handlers
```typescript
// ❌ FORBIDDEN: Direct ORM call and business logic inside route file
router.post('/users', async (req, res) => {
  const existing = await UserModel.findOne({ email: req.body.email }); // VIOLATION!
  if (existing) return res.status(409).json({ error: 'Exists' });
  const user = await UserModel.create(req.body); // VIOLATION!
  res.status(201).json(user);
});
```

### FORBIDDEN: Transport Leakage into Domain Services
```typescript
// ❌ FORBIDDEN: Passing Express req/res into Domain Service
export class UserService {
  async registerUser(req: Request, res: Response) { // VIOLATION: HTTP coupling!
    const email = req.body.email;
    if (!email) return res.status(400).send('Missing email'); // VIOLATION!
  }
}
```

### FORBIDDEN: Fat Routes with Inline Middleware & Logic
```typescript
// ❌ FORBIDDEN: Fat route with > 5 lines of procedural logic
router.post('/orders', async (req, res, next) => {
  // Parsing, validation, database queries, and response formatting in one file
});
```

- Omitting the `next` parameter in 4-argument error handling middleware, causing Express to treat it as standard middleware.
- Missing `await` or unhandled promise rejections in Express 4.x route handlers, causing server hangs.
- Storing request-scoped state on global variables or Express application instances.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://expressjs.com/en/5x/api.html
- Local Inspection: Inspect `node_modules/express/package.json` for installed version.

## 9. Standard Layered Code Blueprint

```typescript
// 1. DTO / Schema (src/dtos/user.dto.ts)
import { z } from 'zod';

export const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2),
  password: z.string().min(8),
});

export type CreateUserDto = z.infer<typeof CreateUserSchema>;
export type UserResponseDto = Omit<CreateUserDto, 'password'> & { id: string; createdAt: Date };

// 2. Repository Interface & Implementation (src/repositories/user.repository.ts)
export interface IUserRepository {
  findByEmail(email: string): Promise<UserEntity | null>;
  create(data: CreateUserDto): Promise<UserEntity>;
}

export class UserRepository implements IUserRepository {
  async findByEmail(email: string): Promise<UserEntity | null> {
    return UserModel.findOne({ email }).exec();
  }

  async create(data: CreateUserDto): Promise<UserEntity> {
    return UserModel.create(data);
  }
}

// 3. Domain Service (src/services/user.service.ts) - Zero HTTP knowledge
export class UserService {
  constructor(private readonly userRepo: IUserRepository) {}

  async registerUser(dto: CreateUserDto): Promise<UserResponseDto> {
    const existing = await this.userRepo.findByEmail(dto.email);
    if (existing) {
      throw new ConflictError('Email already registered');
    }
    const user = await this.userRepo.create(dto);
    return {
      id: user.id,
      email: user.email,
      name: user.name,
      createdAt: user.createdAt,
    };
  }
}

// 4. Controller (src/controllers/user.controller.ts) - Thin adapter
export class UserController {
  constructor(private readonly userService: UserService) {}

  register = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const result = await this.userService.registerUser(req.body);
      res.status(201).json({ success: true, data: result });
    } catch (err) {
      next(err);
    }
  };
}

// 5. Route (src/routes/user.routes.ts) - Declarative wiring only
import { Router } from 'express';

export function createUserRouter(controller: UserController, validate: Middleware): Router {
  const router = Router();
  router.post('/register', validate(CreateUserSchema), controller.register);
  return router;
}
```
