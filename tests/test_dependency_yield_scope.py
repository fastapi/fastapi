import json
from typing import Annotated, Any

import pytest
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.exceptions import FastAPIError
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient


class Session:
    def __init__(self) -> None:
        self.open = True


def dep_session() -> Any:
    s = Session()
    yield s
    s.open = False


def raise_after_yield() -> Any:
    yield
    raise HTTPException(status_code=503, detail="Exception after yield")


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


NamedSessionsDep = Annotated[tuple[NamedSession, Session], Depends(get_named_session)]


def get_named_func_session(session: SessionFuncDep) -> Any:
    named_session = NamedSession(name="named")
    yield named_session, session
    named_session.open = False


def get_named_regular_func_session(session: SessionFuncDep) -> Any:
    named_session = NamedSession(name="named")
    return named_session, session


BrokenSessionsDep = Annotated[
    tuple[NamedSession, Session], Depends(get_named_func_session)
]
NamedSessionsFuncDep = Annotated[
    tuple[NamedSession, Session], Depends(get_named_func_session, scope="function")
]

RegularSessionsDep = Annotated[
    tuple[NamedSession, Session], Depends(get_named_regular_func_session)
]

app = FastAPI()
router = APIRouter()


@router.get("/")
def get_index():
    return {"status": "ok"}


@app.get("/function-scope")
def function_scope(session: SessionFuncDep) -> Any:
    def iter_data():
        yield json.dumps({"is_open": session.open})

    return StreamingResponse(iter_data())


@app.get("/request-scope")
def request_scope(session: SessionRequestDep) -> Any:
    def iter_data():
        yield json.dumps({"is_open": session.open})

    return StreamingResponse(iter_data())


@app.get("/two-scopes")
def get_stream_session(
    function_session: SessionFuncDep, request_session: SessionRequestDep
) -> Any:
    def iter_data():
        yield json.dumps(
            {"func_is_open": function_session.open, "req_is_open": request_session.open}
        )

    return StreamingResponse(iter_data())


@app.get("/sub")
def get_sub(sessions: NamedSessionsDep) -> Any:
    def iter_data():
        yield json.dumps(
            {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
        )

    return StreamingResponse(iter_data())


@app.get("/named-function-scope")
def get_named_function_scope(sessions: NamedSessionsFuncDep) -> Any:
    def iter_data():
        yield json.dumps(
            {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
        )

    return StreamingResponse(iter_data())


@app.get("/regular-function-scope")
def get_regular_function_scope(sessions: RegularSessionsDep) -> Any:
    def iter_data():
        yield json.dumps(
            {"named_session_open": sessions[0].open, "session_open": sessions[1].open}
        )

    return StreamingResponse(iter_data())


app.include_router(
    prefix="/router-scope-function",
    router=router,
    dependencies=[Depends(raise_after_yield, scope="function")],
)

app.include_router(
    prefix="/router-scope-request",
    router=router,
    dependencies=[Depends(raise_after_yield, scope="request")],
)

client = TestClient(app)


def test_function_scope() -> None:
    response = client.get("/function-scope")
    assert response.status_code == 200
    data = response.json()
    assert data["is_open"] is False


def test_request_scope() -> None:
    response = client.get("/request-scope")
    assert response.status_code == 200
    data = response.json()
    assert data["is_open"] is True


def test_two_scopes() -> None:
    response = client.get("/two-scopes")
    assert response.status_code == 200
    data = response.json()
    assert data["func_is_open"] is False
    assert data["req_is_open"] is True


def test_sub() -> None:
    response = client.get("/sub")
    assert response.status_code == 200
    data = response.json()
    assert data["named_session_open"] is True
    assert data["session_open"] is True


def test_broken_scope() -> None:
    with pytest.raises(
        FastAPIError,
        match='The dependency "get_named_func_session" has a scope of "request", it cannot depend on dependencies with scope "function"',
    ):

        @app.get("/broken-scope")
        def get_broken(sessions: BrokenSessionsDep) -> Any:  # pragma: no cover
            pass


def test_named_function_scope() -> None:
    response = client.get("/named-function-scope")
    assert response.status_code == 200
    data = response.json()
    assert data["named_session_open"] is False
    assert data["session_open"] is False


def test_regular_function_scope() -> None:
    response = client.get("/regular-function-scope")
    assert response.status_code == 200
    data = response.json()
    assert data["named_session_open"] is True
    assert data["session_open"] is False


def test_router_level_dep_scope_function() -> None:
    response = client.get("/router-scope-function/")
    assert response.status_code == 503
    assert response.json() == {"detail": "Exception after yield"}


def test_router_level_dep_scope_request() -> None:
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/router-scope-request/")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_app_level_dep_scope_function() -> None:
    app = FastAPI(dependencies=[Depends(raise_after_yield, scope="function")])

    @app.get("/app-scope-function")
    def get_app_scope_function():
        return {"status": "ok"}

    with TestClient(app) as client:
        response = client.get("/app-scope-function")
        assert response.status_code == 503
        assert response.json() == {"detail": "Exception after yield"}


def test_app_level_dep_scope_request() -> None:
    app = FastAPI(dependencies=[Depends(raise_after_yield, scope="request")])

    @app.get("/app-scope-request")
    def get_app_scope_request():
        return {"status": "ok"}

    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/app-scope-request")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
