"""Tests for automatic HEAD method support on GET routes.

RFC 7231 §4.3.2 states that the server SHOULD send the same header fields
in response to a HEAD request as it would have sent if the request had been
a GET.  FastAPI now automatically handles HEAD requests for all GET routes
without adding HEAD to the OpenAPI schema.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


def test_head_returns_200_for_get_route():
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"hello": "world"}

    client = TestClient(app)
    response = client.head("/")
    assert response.status_code == 200
    # HEAD response has no body but preserves headers
    assert response.content == b""
    assert response.headers["content-length"] == "17"
    assert response.headers["content-type"] == "application/json"


def test_head_works_with_path_params():
    app = FastAPI()

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.head("/items/42")
    assert response.status_code == 200
    assert response.content == b""


def test_head_not_in_openapi_schema():
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"hello": "world"}

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    schema = client.get("/openapi.json").json()
    # HEAD should NOT appear in OpenAPI paths
    assert list(schema["paths"]["/"].keys()) == ["get"]
    assert list(schema["paths"]["/items/{item_id}"].keys()) == ["get"]


def test_head_not_added_to_non_get_routes():
    app = FastAPI()

    @app.post("/submit")
    def submit():
        return {"ok": True}

    @app.put("/items/{item_id}")
    def update_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    assert client.head("/submit").status_code == 405
    assert client.head("/items/1").status_code == 405


def test_explicit_head_route_in_schema():
    """When HEAD is explicitly declared, it SHOULD appear in OpenAPI."""
    app = FastAPI()

    @app.head("/health")
    def health_check():
        return JSONResponse(None, headers={"x-status": "ok"})

    client = TestClient(app)
    response = client.head("/health")
    assert response.status_code == 200

    schema = client.get("/openapi.json").json()
    assert "head" in schema["paths"]["/health"]


def test_explicit_get_and_head_via_api_route():
    """When GET and HEAD are both declared via api_route, both work."""
    app = FastAPI()

    @app.api_route("/both", methods=["GET", "HEAD"])
    def both_methods():
        return {"ok": True}

    client = TestClient(app)
    assert client.get("/both").status_code == 200
    assert client.head("/both").status_code == 200


def test_get_still_works_after_auto_head():
    """GET must not be affected by the auto HEAD feature."""
    app = FastAPI()

    @app.get("/data")
    def get_data():
        return {"value": 123}

    client = TestClient(app)
    response = client.get("/data")
    assert response.status_code == 200
    assert response.json() == {"value": 123}


def test_head_with_response_model():
    """HEAD works correctly with routes that have response models."""
    app = FastAPI()

    class Item(BaseModel):
        name: str
        price: float

    @app.get("/item", response_model=Item)
    def get_item():
        return Item(name="Widget", price=9.99)

    client = TestClient(app)
    response = client.head("/item")
    assert response.status_code == 200
    assert response.content == b""
    assert "content-length" in response.headers


def test_head_with_add_api_route():
    """HEAD works for routes added via add_api_route()."""
    app = FastAPI()

    def get_data():
        return {"data": True}

    app.add_api_route("/data", get_data)
    client = TestClient(app)
    response = client.head("/data")
    assert response.status_code == 200
    assert response.content == b""


def test_head_with_router_include():
    """HEAD works for routes added via APIRouter."""
    from fastapi import APIRouter

    app = FastAPI()
    router = APIRouter()

    @router.get("/info")
    def get_info():
        return {"info": "test"}

    app.include_router(router, prefix="/api")
    client = TestClient(app)
    response = client.head("/api/info")
    assert response.status_code == 200
    assert response.content == b""

    # Not in OpenAPI schema
    schema = client.get("/openapi.json").json()
    assert list(schema["paths"]["/api/info"].keys()) == ["get"]
