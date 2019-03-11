from starlette.background import BackgroundTask, BackgroundTasks
from starlette.responses import Response
from starlette.testclient import TestClient


def test_async_task():
    TASK_COMPLETE = False

    async def async_task():
        nonlocal TASK_COMPLETE
        TASK_COMPLETE = True

    task = BackgroundTask(async_task)

    def app(scope):
        async def asgi(receive, send):
            response = Response(
                "task initiated", media_type="text/plain", background=task
            )
            await response(receive, send)

        return asgi

    client = TestClient(app)
    response = client.get("/")
    assert response.text == "task initiated"
    assert TASK_COMPLETE


def test_sync_task():
    TASK_COMPLETE = False

    def sync_task():
        nonlocal TASK_COMPLETE
        TASK_COMPLETE = True

    task = BackgroundTask(sync_task)

    def app(scope):
        async def asgi(receive, send):
            response = Response(
                "task initiated", media_type="text/plain", background=task
            )
            await response(receive, send)

        return asgi

    client = TestClient(app)
    response = client.get("/")
    assert response.text == "task initiated"
    assert TASK_COMPLETE


def test_multiple_tasks():
    TASK_COUNTER = 0

    def increment(amount):
        nonlocal TASK_COUNTER
        TASK_COUNTER += amount

    def app(scope):
        async def asgi(receive, send):
            tasks = BackgroundTasks()
            tasks.add_task(increment, amount=1)
            tasks.add_task(increment, amount=2)
            tasks.add_task(increment, amount=3)
            response = Response(
                "tasks initiated", media_type="text/plain", background=tasks
            )
            await response(receive, send)

        return asgi

    client = TestClient(app)
    response = client.get("/")
    assert response.text == "tasks initiated"
    assert TASK_COUNTER == 1 + 2 + 3