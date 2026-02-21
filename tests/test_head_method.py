"""Test automatic HEAD method support for GET routes."""

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_head_method_automatically_supported():
    """HEAD should work automatically for all GET endpoints."""
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"hello": "world"}

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)

    # GET should work
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}

    # HEAD should work and return same headers but no body
    head_response = client.head("/")
    assert head_response.status_code == 200
    assert head_response.content == b""
    assert head_response.headers.get("content-type") == "application/json"
    assert int(head_response.headers.get("content-length")) > 0

    # HEAD with path params
    head_response = client.head("/items/42")
    assert head_response.status_code == 200
    assert head_response.content == b""


def test_head_not_in_openapi_schema():
    """HEAD should not appear in OpenAPI schema - it's implicit per HTTP semantics."""
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"hello": "world"}

    @app.post("/items")
    def create_item():
        return {"created": True}

    schema = app.openapi()

    # GET should be in schema
    assert "get" in schema["paths"]["/"]

    # HEAD should NOT be in schema
    assert "head" not in schema["paths"]["/"]

    # POST shouldn't have HEAD
    assert "post" in schema["paths"]["/items"]
    assert "head" not in schema["paths"]["/items"]


def test_head_not_added_for_post_routes():
    """HEAD should NOT be added for non-GET routes."""
    app = FastAPI()

    @app.post("/items")
    def create_item():
        return {"created": True}

    client = TestClient(app)

    # POST should work
    response = client.post("/items")
    assert response.status_code == 200

    # HEAD should NOT work for POST-only endpoint
    head_response = client.head("/items")
    assert head_response.status_code == 405


def test_explicit_head_route():
    """User can still define explicit HEAD routes."""
    app = FastAPI()

    @app.head("/custom")
    def custom_head():
        return None

    client = TestClient(app)

    response = client.head("/custom")
    assert response.status_code == 200


def test_head_preserves_response_headers():
    """HEAD response should have the same headers as GET."""
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"data": "x" * 100}  # Longer response

    client = TestClient(app)

    get_response = client.get("/")
    head_response = client.head("/")

    assert head_response.headers.get("content-type") == get_response.headers.get(
        "content-type"
    )
    assert head_response.headers.get("content-length") == get_response.headers.get(
        "content-length"
    )
