"""
Test that background tasks from injected BackgroundTasks and Response.background are both executed.
Related to issue #11215
"""

from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import Response
from fastapi.testclient import TestClient

app = FastAPI()

# Track which background tasks were executed
executed_tasks = []


def task_from_injected():
    executed_tasks.append("injected")


def task_from_response():
    executed_tasks.append("response")


@app.get("/both-tasks")
async def endpoint_with_both_tasks(tasks: BackgroundTasks):
    """Endpoint that uses both injected BackgroundTasks and Response.background"""
    tasks.add_task(task_from_injected)
    return Response(
        content="Custom response",
        background=BackgroundTasks(tasks=[]),
    )


@app.get("/both-tasks-populated")
async def endpoint_with_both_tasks_populated(tasks: BackgroundTasks):
    """Endpoint where both injected and response have background tasks"""
    tasks.add_task(task_from_injected)
    response_bg = BackgroundTasks()
    response_bg.add_task(task_from_response)
    return Response(
        content="Custom response",
        background=response_bg,
    )


@app.get("/only-injected")
async def endpoint_with_only_injected(tasks: BackgroundTasks):
    """Endpoint that only uses injected BackgroundTasks"""
    tasks.add_task(task_from_injected)
    return Response(content="Custom response")


@app.get("/only-response")
async def endpoint_with_only_response():
    """Endpoint that only uses Response.background"""
    response_bg = BackgroundTasks()
    response_bg.add_task(task_from_response)
    return Response(
        content="Custom response",
        background=response_bg,
    )


def test_injected_tasks_not_lost_when_response_has_empty_background():
    """Test that injected background tasks are preserved even when Response has empty background"""
    global executed_tasks
    executed_tasks = []

    client = TestClient(app)
    response = client.get("/both-tasks")

    assert response.status_code == 200
    # Both tasks should be executed
    assert "injected" in executed_tasks, "Injected task was not executed"


def test_both_tasks_executed_when_both_populated():
    """Test that both injected and response background tasks are executed"""
    global executed_tasks
    executed_tasks = []

    client = TestClient(app)
    response = client.get("/both-tasks-populated")

    assert response.status_code == 200
    # Both tasks should be executed
    assert "injected" in executed_tasks, "Injected task was not executed"
    assert "response" in executed_tasks, "Response task was not executed"


def test_only_injected_tasks_work():
    """Test that only injected background tasks work when no Response.background"""
    global executed_tasks
    executed_tasks = []

    client = TestClient(app)
    response = client.get("/only-injected")

    assert response.status_code == 200
    assert "injected" in executed_tasks


def test_only_response_tasks_work():
    """Test that only response background tasks work"""
    global executed_tasks
    executed_tasks = []

    client = TestClient(app)
    response = client.get("/only-response")

    assert response.status_code == 200
    assert "response" in executed_tasks
