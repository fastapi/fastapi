#!/usr/bin/env python3

"""
Tests for the QUERY HTTP method in FastAPI.

This test file follows the FastAPI test patterns and should be compatible
with the existing test suite.
"""

# Ensure compatibility across Python versions
from typing import List, Optional

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


def test_query_method_basic():
    app = FastAPI()

    @app.query("/query")
    def query_endpoint():
        return {"method": "QUERY", "message": "success"}

    client = TestClient(app)
    response = client.request("QUERY", "/query")

    assert response.status_code == 200
    assert response.json() == {"method": "QUERY", "message": "success"}


def test_query_method_with_body():
    app = FastAPI()

    class QueryData(BaseModel):
        query: str
        limit: Optional[int] = 10

    @app.query("/search")
    def search_endpoint(data: QueryData):
        return {"query": data.query, "limit": data.limit}

    client = TestClient(app)
    response = client.request(
        "QUERY", "/search", json={"query": "test search", "limit": 5}
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["query"] == "test search"
    assert json_data["limit"] == 5


def test_query_method_with_response_model():
    app = FastAPI()

    class QueryRequest(BaseModel):
        term: str

    class SearchResult(BaseModel):
        results: List[str]
        count: int

    @app.query("/search", response_model=SearchResult)
    def search_with_model(request: QueryRequest):
        results = [f"result_{i}_{request.term}" for i in range(3)]
        return {"results": results, "count": len(results)}

    client = TestClient(app)
    response = client.request("QUERY", "/search", json={"term": "fastapi"})

    assert response.status_code == 200
    json_data = response.json()
    assert "results" in json_data
    assert "count" in json_data
    assert json_data["count"] == 3
    assert all("fastapi" in result for result in json_data["results"])


def test_query_method_with_status_code():
    app = FastAPI()

    @app.query("/created", status_code=201)
    def created_endpoint():
        return {"status": "created"}

    client = TestClient(app)
    response = client.request("QUERY", "/created")

    assert response.status_code == 201
    assert response.json()["status"] == "created"


def test_query_method_with_dependencies():
    app = FastAPI()

    def get_current_user():
        return {"user_id": "12345", "username": "testuser"}

    @app.query("/user-query")
    def user_query_endpoint(user: dict = Depends(get_current_user)):
        return {"user": user, "method": "QUERY"}

    client = TestClient(app)
    response = client.request("QUERY", "/user-query")

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["method"] == "QUERY"
    assert json_data["user"]["user_id"] == "12345"


def test_query_method_with_tags():
    app = FastAPI()

    @app.query("/tagged-query", tags=["search", "query"])
    def tagged_query():
        return {"tags": ["search", "query"]}

    client = TestClient(app)
    response = client.request("QUERY", "/tagged-query")

    assert response.status_code == 200
    assert response.json()["tags"] == ["search", "query"]


def test_query_method_openapi_schema():
    app = FastAPI()

    class QueryData(BaseModel):
        search_term: str
        filters: Optional[dict] = None

    @app.query("/openapi-query")
    def openapi_query(data: QueryData):
        return {"received": data.search_term}

    openapi_schema = app.openapi()

    # Verify the endpoint is in the schema
    assert "/openapi-query" in openapi_schema["paths"]

    # Verify QUERY method is documented
    path_item = openapi_schema["paths"]["/openapi-query"]
    assert "query" in path_item


def test_query_method_vs_post_comparison():
    """Test that QUERY behaves similarly to POST but with different method."""
    app = FastAPI()

    class RequestData(BaseModel):
        data: str

    @app.post("/post-endpoint")
    def post_endpoint(request: RequestData):
        return {"method": "POST", "data": request.data}

    @app.query("/query-endpoint")
    def query_endpoint(request: RequestData):
        return {"method": "QUERY", "data": request.data}

    client = TestClient(app)

    test_data = {"data": "test content"}

    post_response = client.post("/post-endpoint", json=test_data)
    query_response = client.request("QUERY", "/query-endpoint", json=test_data)

    assert post_response.status_code == 200
    assert query_response.status_code == 200

    post_json = post_response.json()
    query_json = query_response.json()

    # Both should return same data, just different method indication
    assert post_json["data"] == query_json["data"] == "test content"
    assert post_json["method"] == "POST"
    assert query_json["method"] == "QUERY"


def test_query_method_with_path_parameters():
    app = FastAPI()

    class QueryFilter(BaseModel):
        status: str
        limit: int

    @app.query("/items/{item_id}")
    def query_item(item_id: int, filters: QueryFilter):
        return {"item_id": item_id, "filters": filters}

    client = TestClient(app)
    response = client.request(
        "QUERY", "/items/123", json={"status": "active", "limit": 10}
    )

    assert response.status_code == 200
    json_data = response.json()
    assert json_data["item_id"] == 123
    assert json_data["filters"]["status"] == "active"
    assert json_data["filters"]["limit"] == 10


def test_query_method_error_handling():
    app = FastAPI()

    class QueryData(BaseModel):
        required_field: str

    @app.query("/error-test")
    def error_test(data: QueryData):
        return {"received": data.required_field}

    client = TestClient(app)

    # Test missing required field
    response = client.request("QUERY", "/error-test", json={})
    assert response.status_code == 422  # Validation error

    # Test valid request
    response = client.request("QUERY", "/error-test", json={"required_field": "value"})
    assert response.status_code == 200
    assert response.json()["received"] == "value"
