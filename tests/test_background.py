from fastapi import FastAPI
from starlette.background import BackgroundTask, BackgroundTasks
from starlette.testclient import TestClient


def test_multiple_tasks_fastapistyle():
    TASK_COUNTER = 0

    def increment(amount):
        nonlocal TASK_COUNTER
        TASK_COUNTER += amount

    app = FastAPI()

    @app.get("/")
    async def root():
        tasks = BackgroundTasks()
        tasks.add_task(increment, amount=1)
        tasks.add_task(increment, amount=2)
        tasks.add_task(increment, amount=3)
        message = {"status": "successful", "background": tasks}
        return message
        # message = {'status': 'successful'}
        # return JSONResponse(message, background=tasks)

    client = TestClient(app)
    response = client.get("/")
    assert response.json() == {"status": "successful"}
    assert TASK_COUNTER == 1 + 2 + 3


def test_async_task():
    TASK_COMPLETE = False

    async def async_task():
        nonlocal TASK_COMPLETE
        TASK_COMPLETE = True

    app = FastAPI()

    @app.get("/")
    async def root():
        task = BackgroundTask(async_task)
        return {"status": "successful", "background": task}

    client = TestClient(app)
    response = client.get("/")
    assert response.json() == {"status": "successful"}
    assert TASK_COMPLETE
