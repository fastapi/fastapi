from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
    WebSocketRequestValidationError,
)
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    id: int
    name: str


class ExceptionCapture:
    def __init__(self):
        self.exception = None

    def capture(self, exc):
        self.exception = exc
        return exc


app = FastAPI()
sub_app = FastAPI()
captured_exception = ExceptionCapture()

app.mount(path="/sub", app=sub_app)


@app.exception_handler(RequestValidationError)
@sub_app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    captured_exception.capture(exc)
    raise exc


@app.exception_handler(ResponseValidationError)
@sub_app.exception_handler(ResponseValidationError)
async def response_validation_handler(_: Request, exc: ResponseValidationError):
    captured_exception.capture(exc)
    raise exc


@app.exception_handler(WebSocketRequestValidationError)
@sub_app.exception_handler(WebSocketRequestValidationError)
async def websocket_validation_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
):
    captured_exception.capture(exc)
    raise exc


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}  # pragma: no cover


@app.get("/items/", response_model=Item)
def get_item():
    return {"name": "Widget"}


@sub_app.get("/items/", response_model=Item)
def get_sub_item():
    return {"name": "Widget"}  # pragma: no cover


@app.websocket("/ws/{item_id}")
async def websocket_endpoint(websocket: WebSocket, item_id: int):
    await websocket.accept()  # pragma: no cover
    await websocket.send_text(f"Item: {item_id}")  # pragma: no cover
    await websocket.close()  # pragma: no cover


@sub_app.websocket("/ws/{item_id}")
async def subapp_websocket_endpoint(websocket: WebSocket, item_id: int):
    await websocket.accept()  # pragma: no cover
    await websocket.send_text(f"Item: {item_id}")  # pragma: no cover
    await websocket.close()  # pragma: no cover


client = TestClient(app)


def test_request_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        client.get("/users/invalid")
    except Exception:
        pass

    assert captured_exception.exception is not None
    error_str = str(captured_exception.exception)
    assert "get_user" in error_str
    assert "/users/" in error_str


def test_response_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        client.get("/items/")
    except Exception:
        pass

    assert captured_exception.exception is not None
    error_str = str(captured_exception.exception)
    assert "get_item" in error_str
    assert "/items/" in error_str


def test_websocket_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        with client.websocket_connect("/ws/invalid"):
            pass  # pragma: no cover
    except Exception:
        pass

    assert captured_exception.exception is not None
    error_str = str(captured_exception.exception)
    assert "websocket_endpoint" in error_str
    assert "/ws/" in error_str


def test_subapp_request_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        client.get("/sub/items/")
    except Exception:
        pass

    assert captured_exception.exception is not None
    error_str = str(captured_exception.exception)
    assert "get_sub_item" in error_str
    assert "/sub/items/" in error_str


def test_subapp_websocket_validation_error_includes_endpoint_context():
    captured_exception.exception = None
    try:
        with client.websocket_connect("/sub/ws/invalid"):
            pass  # pragma: no cover
    except Exception:
        pass

    assert captured_exception.exception is not None
    error_str = str(captured_exception.exception)
    assert "subapp_websocket_endpoint" in error_str
    assert "/sub/ws/" in error_str


def test_validation_error_with_only_path():
    errors = [{"type": "missing", "loc": ("body", "name"), "msg": "Field required"}]
    exc = RequestValidationError(errors, endpoint_ctx={"path": "GET /api/test"})
    error_str = str(exc)
    assert "Endpoint: GET /api/test" in error_str
    assert 'File "' not in error_str


def test_validation_error_with_no_context():
    errors = [{"type": "missing", "loc": ("body", "name"), "msg": "Field required"}]
    exc = RequestValidationError(errors, endpoint_ctx={})
    error_str = str(exc)
    assert "1 validation error:" in error_str
    assert "Endpoint" not in error_str
    assert 'File "' not in error_str
