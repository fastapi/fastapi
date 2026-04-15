"""Tests for merging injected BackgroundTasks with Response.background.

When a route uses both the injected ``BackgroundTasks`` dependency and returns
a ``Response`` with its own ``background`` parameter, both sets of tasks should
execute.  Previously, the Response's background task silently overwrote the
injected tasks.

See: https://github.com/fastapi/fastapi/issues/11215
"""

from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient
from starlette.background import BackgroundTask
from starlette.background import BackgroundTasks as StarletteBackgroundTasks
from starlette.responses import Response


def test_injected_tasks_not_lost_when_response_has_background():
    """Core bug: injected BackgroundTasks must not be discarded."""
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: results.append("injected"))
        return Response(
            content="ok",
            background=BackgroundTask(lambda: results.append("response")),
        )

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "injected" in results
    assert "response" in results


def test_injected_tasks_run_before_response_tasks():
    """Injected tasks should run first (dependency order), then response tasks."""
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: results.append("first"))
        return Response(
            content="ok",
            background=BackgroundTask(lambda: results.append("second")),
        )

    TestClient(app).get("/")
    assert results == ["first", "second"]


def test_multiple_injected_with_single_response_task():
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: results.append("a"))
        tasks.add_task(lambda: results.append("b"))
        return Response(
            content="ok",
            background=BackgroundTask(lambda: results.append("c")),
        )

    TestClient(app).get("/")
    assert results == ["a", "b", "c"]


def test_injected_with_response_background_tasks():
    """Response.background can also be a BackgroundTasks (not just single task)."""
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: results.append("injected"))
        bg = StarletteBackgroundTasks()
        bg.add_task(lambda: results.append("resp1"))
        bg.add_task(lambda: results.append("resp2"))
        return Response(content="ok", background=bg)

    TestClient(app).get("/")
    assert results == ["injected", "resp1", "resp2"]


def test_only_injected_tasks_still_works():
    """No regression: injected tasks without Response.background still work."""
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: results.append("only"))
        return Response(content="ok")

    TestClient(app).get("/")
    assert results == ["only"]


def test_only_response_background_still_works():
    """No regression: Response.background without injected tasks still works."""
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint():
        return Response(
            content="ok",
            background=BackgroundTask(lambda: results.append("only")),
        )

    TestClient(app).get("/")
    assert results == ["only"]


def test_no_background_tasks_at_all():
    """No regression: routes without any background tasks work normally."""
    app = FastAPI()

    @app.get("/")
    async def endpoint():
        return Response(content="ok")

    response = TestClient(app).get("/")
    assert response.status_code == 200


def test_normal_return_with_injected_tasks():
    """No regression: non-Response returns with injected tasks still work."""
    results: list[str] = []
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: results.append("normal"))
        return {"ok": True}

    TestClient(app).get("/")
    assert results == ["normal"]
