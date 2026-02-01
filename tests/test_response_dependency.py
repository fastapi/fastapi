"""Test using Response type hint as dependency annotation."""

from typing import Annotated

from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient


def test_response_with_depends_annotated():
    """Response type hint should work with Annotated[Response, Depends(...)]."""
    app = FastAPI()

    def modify_response(response: Response) -> Response:
        response.headers["X-Custom"] = "modified"
        return response

    @app.get("/")
    def endpoint(response: Annotated[Response, Depends(modify_response)]):
        return {"status": "ok"}

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    assert resp.headers.get("X-Custom") == "modified"


def test_response_with_depends_default():
    """Response type hint should work with Response = Depends(...)."""
    app = FastAPI()

    def modify_response(response: Response) -> Response:
        response.headers["X-Custom"] = "modified"
        return response

    @app.get("/")
    def endpoint(response: Response = Depends(modify_response)):
        return {"status": "ok"}

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    assert resp.headers.get("X-Custom") == "modified"


def test_response_without_depends():
    """Regular Response injection should still work."""
    app = FastAPI()

    @app.get("/")
    def endpoint(response: Response):
        response.headers["X-Direct"] = "set"
        return {"status": "ok"}

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    assert resp.headers.get("X-Direct") == "set"


def test_response_dependency_chain():
    """Response dependency should work in a chain of dependencies."""
    app = FastAPI()

    def first_modifier(response: Response) -> Response:
        response.headers["X-First"] = "1"
        return response

    def second_modifier(
        response: Annotated[Response, Depends(first_modifier)],
    ) -> Response:
        response.headers["X-Second"] = "2"
        return response

    @app.get("/")
    def endpoint(response: Annotated[Response, Depends(second_modifier)]):
        return {"status": "ok"}

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.headers.get("X-First") == "1"
    assert resp.headers.get("X-Second") == "2"
