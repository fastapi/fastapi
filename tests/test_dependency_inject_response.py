from typing import Union

import pytest
from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient


class SyncGenDep:
    response: Union[None, Response] = None

    def __call__(self):
        self.response = yield 1234
        return


class AsyncGenDep:
    response: Union[None, Response] = None

    async def __call__(self):
        self.response = yield 1234
        return


@pytest.mark.parametrize(
    "gen", (SyncGenDep(), AsyncGenDep()), ids=["sync-generator", "async-generator"]
)
def test_inject_response(gen: Union[SyncGenDep, AsyncGenDep]):
    app = FastAPI()

    @app.get("/raw")
    def raw(v: int = Depends(gen)):
        assert v == 1234
        return Response(status_code=400)

    @app.get("/json")
    def json(v: int = Depends(gen)):
        assert v == 1234
        return "abcd"

    client = TestClient(app)
    client.get("/raw")
    assert gen.response.status_code == 400
    client.get("/json")
    assert gen.response.body == b'"abcd"'


def sync_too_many_yields():
    yield
    yield


async def async_too_many_yields():
    yield
    yield


@pytest.mark.parametrize(
    "bad_dependency", (sync_too_many_yields, async_too_many_yields)
)
def test_dependency_with_too_many_yields(bad_dependency):
    """Dependencies with >=2 yields should raise a RuntimeError
    (raised by contextmanager/asynccontextmanager internally)
    """
    app = FastAPI()

    @app.get("/", dependencies=[Depends(bad_dependency)])
    def root():
        ...

    client = TestClient(app)

    with pytest.raises(RuntimeError, match="generator didn't stop"):
        client.get("/")


class ExpectedException(Exception):
    ...


class NestedException(Exception):
    ...


def sync_raises_exception_in_catch():
    try:
        yield
    except ExpectedException:
        raise NestedException


async def async_raises_exception_in_catch():
    try:
        yield
    except ExpectedException:
        raise NestedException


@pytest.mark.parametrize(
    "bad_dependency", (sync_raises_exception_in_catch, async_raises_exception_in_catch)
)
def test_dependency_raises_exception_in_catch(bad_dependency):
    app = FastAPI()

    @app.get("/", dependencies=[Depends(bad_dependency)])
    def root():
        raise ExpectedException

    client = TestClient(app)

    with pytest.raises(NestedException):
        client.get("/")


class TeardownException(Exception):
    ...


def sync_raises_exception_in_teardown():
    try:
        yield
    finally:
        raise TeardownException


async def async_raises_exception_in_teardown():
    try:
        yield
    finally:
        raise TeardownException


@pytest.mark.parametrize(
    "bad_dependency",
    (sync_raises_exception_in_teardown, async_raises_exception_in_teardown),
)
def test_dependency_raises_exception_in_teardown(bad_dependency):
    app = FastAPI()

    @app.get("/", dependencies=[Depends(bad_dependency)])
    def root():
        ...

    client = TestClient(app)

    with pytest.raises(TeardownException):
        client.get("/")
