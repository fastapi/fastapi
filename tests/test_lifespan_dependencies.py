from typing import Callable

import pytest
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import DependencyResolutionError
from fastapi.testclient import TestClient


class BaseDependency:
    def __init__(self) -> None:
        self.counter = 0
        self.constructed, self.destructed = False, False


class SyncCallable(BaseDependency):
    def __call__(self) -> "SyncCallable":
        self.counter += 1
        self.constructed, self.destructed = True, True
        return self


class AsyncCallable(BaseDependency):
    async def __call__(self) -> "AsyncCallable":
        self.counter += 1
        self.constructed, self.destructed = True, True
        return self


class SyncGenerator(BaseDependency):
    def __call__(self) -> "SyncGenerator":
        self.counter += 1
        self.constructed = True
        yield self
        self.destructed = True


class AsyncGenerator(BaseDependency):
    async def __call__(self) -> "AsyncGenerator":
        self.counter += 1
        self.constructed = True
        yield self
        self.destructed = True


@pytest.mark.parametrize(
    "dependency_cls, stateless",
    [
        (SyncCallable, True),
        (AsyncCallable, True),
        (SyncGenerator, False),
        (AsyncGenerator, False),
    ],
)
def test_startup_dependencies(
    dependency_cls: Callable[[], BaseDependency], stateless: bool
):

    dependency = dependency_cls()

    def startup(placeholder: None = Depends(dependency)):
        ...

    app = FastAPI(on_startup=[startup])

    with TestClient(app):
        assert dependency.constructed
        assert dependency.destructed == stateless
    assert dependency.destructed


@pytest.mark.parametrize(
    "dependency_cls, stateless",
    [
        (SyncCallable, True),
        (AsyncCallable, True),
        (SyncGenerator, False),
        (AsyncGenerator, False),
    ],
)
def test_shutdown_dependencies(
    dependency_cls: Callable[[], BaseDependency], stateless: bool
):

    dependency = dependency_cls()

    def shutdown(placeholder: dependency_cls = Depends(dependency)):
        ...

    app = FastAPI(on_shutdown=[shutdown])

    with TestClient(app):
        assert not dependency.constructed
    assert dependency.destructed


def test_dependency_reset_on_shutdown():
    """lifespan dependencies should be reset when the app shuts down"""
    dependency = SyncCallable()

    def startup(placeholder: SyncCallable = Depends(dependency)):
        ...

    app = FastAPI(on_startup=[startup])

    for lifecycle in range(2):
        with TestClient(app):
            assert dependency.constructed
            assert dependency.counter == lifecycle + 1
        assert dependency.destructed


@pytest.mark.parametrize("use_cache", (True, False))
def test_dependency_caching(use_cache: bool):
    """Startup/shutdown dependencies are cached, unless `use_cache=False` is passed"""

    def child_dep():
        return object()

    class ParentDep(BaseDependency):
        def __call__(self, child: object = Depends(child_dep)) -> "ParentDep":
            self.counter += 1
            self.child = child
            return self

    parent_dep = ParentDep()

    def startup(
        parent: ParentDep = Depends(parent_dep),
        child: object = Depends(child_dep, use_cache=use_cache),
    ):
        assert (parent.child is child) == use_cache

    app = FastAPI(on_startup=[startup])

    with TestClient(app):
        ...


def test_overrides():
    """Dependency overrides set BEFORE startup should be honored"""

    def real() -> int:
        return 1

    def fake() -> int:
        return 2

    class StartupRecorder:
        v = None

        def __call__(self, v: int = Depends(real)):
            self.v = v

    startup = StartupRecorder()

    app = FastAPI(on_startup=[startup])

    with TestClient(app):
        assert startup.v == 1  # from real

    app.dependency_overrides[real] = fake
    with TestClient(app):
        assert startup.v == 2  # from fake


def test_startup_requests_request():
    """Startup events cannot depend on Request, even indirectly"""

    def dep(placeholder: Request):
        ...

    def startup_direct(placeholder: Request):
        ...

    def startup_indirect(placeholder: None = Depends(dep)):
        ...

    for startup in (startup_direct, startup_indirect):
        app = FastAPI(on_startup=[startup])

        with pytest.raises(
            DependencyResolutionError, match="cannot depend on connection parameters"
        ):
            with TestClient(app):
                ...
