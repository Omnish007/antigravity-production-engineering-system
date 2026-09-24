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

The structure below is the profile's preferred boundary pattern. Follow the project's accepted architecture and ADRs when they intentionally use a different valid structure.
- **Preferred Boundary Structure (RULE-ARCH-LAYER-001)**:
  - **Routing (`urls.py`)**: Declarative URL path routing and view binding only.
  - **Views / ViewSets (`views.py`)**: Thin HTTP adapters. Validate inputs via DRF Serializers, invoke domain services in `services.py`, and return HTTP responses. Complex business logic or direct queries in views are FORBIDDEN.
  - **Domain Services (`services.py`)**: Pure business logic, state mutations, and multi-model transactions. Transport-agnostic (never accept `HttpRequest`). Prevents "Fat Models" anti-pattern.
  - **Data Selectors / Repositories (`selectors.py` or Model Managers)**: Pure database read queries, query optimization (`select_related`, `prefetch_related`), and data retrieval.
  - **Serializers / Schemas (`serializers.py`)**: Input validation contracts and response serialization.
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

## 7. Common Anti-patterns & FORBIDDEN Practices

### FORBIDDEN: Direct Queries & Business Logic in Views
```python
# ❌ FORBIDDEN: View mixing validation, queries, and business logic
class OrderView(APIView):
    def post(self, request):
        # VIOLATION: Direct ORM calls and inline transaction logic in view
        order = Order.objects.create(user=request.user, total=request.data['total'])
        Inventory.objects.filter(item_id=request.data['item_id']).update(stock=F('stock') - 1)
        return Response({'id': order.id})
```

### FORBIDDEN: Passing HttpRequest into Domain Services
```python
# ❌ FORBIDDEN: Passing request object into service
def process_order(request: HttpRequest): # VIOLATION: Transport coupling!
    user = request.user
```

- Triggering N+1 database queries by accessing foreign key relations in serializer loops or templates without prefetching.
- Running long-running tasks or external HTTP requests synchronously in request-response views; use Celery or RQ instead.
- Disabling CSRF protection on state-changing endpoints without an explicit token/header authentication model.
- Storing sensitive credentials or `SECRET_KEY` directly in `settings.py`.

## 8. Official & Local Documentation Discovery
- Official Documentation: https://docs.djangoproject.com/en/5.1/
- DRF Documentation: https://www.django-rest-framework.org
- Local Inspection: Inspect `manage.py` and installed package metadata via `pip list`.

## 9. Standard Layered Code Blueprint

```python
# 1. Serializer / DTO (src/orders/serializers.py)
from rest_framework import serializers

class CreateOrderSerializer(serializers.Serializer):
    item_id = serializers.UUIDField()
    quantity = serializers.IntegerField(min_value=1)

# 2. Selectors / Query Layer (src/orders/selectors.py)
from .models import Item, Order

def get_item_by_id(item_id: str) -> Item | None:
    return Item.objects.filter(id=item_id).first()

# 3. Domain Service (src/orders/services.py) - Pure domain logic, no request/response
from django.db import transaction
from rest_framework.exceptions import ValidationError

def create_order(*, user_id: str, item_id: str, quantity: int) -> Order:
    with transaction.atomic():
        item = get_item_by_id(item_id)
        if not item or item.stock < quantity:
            raise ValidationError("Insufficient inventory")
        item.stock -= quantity
        item.save(update_fields=['stock'])
        return Order.objects.create(user_id=user_id, item=item, quantity=quantity)

# 4. View Adapter (src/orders/views.py) - Thin adapter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class OrderCreateView(APIView):
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = create_order(
            user_id=request.user.id,
            item_id=serializer.validated_data['item_id'],
            quantity=serializer.validated_data['quantity'],
        )
        return Response({'id': str(order.id)}, status=status.HTTP_201_CREATED)
```
