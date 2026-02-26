from fastapi import BackgroundTasks, FastAPI
from fastapi.testclient import TestClient
from starlette.background import BackgroundTask
from starlette.responses import JSONResponse

results: list[str] = []


def task_from_injection():
    results.append("injected")


def task_from_response():
    results.append("response")


def test_merge_injected_and_response_background_tasks():
    """Both injected BackgroundTasks and Response background tasks should run."""
    app = FastAPI()

    @app.get("/")
    async def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_from_injection)
        return JSONResponse(
            {"status": "ok"},
            background=BackgroundTask(task_from_response),
        )

    results.clear()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "injected" in results
    assert "response" in results


def test_only_injected_background_tasks():
    """When Response has no background, injected tasks still run."""
    app = FastAPI()

    @app.get("/")
    async def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_from_injection)
        return JSONResponse({"status": "ok"})

    results.clear()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "injected" in results
    assert "response" not in results


def test_only_response_background_task():
    """When no BackgroundTasks are injected, response background task runs."""
    app = FastAPI()

    @app.get("/")
    async def endpoint():
        return JSONResponse(
            {"status": "ok"},
            background=BackgroundTask(task_from_response),
        )

    results.clear()
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "response" in results
    assert "injected" not in results
