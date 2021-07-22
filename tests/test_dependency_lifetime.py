from typing import Callable, Type

import pytest

from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient


class BaseDependency:
    def __init__(self) -> None:
        self.counter = 0
        self.constructed, self.destructed = False, False


class SyncCallable(BaseDependency):

    def __call__(self) -> None:
        self.counter += 1
        self.constructed, self.destructed = True, True


class AsyncCallable(BaseDependency):
    
    async def __call__(self) -> None:
        self.counter += 1
        self.constructed, self.destructed = True, True


class SyncGenerator(BaseDependency):

    def __call__(self) -> None:
        self.counter += 1
        self.destructed = False
        self.constructed = True
        yield
        self.destructed = True


class AsyncGenerator(BaseDependency):

    async def __call__(self) -> None:
        self.counter += 1
        self.destructed = False
        self.constructed = True
        yield
        self.destructed = True


@pytest.mark.parametrize(
    "dep_cls", (SyncGenerator, AsyncGenerator)
)
def test_request_lifespan_context_manager(dep_cls: Callable[[], BaseDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep)])
    def root():
        assert dep.constructed
        assert not dep.destructed

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert dep.destructed
        assert client.get("/").status_code == 200
        assert dep.counter == 2
        assert dep.destructed


@pytest.mark.parametrize(
    "dep_cls", (SyncCallable, AsyncCallable)
)
def test_request_lifespan_callable(dep_cls: Callable[[], BaseDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep)])
    def root():
        ...

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert client.get("/").status_code == 200
        assert dep.counter == 2
