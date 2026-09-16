from fastapi import BackgroundTasks, Depends, FastAPI, Response
from fastapi.testclient import TestClient
from starlette.background import BackgroundTask
from starlette.background import BackgroundTasks as StarletteBackgroundTasks


def test_injected_background_tasks_with_response_background_task():
    execution_order: list[str] = []

    def task_injected():
        execution_order.append("injected")

    def task_response():
        execution_order.append("response")

    app = FastAPI()

    @app.get("/test")
    def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_injected)
        return Response(content="ok", background=BackgroundTask(task_response))

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == ["injected", "response"]


def test_injected_background_tasks_with_response_background_tasks_collection():
    execution_order: list[str] = []

    def task_injected_1():
        execution_order.append("injected_1")

    def task_injected_2():
        execution_order.append("injected_2")

    def task_response_1():
        execution_order.append("response_1")

    def task_response_2():
        execution_order.append("response_2")

    app = FastAPI()

    @app.get("/test")
    def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_injected_1)
        background_tasks.add_task(task_injected_2)
        resp_tasks = StarletteBackgroundTasks(
            [BackgroundTask(task_response_1), BackgroundTask(task_response_2)]
        )
        return Response(content="ok", background=resp_tasks)

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == [
        "injected_1",
        "injected_2",
        "response_1",
        "response_2",
    ]


def test_injected_background_tasks_with_same_instance():
    execution_order: list[str] = []

    def task_injected():
        execution_order.append("injected")

    app = FastAPI()

    @app.get("/test")
    def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_injected)
        return Response(content="ok", background=background_tasks)

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == ["injected"]


def test_dependency_background_tasks_with_response_background():
    execution_order: list[str] = []

    def task_dep():
        execution_order.append("dep")

    def task_response():
        execution_order.append("response")

    def dep(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_dep)

    app = FastAPI()

    @app.get("/test")
    def endpoint(_: None = Depends(dep)):
        return Response(content="ok", background=BackgroundTask(task_response))

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == ["dep", "response"]


def test_dependency_and_endpoint_tasks_with_response_tasks():
    execution_order: list[str] = []

    def task_dep():
        execution_order.append("dep")

    def task_endpoint():
        execution_order.append("endpoint")

    def task_response_1():
        execution_order.append("response_1")

    def task_response_2():
        execution_order.append("response_2")

    def dep(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_dep)

    app = FastAPI()

    @app.get("/test")
    def endpoint(background_tasks: BackgroundTasks, _: None = Depends(dep)):
        background_tasks.add_task(task_endpoint)
        resp_tasks = BackgroundTasks()
        resp_tasks.add_task(task_response_1)
        resp_tasks.add_task(task_response_2)
        return Response(content="ok", background=resp_tasks)

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == ["dep", "endpoint", "response_1", "response_2"]


def test_no_injected_tasks_with_response_background():
    execution_order: list[str] = []

    def task_response():
        execution_order.append("response")

    app = FastAPI()

    @app.get("/test")
    def endpoint():
        return Response(content="ok", background=BackgroundTask(task_response))

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == ["response"]


def test_injected_tasks_without_response_background():
    execution_order: list[str] = []

    def task_injected():
        execution_order.append("injected")

    app = FastAPI()

    @app.get("/test")
    def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(task_injected)
        return Response(content="ok")

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == ["injected"]


def test_async_and_sync_background_tasks():
    execution_order: list[str] = []

    async def async_injected():
        execution_order.append("async_injected")

    def sync_injected():
        execution_order.append("sync_injected")

    async def async_response():
        execution_order.append("async_response")

    def sync_response():
        execution_order.append("sync_response")

    app = FastAPI()

    @app.get("/test")
    async def endpoint(background_tasks: BackgroundTasks):
        background_tasks.add_task(async_injected)
        background_tasks.add_task(sync_injected)
        resp_tasks = BackgroundTasks()
        resp_tasks.add_task(async_response)
        resp_tasks.add_task(sync_response)
        return Response(content="ok", background=resp_tasks)

    client = TestClient(app)
    response = client.get("/test")
    assert response.status_code == 200
    assert response.text == "ok"
    assert execution_order == [
        "async_injected",
        "sync_injected",
        "async_response",
        "sync_response",
    ]
