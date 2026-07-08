"""
Tests for the QUERY HTTP method in FastAPI.

The QUERY method is a custom HTTP method designed for structured query operations.
"""

import pytest
from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient


class TestQueryHttpMethod:
    """Tests for the QUERY HTTP method."""

    @pytest.fixture
    def app(self):
        """Create a test FastAPI application."""
        app = FastAPI()

        @app.query("/search")
        def search(q: str, limit: int = 10):
            """Simple search endpoint using QUERY method."""
            return {
                "query": q,
                "limit": limit,
                "items": [{"id": 1, "name": f"Result for {q}"}],
            }

        return app

    def test_query_method_basic(self, app):
        """Test basic QUERY method request."""
        client = TestClient(app)
        response = client.request("QUERY", "/search?q=python")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "python"
        assert data["limit"] == 10

    def test_query_method_with_params(self, app):
        """Test QUERY method with multiple parameters."""
        client = TestClient(app)
        response = client.request("QUERY", "/search?q=fastapi&limit=20")
        assert response.status_code == 200
        data = response.json()
        assert data["query"] == "fastapi"
        assert data["limit"] == 20

    def test_query_method_default_params(self, app):
        """Test QUERY method uses default parameter values."""
        client = TestClient(app)
        response = client.request("QUERY", "/search?q=default")
        assert response.status_code == 200
        data = response.json()
        assert data["limit"] == 10

    @pytest.fixture
    def router_app(self):
        """Test QUERY method with APIRouter."""
        app = FastAPI()
        router = APIRouter()

        @router.query("/items/search")
        def search_items(name: str, skip: int = 0):
            """Search for items."""
            return {
                "search_term": name,
                "skip": skip,
                "found_items": [{"id": 1, "name": name}],
            }

        app.include_router(router)
        return app

    def test_query_method_with_router(self, router_app):
        """Test QUERY method with APIRouter."""
        client = TestClient(router_app)
        response = client.request("QUERY", "/items/search?name=widget&skip=5")
        assert response.status_code == 200
        data = response.json()
        assert data["search_term"] == "widget"
        assert data["skip"] == 5

    @pytest.fixture
    def tagged_app(self):
        """Test QUERY method with tags and metadata."""
        app = FastAPI()

        @app.query(
            "/search",
            tags=["search"],
            summary="Search endpoint",
            description="Search for items using QUERY method",
        )
        def search(q: str):
            return {"query": q, "results": []}

        return app

    def test_query_method_with_tags(self, tagged_app):
        """Test QUERY method request succeeds."""
        client = TestClient(tagged_app)
        response = client.request("QUERY", "/search?q=tagged")
        assert response.status_code == 200
        assert response.json()["query"] == "tagged"

    def test_query_method_openapi_documentation(self, tagged_app):
        """Test that QUERY method appears in OpenAPI documentation."""
        client = TestClient(tagged_app)
        response = client.get("/openapi.json")
        assert response.status_code == 200
        openapi = response.json()
        assert "/search" in openapi["paths"]

    @pytest.fixture
    def multiple_query_methods(self):
        """Test multiple QUERY endpoints."""
        app = FastAPI()

        @app.query("/users/search")
        def search_users(name: str):
            return {"type": "users", "query": name}

        @app.query("/posts/search")
        def search_posts(title: str):
            return {"type": "posts", "query": title}

        return app

    def test_multiple_query_endpoints(self, multiple_query_methods):
        """Test multiple QUERY method endpoints."""
        client = TestClient(multiple_query_methods)

        # Test first endpoint
        response1 = client.request("QUERY", "/users/search?name=alice")
        assert response1.status_code == 200
        assert response1.json()["type"] == "users"

        # Test second endpoint
        response2 = client.request("QUERY", "/posts/search?title=hello")
        assert response2.status_code == 200
        assert response2.json()["type"] == "posts"


class TestQueryMethodIntegration:
    """Test integration with FastAPI features."""

    @pytest.fixture
    def featured_app(self):
        """App with various FastAPI features."""
        app = FastAPI()

        @app.query("/search", status_code=200, deprecated=False)
        def search(q: str, limit: int = 10):
            """Search endpoint with custom config."""
            return {"q": q, "limit": limit}

        @app.get("/items")
        def list_items():
            """GET endpoint for comparison."""
            return {"items": []}

        return app

    def test_query_and_get_coexist(self, featured_app):
        """Test that QUERY and GET methods can coexist."""
        client = TestClient(featured_app)

        # GET should work
        get_response = client.get("/items")
        assert get_response.status_code == 200

        # QUERY should also work
        query_response = client.request("QUERY", "/search?q=test")
        assert query_response.status_code == 200

    def test_query_method_with_status_code(self, featured_app):
        """Test QUERY method respects status_code parameter."""
        client = TestClient(featured_app)
        response = client.request("QUERY", "/search?q=test")
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
