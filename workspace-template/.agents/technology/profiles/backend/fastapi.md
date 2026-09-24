---
name: FastAPI
category: backend
baselineVersion: 0.115+
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 0.115+
supportedVersions:
- 0.115+
- 0.110+
legacyVersions:
- < 0.100
prohibitedVersions:
- < 0.90
sources:
- https://fastapi.tiangolo.com/
---
# FastAPI Technology Profile

## 1. Scope
Applies to Python asynchronous REST APIs, microservices, and backend services built with FastAPI.

## 2. Detection Signals
- Dependencies: `"fastapi"` in `pyproject.toml`, `requirements.txt`, `Pipfile`, or `setup.py`

## 3. Supported-Version Policy
- Primary Target: FastAPI 0.110+ with Pydantic v2.
- Python Version: Python 3.10+ (prefer Python 3.12+).

## 4. Documentation Sources
- Official: https://fastapi.tiangolo.com/

## 5. Core Architectural Guidance

The structure below is the profile's preferred boundary pattern. Follow the project's accepted architecture and ADRs when they intentionally use a different valid structure.
- **Preferred Boundary Structure (RULE-ARCH-LAYER-001)**:
  - **Routers (`src/routers/`)**: Define `@router.post("/")`, URL paths, query parameters, HTTP status codes, and `response_model`. Must inject domain services via `Depends(get_service)`. Zero direct database queries or session manipulation allowed.
  - **Domain Services (`src/services/`)**: Implement business logic, orchestration, and domain rules. Accept and return domain objects or DTOs. Completely decoupled from FastAPI `Request`, `Response`, or status codes.
  - **Repositories (`src/repositories/`)**: Pure persistence abstractions taking `AsyncSession` (or DB client) and executing SQLAlchemy/asyncpg queries.
  - **Schemas / DTOs (`src/schemas/`)**: Pydantic v2 models defining strict Request and Response schemas (`ConfigDict(extra='forbid', str_strip_whitespace=True)`).
- **Dependency Injection (`Depends`)**:
  - Use FastAPI's dependency injection system for database session management, authentication/authorization checks, and service dependencies.
  - Use lifespan handlers (`@asynccontextmanager async def lifespan(app: FastAPI): ...`) for startup and shutdown resource lifecycles.
- **Async vs. Sync Handler Discipline**:
  - Use `async def` for non-blocking I/O operations (asynchronous database drivers like `asyncpg` or `motor`, async HTTP clients like `httpx.AsyncClient`).
  - Use standard `def` for synchronous, blocking libraries (e.g. `boto3`, legacy ORMs); FastAPI automatically executes standard `def` routes in a background threadpool to prevent blocking the event loop.
- **Router Modularization**:
  - Group related endpoints using `APIRouter` with explicit `prefix` and `tags`.

## 6. Security Guidance
- Authentication: Implement OAuth2 with password flow or Bearer tokens via `fastapi.security.OAuth2PasswordBearer` and `HTTPBearer`.
- CORS Configuration: Configure `CORSMiddleware` with explicit allowed origins; never allow wildcard `"*"` origins when `allow_credentials=True`.
- Rate Limiting: Apply rate limiting on public and mutating endpoints using `slowapi` or Redis token-bucket middleware.

## 7. Performance Guidance
- Deployment Server: Run with `uvicorn` using `--workers` scaled to available CPU cores behind a reverse proxy (Nginx or cloud load balancer).
- Response Compression: Use `GZipMiddleware` for large JSON payloads (>1KB).
- Database Pooling: Use asynchronous database engines (`sqlalchemy.ext.asyncio.create_async_engine`) with bounded connection pools.

## 8. Testing Guidance
- Testing Client: Pytest with `httpx.AsyncClient` (`ASGITransport`) for asynchronous endpoint testing.
- Database Fixtures: Use isolated test database schemas or transactional rollbacks per test case.

## 9. Common Anti-Patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Database Queries or SQL in Route Endpoints
```python
# ❌ FORBIDDEN: Direct session.execute or model query inside router
@router.post("/users")
async def create_user(dto: UserCreate, db: AsyncSession = Depends(get_db)):
    # VIOLATION: Database query directly inside route handler!
    result = await db.execute(select(UserModel).where(UserModel.email == dto.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="User exists")
```

### FORBIDDEN: Transport Objects (Request/Response) in Domain Services
```python
# ❌ FORBIDDEN: Domain service taking FastAPI Request
class UserService:
    async def register(self, request: Request):  # VIOLATION: HTTP coupling in service!
        body = await request.json()
```

- Calling blocking synchronous I/O (`requests.get()`, `time.sleep()`) inside `async def` routes, stalling the entire event loop.
- Omitting `response_model`, causing internal database entity fields (e.g. password hashes) to leak to clients.
- Mixing legacy Pydantic v1 methods (`.dict()`, `.parse_obj()`) with Pydantic v2 (`.model_dump()`, `.model_validate()`).

## 10. Verification Commands
- Typecheck: `mypy .`
- Lint & Format: `ruff check .` and `ruff format --check .`
- Architecture Check: `python3 .agents/validation/check-architecture.py`
- Test: `pytest`

## 11. Standard Layered Code Blueprint

```python
# 1. Schemas / DTOs (src/schemas/user.py)
from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    email: EmailStr
    name: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    email: EmailStr
    name: str

# 2. Repository Layer (src/repositories/user_repo.py)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.session.execute(select(UserModel).where(UserModel.email == email))
        return result.scalar_one_or_none()

    async def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

# 3. Domain Service Layer (src/services/user_service.py) - Zero HTTP knowledge
class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def register_user(self, dto: UserCreate) -> UserResponse:
        existing = await self.repo.get_by_email(dto.email)
        if existing:
            raise DuplicateEntityError("Email already registered")
        entity = UserModel(email=dto.email, name=dto.name)
        saved = await self.repo.create(entity)
        return UserResponse.model_validate(saved)

# 4. Router Adapter (src/routers/user_router.py) - Thin declarative adapter
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    dto: UserCreate,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    return await service.register_user(dto)
```
