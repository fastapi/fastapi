import pytest
from fastapi import BackgroundTasks, FastAPI, Request, Response, WebSocket
from fastapi.security import SecurityScopes
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/request")
def request(r1: Request, r2: Request) -> str:
    assert r1 is not None
    assert r1 is r2
    return "success"


@app.get("/response")
def response(r1: Response, r2: Response) -> str:
    assert r1 is not None
    assert r1 is r2
    return "success"


@app.get("/background-tasks")
def background_tasks(t1: BackgroundTasks, t2: BackgroundTasks) -> str:
    assert t1 is not None
    assert t1 is t2
    return "success"


@app.get("/security-scopes")
def security_scopes(sc1: SecurityScopes, sc2: SecurityScopes) -> str:
    assert sc1 is not None
    assert sc1 is sc2
    return "success"


@app.websocket("/websocket")
async def websocket(ws1: WebSocket, ws2: WebSocket) -> str:
    assert ws1 is ws2
    await ws1.accept()
    await ws1.send_text("success")
    await ws1.close()


@pytest.mark.parametrize(
    "url",
    (
        "/request",
        "/response",
        "/background-tasks",
        "/security-scopes",
    ),
)
def test_duplicate_special_dependency(url: str) -> None:
    assert TestClient(app).get(url).text == '"success"'


def test_duplicate_websocket_dependency() -> None:
    with TestClient(app).websocket_connect("/websocket") as ws:
        text = ws.receive_text()
        assert text == "success"
