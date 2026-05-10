from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager, contextmanager
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str


class Session:
    def __init__(self) -> None:
        self.items = [Item(name="foo"), Item(name="bar"), Item(name="baz")]
        self.open = True

    def __iter__(self) -> Generator[Item, None, None]:
        for item in self.items:
            if self.open:
                yield item
            else:
                raise ValueError("Session closed")

    def __aiter__(self) -> AsyncGenerator[Item, None]:
        return self._async_iter()

    async def _async_iter(self) -> AsyncGenerator[Item, None]:
        for item in self.items:
            if self.open:
                yield item
            else:
                raise ValueError("Session closed")


@contextmanager
def acquire_session() -> Generator[Session, None, None]:
    session = Session()
    try:
        yield session
    finally:
        session.open = False


@asynccontextmanager
async def acquire_async_session() -> AsyncGenerator[Session, None]:
    session = Session()
    try:
        yield session
    finally:
        session.open = False


def dep_session() -> Any:
    with acquire_session() as s:
        yield s


async def async_dep_session() -> Any:
    async with acquire_async_session() as s:
        yield s


def broken_dep_session() -> Any:
    with acquire_session() as s:
        s.open = False
        yield s


async def async_broken_dep_session() -> Any:
    async with acquire_async_session() as s:
        s.open = False
        yield s


SessionDep = Annotated[Session, Depends(dep_session)]
AsyncSessionDep = Annotated[Session, Depends(async_dep_session)]
BrokenSessionDep = Annotated[Session, Depends(broken_dep_session)]
AsyncBrokenSessionDep = Annotated[Session, Depends(async_broken_dep_session)]

app = FastAPI()


@app.get("/sse-sync", response_class=EventSourceResponse)
def sse_sync(session: SessionDep) -> Any:
    def gen() -> Generator[Item, None, None]:
        yield from session

    return gen()


@app.get("/sse-async", response_class=EventSourceResponse)
async def sse_async(session: AsyncSessionDep) -> AsyncGenerator[Item, None]:
    async for item in session:
        yield item


@app.get("/sse-broken-sync", response_class=EventSourceResponse)
def sse_broken_sync(session: BrokenSessionDep) -> Any:
    def gen() -> Generator[Item, None, None]:
        yield from session

    return gen()


@app.get("/sse-broken-async", response_class=EventSourceResponse)
async def sse_broken_async(
    session: AsyncBrokenSessionDep,
) -> AsyncGenerator[Item, None]:
    async for item in session:
        yield item


client = TestClient(app)


def _parse_sse_data_lines(text: str) -> list[str]:
    return [
        line[len("data: ") :]
        for line in text.strip().splitlines()
        if line.startswith("data: ")
    ]


def test_sse_sync_streams_items():
    response = client.get("/sse-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    data_lines = _parse_sse_data_lines(response.text)
    assert len(data_lines) == 3


def test_sse_sync_dependency_cleaned_up():
    """Yield dependency cleanup runs after the SSE stream completes."""
    sessions: list[Session] = []

    def tracking_dep() -> Any:
        with acquire_session() as s:
            sessions.append(s)
            yield s

    app.dependency_overrides[dep_session] = tracking_dep
    try:
        response = client.get("/sse-sync")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()

    assert len(sessions) == 1
    # The session's open flag must be False after stream ends -
    # meaning the finally block in acquire_session() ran.
    assert sessions[0].open is False


def test_sse_async_streams_items():
    response = client.get("/sse-async")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    data_lines = _parse_sse_data_lines(response.text)
    assert len(data_lines) == 3


def test_sse_async_dependency_cleaned_up():
    """Async yield dependency cleanup runs after the SSE stream completes."""
    sessions: list[Session] = []

    async def tracking_dep() -> Any:
        async with acquire_async_session() as s:
            sessions.append(s)
            yield s

    app.dependency_overrides[async_dep_session] = tracking_dep
    try:
        response = client.get("/sse-async")
        assert response.status_code == 200
    finally:
        app.dependency_overrides.clear()

    assert len(sessions) == 1
    assert sessions[0].open is False


def test_sse_broken_sync_raises():
    """When a sync yield dependency is broken the stream fails."""
    with pytest.raises((ValueError, Exception)):
        client.get("/sse-broken-sync")


def test_sse_broken_sync_no_raise():
    """
    When a sync yield dependency raises after streaming has started,
    the 200 status code is already sent but the body is empty.
    """
    with TestClient(app, raise_server_exceptions=False) as c:
        response = c.get("/sse-broken-sync")
    assert response.status_code == 200
    assert _parse_sse_data_lines(response.text) == []


def test_sse_broken_async_raises():
    """When an async yield dependency is broken the stream fails."""
    with pytest.raises((ValueError, Exception)):
        client.get("/sse-broken-async")


def test_sse_broken_async_no_raise():
    """
    When an async yield dependency raises after streaming has started,
    the 200 status code is already sent but the body is empty.
    """
    with TestClient(app, raise_server_exceptions=False) as c:
        response = c.get("/sse-broken-async")
    assert response.status_code == 200
    assert _parse_sse_data_lines(response.text) == []
