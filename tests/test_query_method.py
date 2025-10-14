"""
Tests for the QUERY HTTP method implementation in FastAPI
"""

from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class SearchQuery(BaseModel):
    terms: List[str]
    filters: Dict[str, Any] = {}
    limit: int = 10


def test_query_method_basic():
    """Test basic QUERY method functionality"""
    app = FastAPI()

    @app.query("/search/")
    def search_items(query: SearchQuery):
        return {"results": [{"id": 1, "name": "test"}], "query": query.dict()}

    client = TestClient(app)

    # Test QUERY request with body
    response = client.request(
        "QUERY",
        "/search/",
        json={
            "terms": ["test", "search"],
            "filters": {"category": "books"},
            "limit": 5,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "query" in data
    assert data["query"]["terms"] == ["test", "search"]
    assert data["query"]["filters"] == {"category": "books"}
    assert data["query"]["limit"] == 5


def test_query_method_validation():
    """Test QUERY method with validation errors"""
    app = FastAPI()

    @app.query("/search/")
    def search_items(query: SearchQuery):
        return {"results": []}

    client = TestClient(app)

    # Test with invalid data (missing required field)
    response = client.request(
        "QUERY",
        "/search/",
        json={
            "filters": {"category": "books"}
            # Missing required 'terms' field
        },
    )

    assert response.status_code == 422  # Validation error


def test_query_method_openapi_schema():
    """Test that QUERY method appears in OpenAPI schema"""
    app = FastAPI()

    @app.query("/search/")
    def search_items(query: SearchQuery):
        return {"results": []}

    client = TestClient(app)

    # Get OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi_schema = response.json()

    # Check that the QUERY method is in the schema
    assert "/search/" in openapi_schema["paths"]
    assert "query" in openapi_schema["paths"]["/search/"]

    query_operation = openapi_schema["paths"]["/search/"]["query"]
    assert "requestBody" in query_operation
    assert query_operation["requestBody"]["required"] is True


def test_query_method_with_dependencies():
    """Test QUERY method with FastAPI dependencies"""
    from fastapi import Depends

    app = FastAPI()

    def get_current_user():
        return {"user_id": 123}

    @app.query("/search/", dependencies=[Depends(get_current_user)])
    def search_items(query: SearchQuery):
        return {"results": []}

    client = TestClient(app)

    response = client.request("QUERY", "/search/", json={"terms": ["test"]})

    assert response.status_code == 200


def test_query_method_response_model():
    """Test QUERY method with response model"""
    app = FastAPI()

    class SearchResponse(BaseModel):
        results: List[Dict[str, Any]]
        total: int

    @app.query("/search/", response_model=SearchResponse)
    def search_items(query: SearchQuery):
        return {"results": [{"id": 1, "name": "test"}], "total": 1}

    client = TestClient(app)

    response = client.request("QUERY", "/search/", json={"terms": ["test"]})

    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "total" in data
    assert data["total"] == 1
