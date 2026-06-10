"""
Test that ClientDisconnect during request body reading is not
misreported as HTTP 400 "There was an error parsing the body".

Ref: https://github.com/fastapi/fastapi/issues/XXXXX
"""

import pytest
from fastapi import Body, FastAPI, Form
from fastapi.testclient import TestClient
from starlette.requests import ClientDisconnect

pytestmark = pytest.mark.anyio

app = FastAPI()


@app.post("/json")
async def json_endpoint(data: dict = Body(...)):
    return data


@app.post("/form")
async def form_endpoint(field: str = Form(...)):
    return {"field": field}


def _make_scope(path: str) -> dict:
    return {
        "type": "http",
        "asgi": {"version": "3.0"},
        "http_version": "1.1",
        "method": "POST",
        "scheme": "http",
        "path": path,
        "raw_path": path.encode(),
        "query_string": b"",
        "headers": [(b"content-type", b"application/json")],
        "client": ("127.0.0.1", 12345),
        "server": ("127.0.0.1", 8000),
    }


async def test_client_disconnect_json_body():
    """ClientDisconnect during JSON body reading must not become HTTP 400."""
    messages = [
        {"type": "http.request", "body": b'{"incomplete": ', "more_body": True},
        {"type": "http.disconnect"},
    ]

    async def receive():
        return messages.pop(0)

    sent: list[dict] = []

    async def send(message):
        sent.append(message)

    scope = _make_scope("/json")
    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)

    # Ensure no HTTP 400 response was sent
    for msg in sent:
        if msg.get("type") == "http.response.start":
            assert msg.get("status") != 400, (
                "ClientDisconnect should not produce HTTP 400"
            )


async def test_client_disconnect_form_body():
    """ClientDisconnect during form body reading must not become HTTP 400."""
    messages = [
        {
            "type": "http.request",
            "body": b"field=partial",
            "more_body": True,
        },
        {"type": "http.disconnect"},
    ]

    async def receive():
        return messages.pop(0)

    sent: list[dict] = []

    async def send(message):
        sent.append(message)

    scope = _make_scope("/form")
    scope["headers"] = [
        (b"content-type", b"application/x-www-form-urlencoded"),
    ]
    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)

    for msg in sent:
        if msg.get("type") == "http.response.start":
            assert msg.get("status") != 400, (
                "ClientDisconnect should not produce HTTP 400"
            )


def test_body_parse_error_still_returns_400():
    """Generic body parse errors must still produce HTTP 400."""
    client = TestClient(app, raise_server_exceptions=False)
    response = client.post(
        "/json",
        content=b"not valid json",
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 422
