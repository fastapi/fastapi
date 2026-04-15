"""Test that HEAD requests are automatically supported for GET routes (issue #1773)."""

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_head_for_get_route():
    """HEAD request on a GET route should return 200, not 405."""
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)
    response = client.head("/")
    assert response.status_code == 200
    assert response.headers.get("content-type") is not None


def test_head_for_get_route_with_path():
    """HEAD request on a parameterized GET route should work."""
    app = FastAPI()

    @app.get("/items/{item_id}")
    def read_item(item_id: int):
        return {"item_id": item_id}

    client = TestClient(app)
    response = client.head("/items/42")
    assert response.status_code == 200


def test_head_not_auto_added_for_post():
    """POST routes should NOT automatically support HEAD."""
    app = FastAPI()

    @app.post("/items/")
    def create_item():
        return {"created": True}

    client = TestClient(app)
    response = client.head("/items/")
    assert response.status_code == 405


def test_head_response_has_no_body():
    """HEAD response should have no body content."""
    app = FastAPI()

    @app.get("/")
    def read_root():
        return {"Hello": "World"}

    client = TestClient(app)
    response = client.head("/")
    assert response.status_code == 200
    assert response.content == b""
