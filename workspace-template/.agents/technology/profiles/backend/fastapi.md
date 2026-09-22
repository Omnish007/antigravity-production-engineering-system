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
- **Pydantic v2 Data Validation**:
  - Define explicit request, query, and response models using `pydantic.BaseModel`.
  - Use `model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)` to reject unmapped input fields.
  - Always specify `response_model` on endpoints to filter internal database fields and ensure type-safe serialization.
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

## 9. Common Anti-Patterns
- Calling blocking synchronous I/O (`requests.get()`, `time.sleep()`) inside `async def` routes, stalling the entire event loop.
- Omitting `response_model`, causing internal database entity fields (e.g. password hashes) to leak to clients.
- Mixing legacy Pydantic v1 methods (`.dict()`, `.parse_obj()`) with Pydantic v2 (`.model_dump()`, `.model_validate()`).
- Instantiating database sessions directly inside route handlers instead of using `Depends`.

## 10. Verification Commands
- Typecheck: `mypy .`
- Lint & Format: `ruff check .` and `ruff format --check .`
- Test: `pytest`
