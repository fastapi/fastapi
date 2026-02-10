from collections.abc import Generator
from contextlib import contextmanager
from typing import Annotated, Any

import pytest
from fastapi import Depends, FastAPI, WebSocket
from fastapi.testclient import TestClient


class Session:
    def __init__(self) -> None:
        self.data = ["foo", "bar", "baz"]
        self.open = True

    def __iter__(self) -> Generator[str, None, None]:
        for item in self.data:
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


def dep_session() -> Any:
    with acquire_session() as s:
        yield s


def broken_dep_session() -> Any:
    with acquire_session() as s:
        s.open = False
        yield s


SessionDep = Annotated[Session, Depends(dep_session)]
BrokenSessionDep = Annotated[Session, Depends(broken_dep_session)]

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: SessionDep):
    await websocket.accept()
    for item in session:
        await websocket.send_text(f"{item}")


@app.websocket("/ws-broken")
async def websocket_endpoint_broken(websocket: WebSocket, session: BrokenSessionDep):
    await websocket.accept()
    for item in session:
        await websocket.send_text(f"{item}")  # pragma no cover


client = TestClient(app)


def test_websocket_dependency_after_yield():
    with client.websocket_connect("/ws") as websocket:
        data = websocket.receive_text()
        assert data == "foo"
        data = websocket.receive_text()
        assert data == "bar"
        data = websocket.receive_text()
        assert data == "baz"


def test_websocket_dependency_after_yield_broken():
    with pytest.raises(ValueError, match="Session closed"):
        with client.websocket_connect("/ws-broken"):
            pass  # pragma no cover
