import contextlib
from unittest.mock import Mock, patch

import pytest
from fastapi import APIRouter, Depends, FastAPI
from fastapi.testclient import TestClient
from starlette.background import BackgroundTasks

background_task = Mock()


@pytest.fixture(autouse=True)
def background_task_fixture():
    global background_task

    background_task = Mock()

    return background_task


class BackgroundTasksOverride(BackgroundTasks):
    pass


app = FastAPI()


@app.get("/endpoint")
def app_overrides(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task, type(background_tasks))


def nested_dependency(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task, type(background_tasks))


@app.get("/nested-dependency-override")
def nested_dependency_override(nested: str = Depends(nested_dependency)):
    pass


@app.get("/specify-background-tasks-dependency-with-subclass-of-BackgroundTasks")
def explicit_background_tasks_dependency(background_tasks: BackgroundTasksOverride):
    background_tasks.add_task(background_task, type(background_tasks))


router = APIRouter()


@router.get("/router-endpoint")
def router_endpoint(background_tasks: BackgroundTasks):
    background_tasks.add_task(background_task, type(background_tasks))


app.include_router(router)


client = TestClient(app)


@contextlib.contextmanager
def override_background_tasks(app, override_with):
    with patch.dict(app.dependency_overrides, {BackgroundTasks: override_with}):
        yield


def test_normal_app_uses_standard_background_tasks():
    client.get("/endpoint")

    background_task.assert_called_once_with(BackgroundTasks)


@pytest.mark.parametrize(
    "url",
    [
        "/endpoint",
        "/nested-dependency-override",
        "/router-endpoint",
        "/specify-background-tasks-dependency-with-subclass-of-BackgroundTasks",
    ],
)
def test_app_uses_background_task_override(url):
    background_task.reset_mock()

    with override_background_tasks(app, BackgroundTasksOverride):
        client.get(url)

        background_task.assert_called_once_with(BackgroundTasksOverride)
