---
name: Python
category: language
baselineVersion: 3.14 (3.13 / 3.12 LTS compatibility)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 3.13 LTS
supportedVersions:
- '3.14'
- 3.13 LTS
- 3.12 LTS
legacyVersions:
- '3.11'
- '3.10'
prohibitedVersions:
- < 3.10
sources:
- https://docs.python.org/3/
- https://docs.python.org/3/library/typing.html
---
# Python Language Profile

## 1. Scope
Applies to Python applications, libraries, APIs, data processing scripts, and automation tools.

## 2. Detection Signals
- Files: `pyproject.toml`, `requirements.txt`, `setup.py`, `.python-version`
- File extensions: `**/*.py`

## 3. Supported-Version Policy
- Primary Target: Python 3.14.
- Baseline: Python 3.13 and 3.12 LTS.

## 4. Core Architectural Guidance
- **Type Annotations**: Use modern type hinting (`typing`, `list[str]`, `dict[str, Any]`, `X | Y` union syntax). Avoid untyped function signatures in production code.
- **Environment & Dependency Management**: Use `pyproject.toml` with modern package managers (`uv` or `poetry`). Avoid unpinned global `pip install`.
- **Async Concurrency**: Use `asyncio` with structured concurrency (`asyncio.TaskGroup` in Python 3.11+). Never mix blocking I/O calls directly into async event loops without `asyncio.to_thread()`.
- **Data Modeling**: Use `@dataclass(slots=True)` or Pydantic v2 models for structured data transfer objects.

## 5. Security & Performance Guidance
- **Code Execution**: Never use `eval()`, `exec()`, or untrusted `pickle.loads()`.
- **Process Management**: Use `subprocess.run()` with explicit list arguments (`shell=False`) to prevent shell injection.
- **Linting & Formatting**: Enforce `ruff` for lightning-fast linting and formatting; use `mypy --strict` for static type checking.
- **Dependency Auditing**: Audit dependencies for CVEs using `pip-audit` or `uv pip audit`.

## 6. Testing Guidance
- Test Framework: `pytest` with `pytest-asyncio` for async tests and `pytest-cov` for coverage.
- Fixtures: Use typed, modular pytest fixtures with explicit scoping (`scope="session"`, `scope="function"`).
- Verification: `ruff format --check . && ruff check . && mypy . && pytest`.

## 7. Common Anti-patterns
- Using mutable default arguments (e.g., `def func(items=[])`).
- Catching bare `except:` or `except Exception:` without re-raising or logging context.
- Running blocking synchronous I/O inside async functions without `asyncio.to_thread()`.
- Unpinned dependencies in production deployment manifests.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.python.org/3/
- Typing Documentation: https://docs.python.org/3/library/typing.html
- Local Inspection: Run `python3 -c "import sys; print(sys.version)"` and inspect `pyproject.toml`.
