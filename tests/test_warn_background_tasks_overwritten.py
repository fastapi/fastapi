"""Test that a warning is emitted when a returned Response already has a background
task set and the dependency-injected BackgroundTasks would be silently discarded.

Ref: https://github.com/fastapi/fastapi/issues/11215
"""

import warnings

from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse, Response


def test_warn_when_response_background_overwrites_injected_tasks():
    """When the endpoint returns a Response with its own `background`,
    and the user also injected `BackgroundTasks`, a UserWarning should
    be emitted so the silent data loss is visible."""
    app = FastAPI()

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(lambda: None)
        return Response(
            content="Custom response",
            background=BackgroundTask(lambda: None),
        )

    client = TestClient(app, raise_server_exceptions=False)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        resp = client.get("/")

    assert resp.status_code == 200
    bg_warnings = [w for w in caught if "background" in str(w.message).lower()]
    assert len(bg_warnings) == 1
    assert issubclass(bg_warnings[0].category, UserWarning)


def test_no_warn_when_response_has_no_background():
    """When the endpoint returns a Response without a `background`,
    no warning should be emitted (the injected tasks are attached)."""
    app = FastAPI()
    executed = []

    def bg_task():
        executed.append(True)

    @app.get("/")
    async def endpoint(tasks: BackgroundTasks):
        tasks.add_task(bg_task)
        return JSONResponse(content={"ok": True})

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        resp = client.get("/")

    assert resp.status_code == 200
    bg_warnings = [w for w in caught if "background" in str(w.message).lower()]
    assert len(bg_warnings) == 0
    # The injected task should have run
    assert executed == [True]


def test_no_warn_when_no_injected_background_tasks():
    """When the endpoint returns a Response with a `background` but did
    NOT inject BackgroundTasks, no warning should be emitted."""
    app = FastAPI()
    executed = []

    @app.get("/")
    async def endpoint():
        return Response(
            content="ok",
            background=BackgroundTask(lambda: executed.append(True)),
        )

    client = TestClient(app)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        resp = client.get("/")

    assert resp.status_code == 200
    bg_warnings = [w for w in caught if "background" in str(w.message).lower()]
    assert len(bg_warnings) == 0
    assert executed == [True]
