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
    "lifespan,expected_calls,n_requests", [
        ("app", 1, 1),
        ("app", 1, 5),
        ("request", 1, 1),
        ("request", 2, 2),
        ("request", 5, 5),
    ]
)
@pytest.mark.parametrize(
    "dependency_cls", [SyncCallable, AsyncCallable]
)
def test_dependency_lifespans_callable(lifespan: str, expected_calls: int, n_requests: int, dependency_cls: Callable[[], BaseDependency]):
    """lifespan dependencies should only be called/created once"""

    dependency = dependency_cls()

    app = FastAPI()

    @app.get("/")
    def root(placeholder: dependency = Depends(lifespan=lifespan)):
        ...

    with TestClient(app) as client:
        for req in range(n_requests):
            assert client.get("/").status_code == 200
            assert dependency.constructed
            assert dependency.destructed
        assert dependency.counter == expected_calls
    assert dependency.destructed


@pytest.mark.parametrize(
    "lifespan,expected_calls,n_requests", [
        ("app", 1, 1),
        ("app", 1, 5),
        ("request", 1, 1),
        ("request", 2, 2),
        ("request", 5, 5),
    ]
)
@pytest.mark.parametrize(
    "dependency_cls", [SyncGenerator, AsyncGenerator]
)
def test_dependency_lifespans_generator(lifespan: str, expected_calls: int, n_requests: int, dependency_cls: Callable[[], BaseDependency]):
    """lifespan dependencies should only be called/created once"""

    dependency = dependency_cls()

    app = FastAPI()

    @app.get("/")
    def root(placeholder: dependency = Depends(lifespan=lifespan)):
        ...

    with TestClient(app) as client:
        for req in range(n_requests):
            assert client.get("/").status_code == 200
            assert dependency.constructed
            assert dependency.destructed == (lifespan == "request")
        assert dependency.counter == expected_calls
    assert dependency.destructed


def test_invalid_lifespan():
    """The only valid lifespans are "app" and "request\""""
    with pytest.raises(AssertionError):
        Depends(lifespan="invalid")



def test_lifespan_dependency_reset_on_shutdown():
    """lifespan dependencies should be reset when the app shuts down"""
    dependency = SyncCallable()

    app = FastAPI()

    @app.get("/")
    def root(placeholder: dependency = Depends(lifespan="app")):
        ...
    
    for lifecycle in range(2):
        with TestClient(app) as client:
            for req in range(3):
                assert client.get("/").status_code == 200
                assert dependency.constructed
                assert dependency.counter == lifecycle + 1
        assert dependency.destructed


def test_nested_dependencies():
    """Only the root of the dependency tree needs to be marked for app lifespan"""

    subdep_counter = 0

    def subdep():
        nonlocal subdep_counter
        subdep_counter += 1
        return subdep_counter

    def dep(v: int = Depends(subdep)):
        return v
    
    app = FastAPI()

    @app.get("/")
    def root(v: int = Depends(dep, lifespan="app")):
        assert v == 1

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/").status_code == 200


def test_overrides():
    """Dependency overrides set BEFORE startup should be honored"""

    def real() -> int:
        return 1

    def fake() -> int:
        return 2

    app = FastAPI()

    @app.get("/")
    def root(v: int = Depends(real, lifespan="app")) -> int:
        return v

    with TestClient(app) as client:
        res = client.get("/")
        assert res.status_code == 200
        assert res.json() == 1
    
    app.dependency_overrides[real] = fake
    with TestClient(app) as client:
        res = client.get("/")
        assert res.status_code == 200
        assert res.json() == 2  # from fake
