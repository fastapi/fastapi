# HTTP QUERY Method Support in FastAPI

## Overview

The HTTP QUERY method is a proposed HTTP method that allows for safe, cacheable requests with a request body. Unlike GET requests, which are limited by URL length constraints, QUERY enables complex queries to be sent in the request body while maintaining the safety and cacheability characteristics of GET.

## Current Status in HTTP Standards

The QUERY method is defined in [draft-ietf-httpbis-safe-method-w-body](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-safe-method-w-body), which proposes adding safe HTTP methods that can carry request bodies.

## Proposed FastAPI Usage

```python
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class SearchQuery(BaseModel):
    terms: List[str]
    filters: Optional[dict] = None
    sort_by: Optional[str] = None
    limit: Optional[int] = 100

@app.query("/search")
async def search_items(query: SearchQuery):
    """Search items using complex query parameters in request body"""
    # Process search with complex filters
    results = perform_search(
        terms=query.terms,
        filters=query.filters,
        sort_by=query.sort_by,
        limit=query.limit
    )
    return {"results": results, "count": len(results)}

@app.query("/analytics")
async def get_analytics(query: dict):
    """Get analytics data with complex query parameters"""
    # Process analytics query
    return calculate_analytics(query)
```

## POST Workaround (Current Implementation)

Until QUERY method gains wider support, FastAPI can provide a workaround using POST:

```python
@app.post("/search", tags=["query-workaround"])
async def search_items_post_workaround(query: SearchQuery):
    """Search items using POST as QUERY workaround"""
    # Same implementation as QUERY method
    results = perform_search(
        terms=query.terms,
        filters=query.filters,
        sort_by=query.sort_by,
        limit=query.limit
    )
    return {"results": results, "count": len(results)}
```

## OpenAPI/Swagger Limitations

### Current Limitations
- OpenAPI 3.0.x specification doesn't officially support QUERY method
- Swagger UI may not render QUERY endpoints correctly
- Some HTTP clients don't support QUERY method yet

### Potential Solutions
- Document QUERY endpoints as POST in OpenAPI spec with special annotations
- Add custom OpenAPI extensions for QUERY method documentation
- Provide clear documentation about method semantics

```python
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="FastAPI with QUERY Method",
        version="1.0.0",
        description="API supporting HTTP QUERY method",
        routes=app.routes,
    )
    
    # Add custom extensions for QUERY method
    for path, methods in openapi_schema["paths"].items():
        if "post" in methods and "query-method" in methods["post"].get("tags", []):
            methods["post"]["x-http-method"] = "QUERY"
            methods["post"]["description"] += "\n\n**Note**: This endpoint uses HTTP QUERY method semantics (safe, cacheable, idempotent) but is documented as POST due to OpenAPI limitations."
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

## Implementation Examples

### Complex Search Query

```python
class AdvancedSearchQuery(BaseModel):
    text_search: Optional[str] = None
    date_range: Optional[dict] = None
    categories: Optional[List[str]] = None
    price_range: Optional[dict] = None
    geo_location: Optional[dict] = None
    sort_options: Optional[List[dict]] = None
    pagination: Optional[dict] = {"page": 1, "size": 20}

@app.query("/products/search")
async def search_products(query: AdvancedSearchQuery):
    """Advanced product search with complex filtering"""
    return await product_service.search(query)
```

### Analytics Query

```python
class AnalyticsQuery(BaseModel):
    metrics: List[str]
    dimensions: List[str]
    filters: Optional[List[dict]] = None
    date_range: dict
    aggregations: Optional[List[dict]] = None

@app.query("/analytics/report")
async def generate_report(query: AnalyticsQuery):
    """Generate analytics report based on complex query"""
    return await analytics_service.generate_report(query)
```

## Benefits of QUERY Method

1. **Safety**: Like GET, QUERY requests are safe and should not modify server state
2. **Cacheability**: Responses can be cached by intermediaries
3. **Idempotency**: Multiple identical requests have the same effect
4. **Complex Parameters**: Request body allows for complex query structures
5. **No URL Length Limits**: Unlike GET, not constrained by URL length

## Migration Strategy

1. **Phase 1**: Implement QUERY endpoints with POST fallback
2. **Phase 2**: Add OpenAPI extensions and documentation
3. **Phase 3**: Gradual adoption as client support improves
4. **Phase 4**: Full QUERY method support when standardized

## Testing QUERY Endpoints

```python
import pytest
from fastapi.testclient import TestClient

def test_query_search():
    with TestClient(app) as client:
        query_data = {
            "terms": ["python", "fastapi"],
            "filters": {"category": "programming"},
            "sort_by": "relevance",
            "limit": 50
        }
        
        # Test with POST workaround
        response = client.post("/search", json=query_data)
        assert response.status_code == 200
        assert "results" in response.json()
```

## References

- [HTTP QUERY Method Draft](https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-safe-method-w-body)
- [HTTP Methods Specification](https://tools.ietf.org/html/rfc7231#section-4)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI 3.0 Specification](https://swagger.io/specification/)

## Related Issues

- FastAPI Issue #12965: Add support for HTTP QUERY method
- Discussion on safe methods with request bodies
- OpenAPI specification limitations and extensions
