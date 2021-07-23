import asyncio
from time import sleep
from threading import Event
from typing import AsyncGenerator, Callable, Generator, List

import pytest

from fastapi import Depends, FastAPI, HTTPException
from fastapi.dependencies.lifetime import DependencyLifetime
from fastapi.testclient import TestClient


DESTROY_TIME = 0.1  # simulate work


class CallableDependency:
    def __init__(self) -> None:
        self.counter = 0


class SyncCallableDep(CallableDependency):
    def __call__(self) -> "SyncCallableDep":
        self.counter += 1
        return self


class AsyncCallableDep(CallableDependency):
    async def __call__(self) -> "AsyncCallableDep":
        self.counter += 1
        return self


class LifespanEvents:

    def __init__(self) -> None:
        self.destroying = Event()
        self.destroyed = Event()


class GeneratorDependency:
    def __init__(self):
        self.counter = 0
        self.lifespan_events: List[LifespanEvents] = []


class SyncGeneratorDep(GeneratorDependency):

    def __call__(self) -> Generator["SyncGeneratorDep", None, None]:
        self.counter += 1
        events = LifespanEvents()
        self.lifespan_events.append(events)
        yield self
        events.destroying.set()
        sleep(DESTROY_TIME)  # simulate work
        events.destroyed.set()


class AsyncGeneratorDep(GeneratorDependency):

    async def __call__(self) -> AsyncGenerator["AsyncGeneratorDep", None]:
        self.counter += 1
        events = LifespanEvents()
        self.lifespan_events.append(events)
        yield self
        events.destroying.set()
        await asyncio.sleep(DESTROY_TIME)  # simulate work
        events.destroyed.set()


@pytest.mark.parametrize(
    "dep_cls", (SyncGeneratorDep, AsyncGeneratorDep)
)
def test_request_lifetime_context_manager(dep_cls: Callable[[], GeneratorDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep, lifetime=DependencyLifetime.request)])
    def root():
        assert not dep.lifespan_events[-1].destroying.is_set()

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert dep.lifespan_events[0].destroying.is_set()
        assert dep.lifespan_events[0].destroyed.wait(DESTROY_TIME)
        assert client.get("/").status_code == 200
        assert dep.counter == 2
        assert dep.lifespan_events[1].destroyed.wait(DESTROY_TIME)


@pytest.mark.parametrize(
    "dep_cls", (SyncCallableDep, AsyncCallableDep)
)
def test_request_lifetime_callable(dep_cls: Callable[[], CallableDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep, lifetime=DependencyLifetime.request)])
    def root():
        ...

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert client.get("/").status_code == 200
        assert dep.counter == 2


@pytest.mark.parametrize(
    "dep_cls", (SyncGeneratorDep, AsyncGeneratorDep)
)
def test_app_lifetime_context_manager(dep_cls: Callable[[], GeneratorDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep, lifetime=DependencyLifetime.app)])
    def root():
        assert not dep.lifespan_events[-1].destroying.is_set()

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert not dep.lifespan_events[0].destroying.is_set()
        assert client.get("/").status_code == 200
        assert dep.counter == 2
        assert not dep.lifespan_events[1].destroying.is_set()
    assert all(e.destroyed.is_set() for e in dep.lifespan_events)


@pytest.mark.parametrize(
    "dep_cls", (SyncCallableDep, AsyncCallableDep)
)
def test_app_lifetime_callable(dep_cls: Callable[[], CallableDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep, lifetime=DependencyLifetime.app)])
    def root():
        ...

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert client.get("/").status_code == 200
        assert dep.counter == 2



@pytest.mark.parametrize(
    "dep_cls", (SyncGeneratorDep, AsyncGeneratorDep)
)
def test_endpoint_lifetime_context_manager(dep_cls: Callable[[], GeneratorDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep, lifetime=DependencyLifetime.endpoint)])
    def root():
        assert not dep.lifespan_events[-1].destroying.is_set()

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert dep.lifespan_events[0].destroyed.is_set()
        assert client.get("/").status_code == 200
        assert dep.counter == 2
        assert dep.lifespan_events[1].destroyed.is_set()


def test_endpoint_lifetime_context_manager_cleanup_raises_HTTPException():

    def error_gen():
        yield
        raise HTTPException(400)  # should set status code

    app = FastAPI()

    called = False

    @app.get("/", dependencies=[Depends(error_gen, lifetime=DependencyLifetime.endpoint)])
    def root():
        nonlocal called
        called = True

    with TestClient(app) as client:
        res = client.get("/")
        assert res.status_code == 400
        assert called


def test_endpoint_lifetime_context_manager_cleanup_raises_Exception():

    def error_gen():
        yield
        raise Exception()  # results in 500 status code

    app = FastAPI()

    called = False

    @app.get("/", dependencies=[Depends(error_gen, lifetime=DependencyLifetime.endpoint)])
    def root():
        nonlocal called
        called = True

    with TestClient(app, raise_server_exceptions=False) as client:
        assert client.get("/").status_code == 500
        assert called


@pytest.mark.parametrize(
    "dep_cls", (SyncCallableDep, AsyncCallableDep)
)
def test_endpoint_lifetime_callable(dep_cls: Callable[[], CallableDependency]):

    dep = dep_cls()

    app = FastAPI()

    @app.get("/", dependencies=[Depends(dep, lifetime=DependencyLifetime.endpoint)])
    def root():
        ...

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert dep.counter == 1
        assert client.get("/").status_code == 200
        assert dep.counter == 2
