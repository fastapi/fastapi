import json

import pytest
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, status
from fastapi.testclient import TestClient

app = FastAPI()


@app.websocket("/ws/{item_id}")
async def websocket_endpoint(websocket: WebSocket, item_id: int):
    await websocket.accept()  # pragma: no cover
    await websocket.send_text(f"Item: {item_id}")  # pragma: no cover
    await websocket.close()  # pragma: no cover


client = TestClient(app)


def test_websocket_request_validation_closes_with_json_reason():
    """
    The default WebSocket validation exception handler must close the
    connection with code 1008 and a string reason.

    `WebSocket.close()` only accepts `reason` of type `str | None`, so the
    validation errors have to be serialized (to a JSON string) instead of
    being passed as a list.
    """
    with pytest.raises(WebSocketDisconnect) as exc_info:
        with client.websocket_connect("/ws/not-an-int"):
            pass  # pragma: no cover
    assert exc_info.value.code == status.WS_1008_POLICY_VIOLATION
    reason = exc_info.value.reason
    assert isinstance(reason, str)
    errors = json.loads(reason)
    assert len(errors) == 1
    assert errors[0]["type"] == "int_parsing"
    assert errors[0]["loc"] == ["path", "item_id"]
    assert errors[0]["input"] == "not-an-int"
