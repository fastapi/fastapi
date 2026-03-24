"""Test using special types (Response, Request, BackgroundTasks) as dependency annotations.

These tests verify that special FastAPI types can be used with Depends() annotations
and that the dependency injection system properly handles them.
"""

from typing import Annotated

from fastapi import BackgroundTasks, Depends, FastAPI, Request, Response
from fastapi.responses import JSONResponse
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


def test_response_dependency_returns_different_response_instance():
    """Dependency that returns a different Response instance should work.

    When a dependency returns a new Response object (e.g., JSONResponse) instead
    of modifying the injected one, the returned response should be used and any
    modifications to it in the endpoint should be preserved.
    """
    app = FastAPI()

    def default_response() -> Response:
        response = JSONResponse(content={"status": "ok"})
        response.headers["X-Custom"] = "initial"
        return response

    @app.get("/")
    def endpoint(response: Annotated[Response, Depends(default_response)]):
        response.headers["X-Custom"] = "modified"
        return response

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
    assert resp.headers.get("X-Custom") == "modified"


# Tests for Request type hint with Depends
def test_request_with_depends_annotated():
    """Request type hint should work in dependency chain."""
    app = FastAPI()

    def extract_request_info(request: Request) -> dict:
        return {
            "path": request.url.path,
            "user_agent": request.headers.get("user-agent", "unknown"),
        }

    @app.get("/")
    def endpoint(
        info: Annotated[dict, Depends(extract_request_info)],
    ):
        return info

    client = TestClient(app)
    resp = client.get("/", headers={"user-agent": "test-agent"})

    assert resp.status_code == 200
    assert resp.json() == {"path": "/", "user_agent": "test-agent"}


# Tests for BackgroundTasks type hint with Depends
def test_background_tasks_with_depends_annotated():
    """BackgroundTasks type hint should work with Annotated[BackgroundTasks, Depends(...)]."""
    app = FastAPI()
    task_results = []

    def background_task(message: str):
        task_results.append(message)

    def add_background_task(background_tasks: BackgroundTasks) -> BackgroundTasks:
        background_tasks.add_task(background_task, "from dependency")
        return background_tasks

    @app.get("/")
    def endpoint(
        background_tasks: Annotated[BackgroundTasks, Depends(add_background_task)],
    ):
        background_tasks.add_task(background_task, "from endpoint")
        return {"status": "ok"}

    client = TestClient(app)
    resp = client.get("/")

    assert resp.status_code == 200
    assert "from dependency" in task_results
    assert "from endpoint" in task_results
