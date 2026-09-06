from collections.abc import AsyncIterator
from contextvars import ContextVar

from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.asgi import ASGIMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.datastructures import MutableHeaders

current_user = ContextVar[str]("current_user", default="anonymous")


class Item(BaseModel):
    name: str


class StateMiddleware(ASGIMiddleware):
    async def on_request(self, request: Request) -> None:
        request.state.tag = "from-middleware"

    async def on_response(
        self, request: Request, status_code: int, headers: MutableHeaders
    ) -> None:
        headers["X-Tag"] = request.state.tag
        headers["X-Status"] = str(status_code)
        headers["X-User"] = current_user.get()


class BlockMiddleware(ASGIMiddleware):
    async def on_request(self, request: Request) -> JSONResponse | None:
        if request.headers.get("x-block"):
            return JSONResponse({"detail": "Blocked"}, status_code=403)
        return None


class BodyReadingMiddleware(ASGIMiddleware):
    async def on_request(self, request: Request) -> None:
        request.state.body_size = len(await request.body())


class ServerHeaderMiddleware(ASGIMiddleware):
    async def on_response(
        self, request: Request, status_code: int, headers: MutableHeaders
    ) -> None:
        headers["X-Server"] = "FastAPI"


app = FastAPI()
app.add_middleware(ServerHeaderMiddleware)
app.add_middleware(BodyReadingMiddleware)
app.add_middleware(BlockMiddleware)
app.add_middleware(StateMiddleware)


@app.get("/tag")
async def get_tag(request: Request) -> dict[str, str]:
    current_user.set("deadpond")
    return {"tag": request.state.tag}


@app.post("/items")
async def create_item(item: Item, request: Request) -> dict[str, object]:
    return {"name": item.name, "body_size": request.state.body_size}


@app.get("/stream")
async def get_stream() -> StreamingResponse:
    async def numbers() -> AsyncIterator[str]:
        for number in range(3):
            yield str(number)

    return StreamingResponse(numbers(), media_type="text/plain")


@app.get("/error")
async def get_error() -> None:
    raise RuntimeError("Oops")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    await websocket.send_text("Hello")
    await websocket.close()


client = TestClient(app)


def test_state_shared_between_hooks_and_path_operation():
    response = client.get("/tag")
    assert response.status_code == 200, response.text
    assert response.json() == {"tag": "from-middleware"}
    assert response.headers["X-Tag"] == "from-middleware"
    assert response.headers["X-Status"] == "200"
    assert response.headers["X-Server"] == "FastAPI"


def test_contextvar_set_in_path_operation_is_visible():
    response = client.get("/tag")
    assert response.headers["X-User"] == "deadpond"


def test_on_request_can_return_a_response():
    response = client.get("/tag", headers={"x-block": "yes"})
    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Blocked"}
    assert response.headers["X-Tag"] == "from-middleware"


def test_body_read_in_on_request_still_reaches_the_path_operation():
    response = client.post("/items", json={"name": "Plumbus"})
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Plumbus", "body_size": 18}


def test_streaming_response_is_not_buffered():
    with (
        TestClient(app) as streaming_client,
        streaming_client.stream("GET", "/stream") as response,
    ):
        assert response.headers["X-Status"] == "200"
        assert response.read() == b"012"


def test_unhandled_exception_is_not_swallowed():
    silent_client = TestClient(app, raise_server_exceptions=False)
    response = silent_client.get("/error")
    assert response.status_code == 500, response.text
    assert "X-Tag" not in response.headers


def test_websocket_is_passed_through():
    with client.websocket_connect("/ws") as websocket:
        assert websocket.receive_text() == "Hello"
