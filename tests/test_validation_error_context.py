import pytest
from fastapi import FastAPI, Request, WebSocket
from fastapi.exceptions import (
    RequestValidationError,
    ResponseValidationError,
    WebSocketRequestValidationError,
)
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    id: int  # Required field


class ExceptionCapture:
    def __init__(self):
        self.exception = None

    def capture(self, exc):
        self.exception = exc
        return exc


# App with custom exception handlers that capture exceptions for testing
app = FastAPI()
captured_exception = ExceptionCapture()


@app.exception_handler(RequestValidationError)
async def request_validation_handler(request: Request, exc: RequestValidationError):
    captured_exception.capture(exc)
    raise exc


@app.exception_handler(WebSocketRequestValidationError)
async def websocket_validation_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
):
    captured_exception.capture(exc)
    raise exc


@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"user_id": user_id}


@app.get("/items/", response_model=Item)
def get_item():
    return {"name": "Widget"}


@app.websocket("/ws/{item_id}")
async def websocket_endpoint(websocket: WebSocket, item_id: int):
    await websocket.accept()
    await websocket.send_text(f"Item: {item_id}")
    await websocket.close()


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
    try:
        client.get("/items/")
    except ResponseValidationError as exc:
        error_str = str(exc)
        assert "get_item" in error_str
        assert "/items/" in error_str


def test_websocket_validation_error_includes_endpoint_context():
    try:
        with client.websocket_connect("/ws/invalid"):
            pass
    except Exception:
        pass

    assert captured_exception.exception is not None
    error_str = str(captured_exception.exception)
    assert "websocket_endpoint" in error_str
    assert "/ws/" in error_str
