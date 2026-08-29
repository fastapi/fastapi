import pytest
from fastapi import Body, FastAPI, File, Form, Request, UploadFile
from pydantic import BaseModel
from starlette.requests import ClientDisconnect


class Item(BaseModel):
    name: str
    price: float


@pytest.mark.anyio
async def test_client_disconnect_json_body():
    app = FastAPI()

    @app.post("/items")
    async def create_item(item: Item):
        return item

    async def receive():
        return {"type": "http.disconnect"}

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/items",
        "raw_path": b"/items",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)


@pytest.mark.anyio
async def test_client_disconnect_raw_body():
    app = FastAPI()

    @app.post("/raw")
    async def create_raw(body: bytes = Body()):
        return {"length": len(body)}

    async def receive():
        return {"type": "http.disconnect"}

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/raw",
        "raw_path": b"/raw",
        "query_string": b"",
        "headers": [
            (b"content-type", b"text/plain"),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)


@pytest.mark.anyio
async def test_client_disconnect_form_body():
    app = FastAPI()

    @app.post("/form")
    async def create_form(username: str = Form()):
        return {"username": username}

    async def receive():
        return {"type": "http.disconnect"}

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/form",
        "raw_path": b"/form",
        "query_string": b"",
        "headers": [
            (
                b"content-type",
                b"application/x-www-form-urlencoded",
            ),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)


@pytest.mark.anyio
async def test_client_disconnect_file_upload():
    app = FastAPI()

    @app.post("/upload")
    async def upload_file(file: UploadFile = File()):
        return {"filename": file.filename}

    async def receive():
        return {"type": "http.disconnect"}

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/upload",
        "raw_path": b"/upload",
        "query_string": b"",
        "headers": [
            (
                b"content-type",
                b"multipart/form-data; boundary=----WebKitFormBoundarytest",
            ),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)


@pytest.mark.anyio
async def test_client_disconnect_request_direct():
    app = FastAPI()

    @app.post("/direct")
    async def direct(request: Request):
        await request.body()
        return {"status": "ok"}

    async def receive():
        return {"type": "http.disconnect"}

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/direct",
        "raw_path": b"/direct",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    with pytest.raises(ClientDisconnect):
        await app(scope, receive, send)


@pytest.mark.anyio
async def test_body_parsing_generic_error_returns_400():
    app = FastAPI()

    @app.post("/items")
    async def create_item(item: Item):
        return item

    async def receive():
        raise RuntimeError("Custom stream error")

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/items",
        "raw_path": b"/items",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    await app(scope, receive, send)
    assert events[0]["type"] == "http.response.start"
    assert events[0]["status"] == 400
    assert events[1]["type"] == "http.response.body"
    assert b"There was an error parsing the body" in events[1]["body"]


@pytest.mark.anyio
async def test_body_parsing_http_exception_reraised():
    from fastapi import HTTPException

    app = FastAPI()

    @app.post("/items")
    async def create_item(item: Item):
        return item

    async def receive():
        raise HTTPException(status_code=418, detail="Custom HTTP Error")

    scope = {
        "type": "http",
        "http_version": "1.1",
        "method": "POST",
        "path": "/items",
        "raw_path": b"/items",
        "query_string": b"",
        "headers": [
            (b"content-type", b"application/json"),
            (b"content-length", b"100"),
        ],
    }

    events = []

    async def send(event):
        events.append(event)

    await app(scope, receive, send)
    assert events[0]["type"] == "http.response.start"
    assert events[0]["status"] == 418
    assert events[1]["type"] == "http.response.body"
    assert b"Custom HTTP Error" in events[1]["body"]
