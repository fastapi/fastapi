import json
from typing import Any

from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse
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


app = FastAPI()


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


client = TestClient(app)


def test_function_scope() -> None:
    response = client.get("/function-scope")
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["is_open"] is False


def test_request_scope() -> None:
    response = client.get("/request-scope")
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["is_open"] is True


def test_two_scopes() -> None:
    response = client.get("/two-scopes")
    assert response.status_code == 200
    data = json.loads(response.content)
    assert data["func_is_open"] is False
    assert data["req_is_open"] is True
