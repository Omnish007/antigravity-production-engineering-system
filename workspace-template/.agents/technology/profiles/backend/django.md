---
name: Django
category: backend
baselineVersion: 6.1 (5.2 LTS compatibility)
lastVerified: '2026-09-22'
reviewAfter: '2026-12-31'
preferredVersion: 5.2 LTS
supportedVersions:
- 5.2 LTS
- '6.1'
legacyVersions:
- 4.2 LTS
prohibitedVersions:
- < 4.2
sources:
- https://docs.djangoproject.com/en/5.1/
- https://www.django-rest-framework.org
---
# Django Technology Profile

## 1. Scope
Applies to Python web applications, APIs, and administrative backends built with Django and Django REST Framework (DRF).

## 2. Detection Signals
- Files: `manage.py`, `wsgi.py`, `asgi.py`
- Dependencies: `"django"` or `"djangorestframework"` in `pyproject.toml`, `requirements.txt`

## 3. Supported-Version Policy
- Primary Target: Django 6.1 (Python 3.12 / 3.13 / 3.14).
- Compatibility Target: Django 5.2 LTS.

## 4. Core Architectural Guidance
- **Modular App Structure**: Organize domains into self-contained apps (`models.py`, `views.py`, `serializers.py`, `urls.py`, `services.py`).
- **Fat Models vs Service Layer**: Put data integrity constraints in Models; place complex multi-model business logic in a dedicated `services/` layer.
- **Query Optimization**:
  - Always use `select_related()` for foreign key and one-to-one relations.
  - Always use `prefetch_related()` for many-to-many and reverse foreign key relations.
  - Use `values()` or `only()` for read-heavy operations requiring only a subset of fields.
- **Migrations Discipline**: Every schema change must have a generated migration; never edit existing applied migrations.

## 5. Security & Performance Guidance
- **Built-in Protections**: Maintain Django's built-in CSRF, XSS, clickjacking (`X-Frame-Options`), and secure password hashing.
- **SQL Injection Prevention**: Use Django ORM parameterization; never use raw SQL string interpolation.
- **Settings Segregation**: Separate settings into `base.py`, `development.py`, and `production.py`, loading secrets from environment variables.
- **Database Connection Pooling**: Configure `CONN_MAX_AGE` for persistent database connections in production.

## 6. Testing Guidance
- Test Framework: `pytest-django` or `python manage.py test`.
- Database Isolation: Use `@pytest.mark.django_db` with transactional test cases for rollback isolation.
- Verification: `python manage.py test` and `python manage.py check --deploy`.

## 7. Common Anti-patterns
- Triggering N+1 database queries by accessing foreign key relations in serializer loops or templates without prefetching.
- Running long-running tasks or external HTTP requests synchronously in request-response views; use Celery or RQ instead.
- Disabling CSRF protection on state-changing endpoints without an explicit token/header authentication model.
- Storing sensitive credentials or `SECRET_KEY` directly in `settings.py`.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.djangoproject.com/en/5.1/
- DRF Documentation: https://www.django-rest-framework.org
- Local Inspection: Inspect `manage.py` and installed package metadata via `pip list`.
