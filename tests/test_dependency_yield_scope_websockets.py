from typing import Any, Tuple

import pytest
from fastapi import Depends, FastAPI, WebSocket
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient
from typing_extensions import Annotated


class Session:
    def __init__(self) -> None:
        self.open = True


def dep_session() -> Any:
    s = Session()
    yield s
    s.open = False


SessionFuncDep = Annotated[Session, Depends(dep_session, scope="function")]
SessionRequestDep = Annotated[Session, Depends(dep_session, scope="request")]
SessionDefaultDep = Annotated[Session, Depends(dep_session)]


class NamedSession:
    def __init__(self, name: str = "default") -> None:
        self.name = name
        self.open = True


def get_named_session(session: SessionRequestDep, session_b: SessionDefaultDep) -> Any:
    assert session is session_b
    named_session = NamedSession(name="named")
    yield named_session, session_b
    named_session.open = False


NamedSessionsDep = Annotated[Tuple[NamedSession, Session], Depends(get_named_session)]


def get_named_func_session(session: SessionFuncDep) -> Any:
    named_session = NamedSession(name="named")
    yield named_session, session
    named_session.open = False


def get_named_regular_func_session(session: SessionFuncDep) -> Any:
    named_session = NamedSession(name="named")
    return named_session, session


BrokenSessionsDep = Annotated[
    Tuple[NamedSession, Session], Depends(get_named_func_session)
]
NamedSessionsFuncDep = Annotated[
    Tuple[NamedSession, Session], Depends(get_named_func_session, scope="function")
]

RegularSessionsDep = Annotated[
    Tuple[NamedSession, Session], Depends(get_named_regular_func_session)
]

app = FastAPI()


@app.websocket("/function-scope")
async def function_scope(websocket: WebSocket, session: SessionFuncDep) -> Any:
    await websocket.accept()
    await websocket.send_json({"is_open": session.open})


@app.websocket("/request-scope")
async def request_scope(websocket: WebSocket, session: SessionRequestDep) -> Any:
    await websocket.accept()
    await websocket.send_json({"is_open": session.open})


@app.websocket("/two-scopes")
async def get_stream_session(
    websocket: WebSocket,
    function_session: SessionFuncDep,
    request_session: SessionRequestDep,
) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"func_is_open": function_session.open, "req_is_open": request_session.open}
    )


@app.websocket("/sub")
async def get_sub(websocket: WebSocket, sessions: NamedSessionsDep) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
    )


@app.websocket("/named-function-scope")
async def get_named_function_scope(
    websocket: WebSocket, sessions: NamedSessionsFuncDep
) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
    )


@app.websocket("/regular-function-scope")
async def get_regular_function_scope(
    websocket: WebSocket, sessions: RegularSessionsDep
) -> Any:
    await websocket.accept()
    await websocket.send_json(
        {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
    )


client = TestClient(app)


def test_function_scope() -> None:
    with client.websocket_connect("/function-scope") as websocket:
        data = websocket.receive_json()
    assert data["is_open"] is True


def test_request_scope() -> None:
    with client.websocket_connect("/request-scope") as websocket:
        data = websocket.receive_json()
    assert data["is_open"] is True


def test_two_scopes() -> None:
    with client.websocket_connect("/two-scopes") as websocket:
        data = websocket.receive_json()
    assert data["func_is_open"] is True
    assert data["req_is_open"] is True


def test_sub() -> None:
    with client.websocket_connect("/sub") as websocket:
        data = websocket.receive_json()
    assert data["named_session_open"] is True
    assert data["session_open"] is True


def test_broken_scope() -> None:
    with pytest.raises(
        FastAPIError,
        match='The dependency "get_named_func_session" has a scope of "request", it cannot depend on dependencies with scope "function"',
    ):

        @app.websocket("/broken-scope")
        async def get_broken(
            websocket: WebSocket, sessions: BrokenSessionsDep
        ) -> Any:  # pragma: no cover
            pass


def test_named_function_scope() -> None:
    with client.websocket_connect("/named-function-scope") as websocket:
        data = websocket.receive_json()
    assert data["named_session_open"] is True
    assert data["session_open"] is True


def test_regular_function_scope() -> None:
    with client.websocket_connect("/regular-function-scope") as websocket:
        data = websocket.receive_json()
    assert data["named_session_open"] is True
    assert data["session_open"] is True
