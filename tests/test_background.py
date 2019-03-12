from starlette.background import BackgroundTasks
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from fastapi import FastAPI, Depends


def test_multiple_tasks():
    TASK_COUNTER = 0
    def increment(amount):
        nonlocal TASK_COUNTER
        TASK_COUNTER += amount
    app = FastAPI()
    @app.route("/")
    async def root(request: Request):
        tasks = BackgroundTasks()
        tasks.add_task(increment, amount=1)
        tasks.add_task(increment, amount=2)
        tasks.add_task(increment, amount=3)
        message = {'status': 'successful'}
        return JSONResponse(message, background=tasks)
    client = TestClient(app)
    response = client.get("/")
    assert response.json() == {'status': 'successful'}
    assert TASK_COUNTER == 1 + 2 + 3

def test_multiple_tasks2():
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
        message = {'status': 'successful'}

        return JSONResponse(message, background=tasks)
    client = TestClient(app)
    response = client.get("/")
    assert response.json() == {'status': 'successful'}
    assert TASK_COUNTER == 1 + 2 + 3

