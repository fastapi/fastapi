"""
Tests for automatic HEAD method support on GET routes (issue #1773).

FastAPI should automatically handle HEAD requests on any route that supports
GET, mirroring Starlette's behaviour (starlette/routing.py Route.__init__).
The HEAD method should be supported at the routing level but must NOT appear
as a separate operation in the OpenAPI schema.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/{item_id}")
def get_item(item_id: str):
    return {"item_id": item_id}


@app.get("/ping")
def ping():
    return {"status": "ok"}


@app.post("/submit")
def submit():
    return {"result": "created"}


client = TestClient(app)


# ---------------------------------------------------------------------------
# Routing: HEAD should succeed for GET routes
# ---------------------------------------------------------------------------


def test_head_on_get_route_returns_200():
    response = client.head("/items/foo")
    assert response.status_code == 200, response.text


def test_head_on_get_route_returns_empty_body():
    """HEAD responses must have no body."""
    response = client.head("/items/foo")
    assert response.content == b""


def test_head_response_has_same_headers_as_get():
    """Content-Type set on GET should also be present on HEAD."""
    get_response = client.get("/ping")
    head_response = client.head("/ping")
    assert head_response.status_code == 200
    assert head_response.headers.get("content-type") == get_response.headers.get(
        "content-type"
    )


def test_post_route_still_works():
    """POST on the submit route must still work normally."""
    response = client.post("/submit")
    assert response.status_code == 200
    assert response.json() == {"result": "created"}


def test_head_on_post_only_route_returns_405():
    """Routes without GET must still return 405 for HEAD."""
    response = client.head("/submit")
    assert response.status_code == 405


def test_get_still_works_after_head_support():
    """Adding HEAD must not break GET."""
    response = client.get("/items/bar")
    assert response.status_code == 200
    assert response.json() == {"item_id": "bar"}


# ---------------------------------------------------------------------------
# OpenAPI: HEAD must NOT appear as a separate operation in the schema
# ---------------------------------------------------------------------------


def test_head_not_in_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    for path, path_item in schema.get("paths", {}).items():
        assert "head" not in path_item, (
            f"HEAD should not be a documented OpenAPI operation, "
            f"but found it at path '{path}'"
        )


def test_get_present_in_openapi_schema():
    response = client.get("/openapi.json")
    schema = response.json()
    assert "get" in schema["paths"]["/items/{item_id}"]
    assert "get" in schema["paths"]["/ping"]
