# API Endpoint Contract

## Identity

- Endpoint ID:
- Method:
- Path:
- Version:
- Summary:
- Owner/module:

## Authentication

- Required: yes/no
- Mechanism:
- Required role/permission:

## Request

### Path parameters

### Query parameters

### Headers

### Body

## Validation

- Required fields:
- Type constraints:
- Length/range constraints:
- Allowed values:
- Cross-field rules:

## Authorization

Describe actor, resource, action, and property-level checks.

## Responses

| Status | Meaning | Body contract | When returned |
|---|---|---|---|
| 200 | Success | | |
| 201 | Created | | |
| 204 | No content | | |
| 400 | Bad request | Standard error body | Validation failure |
| 401 | Unauthorized | Standard error body | Missing/invalid auth |
| 403 | Forbidden | Standard error body | Insufficient permissions |
| 404 | Not found | Standard error body | Resource does not exist |
| 409 | Conflict | Standard error body | Idempotency conflict |
| 422 | Unprocessable entity | Standard error body | Business rule violation |
| 429 | Too many requests | Standard error body + Retry-After header | Rate limit exceeded |
| 500 | Internal server error | Standard error body | Unexpected failure |

### Standard error body

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Human-readable description",
    "details": []
  }
}
```

## Idempotency / retries

## Pagination / filtering / sorting

## Rate/resource limits

## Side effects

## Observability

- Log request/response at `info` level with correlation ID.
- Log errors at `error` level with stack trace and context.
- Include `requestId` in all responses for client-side debugging.
- Track latency, error rate, and throughput metrics.

## Caching

- Cache-Control header:
- ETag/Last-Modified support:
- Cache invalidation strategy:

## Versioning and deprecation

- Current version:
- Deprecated in:
- Removal date:
- Migration guide:

## Security considerations

- Input sanitization:
- Output encoding:
- CSRF protection:
- Injection prevention:
- File upload restrictions (if applicable):

## Tests

- Happy path test:
- Validation failure test:
- Auth/authz test:
- Edge case tests:
- Performance test (if applicable):

## Related files / ADRs
