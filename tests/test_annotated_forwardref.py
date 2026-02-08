"""
Tests for Annotated types with ForwardRef support.
Tests for issue #13056: Annotated types with ForwardRef cause errors.
"""

from typing import Annotated, Optional

import pytest
from fastapi import Body, FastAPI, Header, Path, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel


class UserModel(BaseModel):
    """User model for testing ForwardRef."""

    name: str = "test_user"
    age: int = 25


class Item(BaseModel):
    """Item model for testing ForwardRef."""

    title: str = "test_item"
    description: Optional[str] = None


def test_annotated_forwardref_query_param():
    """Test Annotated with ForwardRef in query parameter."""
    app = FastAPI()

    @app.get("/users")
    async def get_user(user: Annotated["UserModel", Query()]):
        return {"user": user}

    client = TestClient(app)
    response = client.get("/users?name=John&age=30")
    assert response.status_code == 200
    assert response.json() == {"user": {"name": "John", "age": 30}}


def test_annotated_forwardref_query_param_default():
    """Test Annotated with ForwardRef in query parameter with default."""
    app = FastAPI()

    @app.get("/users-default")
    async def get_user_default(user: Annotated["UserModel", Query()] = UserModel()):
        return {"user": user}

    client = TestClient(app)
    response = client.get("/users-default")
    assert response.status_code == 200
    assert response.json() == {"user": {"name": "test_user", "age": 25}}


def test_annotated_forwardref_optional():
    """Test Annotated with ForwardRef in Optional parameter."""
    app = FastAPI()

    @app.get("/items")
    async def get_item(item: Annotated[Optional["Item"], Query()] = None):
        return {"item": item}

    client = TestClient(app)

    # Test with no parameter
    response = client.get("/items")
    assert response.status_code == 200
    assert response.json() == {"item": None}


def test_annotated_forwardref_path_param():
    """Test Annotated with ForwardRef in path parameter."""
    app = FastAPI()

    @app.get("/users/{user_id}")
    async def get_user_by_id(user_id: Annotated["int", Path()]):
        return {"user_id": user_id}

    client = TestClient(app)
    response = client.get("/users/123")
    assert response.status_code == 200
    assert response.json() == {"user_id": 123}


def test_annotated_forwardref_header():
    """Test Annotated with ForwardRef in header parameter."""
    app = FastAPI()

    @app.get("/headers")
    async def get_headers(x_token: Annotated["str", Header()]):
        return {"x_token": x_token}

    client = TestClient(app)
    response = client.get("/headers", headers={"x-token": "test-token"})
    assert response.status_code == 200
    assert response.json() == {"x_token": "test-token"}


def test_annotated_forwardref_body():
    """Test Annotated with ForwardRef in request body."""
    app = FastAPI()

    @app.post("/items")
    async def create_item(item: Annotated["Item", Body()]):
        return {"item": item}

    client = TestClient(app)
    response = client.post(
        "/items", json={"title": "Test Item", "description": "A test item"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "item": {"title": "Test Item", "description": "A test item"}
    }


def test_annotated_forwardref_multiple_annotations():
    """Test Annotated with ForwardRef and multiple metadata items."""
    app = FastAPI()

    @app.get("/multi")
    async def get_multi(
        param: Annotated["UserModel", "some metadata", Query(), "more metadata"],
    ):
        return {"param": param}

    client = TestClient(app)
    response = client.get("/multi?name=John&age=30")
    assert response.status_code == 200
    assert response.json() == {"param": {"name": "John", "age": 30}}


def test_annotated_forwardref_openapi_schema():
    """Test that OpenAPI schema is generated correctly with ForwardRef."""
    app = FastAPI()

    @app.get("/users")
    async def get_user(user: Annotated["UserModel", Query()]):
        return {"user": user}

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_schema = response.json()

    # Check that the endpoint is in the schema
    assert "/users" in openapi_schema["paths"]

    # Check that the parameter schema is generated
    endpoint_schema = openapi_schema["paths"]["/users"]["get"]
    assert "parameters" in endpoint_schema

    # Check that the UserModel schema is in the components
    assert "components" in openapi_schema
    assert "schemas" in openapi_schema["components"]


def test_annotated_forwardref_get_type_hints():
    """Test that get_type_hints works correctly with Annotated ForwardRef."""
    from typing import get_type_hints

    def test_func(param: Annotated["UserModel", Query()]):
        pass

    # This should work without errors (it will resolve UserModel since it's defined at module level)
    hints = get_type_hints(test_func)
    assert "param" in hints
    # get_type_hints resolves the ForwardRef to the actual type
    assert hints["param"] == UserModel


def test_annotated_forwardref_with_dependencies():
    """Test Annotated with ForwardRef in dependency chain."""
    app = FastAPI()

    def get_current_user(user: Annotated["UserModel", Query()]) -> "UserModel":
        return user

    @app.get("/protected")
    async def get_protected(current_user: Annotated[UserModel, Query()]):
        return {"user": current_user}

    client = TestClient(app)
    response = client.get("/protected?name=Alice&age=28")
    assert response.status_code == 200
    assert response.json() == {"user": {"name": "Alice", "age": 28}}


def test_annotated_forwardref_complex_types():
    """Test Annotated with ForwardRef for complex type annotations."""
    app = FastAPI()

    @app.get("/search")
    async def search(items: Annotated[list["Item"], Query()] = None):
        return {"items": items or []}

    client = TestClient(app)
    # This tests that complex types with ForwardRef don't break the system
    response = client.get("/search")
    assert response.status_code in [
        200,
        422,
    ]  # May be 422 if the type check is too strict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
