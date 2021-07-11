from typing import Callable

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
        self.constructed = True
        yield
        self.destructed = True


class AsyncGenerator(BaseDependency):

    async def __call__(self) -> None:
        self.counter += 1
        self.constructed = True
        yield
        self.destructed = True


@pytest.mark.parametrize(
    "lifetime,expected_calls,n_requests", [
        ("app", 1, 1),
        ("app", 1, 5),
        ("request", 1, 1),
        ("request", 2, 2),
        ("request", 5, 5),
    ]
)
@pytest.mark.parametrize(
    "dependency_cls", [SyncCallable, AsyncCallable, SyncGenerator, AsyncGenerator]
)
def test_dependency_lifetimes(lifetime: str, expected_calls: int, n_requests: int, dependency_cls: Callable[[], BaseDependency]):
    """Lifetime dependencies should only be called/created once"""

    dependency = dependency_cls()

    app = FastAPI()

    @app.get("/")
    def root(placeholder: dependency = Depends(lifetime=lifetime)):
        ...

    with TestClient(app) as client:
        for req in range(n_requests):
            assert client.get("/").status_code == 200
            assert dependency.constructed
        assert dependency.counter == expected_calls
    assert dependency.destructed


def test_invalid_lifetime():
    """The only valid lifetimes are "app" and "request\""""
    with pytest.raises(AssertionError):
        Depends(lifetime="invalid")



def test_lifetime_dependency_reset_on_shutdown():
    """Lifetime dependencies should be reset when the app shuts down"""
    dependency = SyncCallable()

    app = FastAPI()

    @app.get("/")
    def root(placeholder: dependency = Depends(lifetime="app")):
        ...
    
    for lifecycle in range(2):
        with TestClient(app) as client:
            for req in range(3):
                assert client.get("/").status_code == 200
                assert dependency.constructed
                assert dependency.counter == lifecycle + 1
        assert dependency.destructed


def test_nested_dependencies():
    """Only the root of the dependency tree needs to be marked for app lifetime"""

    subdep_counter = 0

    def subdep():
        nonlocal subdep_counter
        subdep_counter += 1
        return subdep_counter

    def dep(v: int = Depends(subdep)):
        return v
    
    app = FastAPI()

    @app.get("/")
    def root(v: int = Depends(dep, lifetime="app")):
        assert v == 1

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/").status_code == 200
