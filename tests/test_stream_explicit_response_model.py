import json
from collections.abc import AsyncIterable, Iterable

import pytest
from fastapi import FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    secret: str
    optional: str | None = None


app = FastAPI()


@app.get("/jsonl-sync", response_model=Item, response_model_exclude={"secret"})
def jsonl_sync():
    yield Item(name="foo", secret="hidden")


@app.get("/jsonl-async", response_model=Item, response_model_exclude={"secret"})
async def jsonl_async():
    yield Item(name="foo", secret="hidden")


@app.get("/jsonl-iterable", response_model=Iterable[Item])
def jsonl_iterable():
    yield Item(name="foo", secret="hidden")


@app.get("/jsonl-async-iterable", response_model=AsyncIterable[Item])
async def jsonl_async_iterable():
    yield Item(name="foo", secret="hidden")


@app.get("/jsonl-exclude-none", response_model=Item, response_model_exclude_none=True)
def jsonl_exclude_none():
    yield Item(name="foo", secret="hidden")


@app.get(
    "/sse",
    response_class=EventSourceResponse,
    response_model=Item,
    response_model_exclude={"secret"},
)
def sse():
    yield Item(name="foo", secret="hidden")


@app.get("/not-a-stream", response_model=Item, response_model_exclude={"secret"})
def not_a_stream():
    return Item(name="foo", secret="hidden")


@app.get("/invalid-item", response_model=Item)
def invalid_item():
    yield {"name": "foo"}


client = TestClient(app)


@pytest.mark.parametrize(
    "path",
    ["/jsonl-sync", "/jsonl-async", "/jsonl-iterable", "/jsonl-async-iterable"],
)
def test_explicit_response_model_streams_items(path):
    response = client.get(path)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    if "iterable" in path:
        assert lines == [{"name": "foo", "secret": "hidden", "optional": None}]
    else:
        # response_model_exclude applies to each streamed item
        assert lines == [{"name": "foo", "optional": None}]


def test_explicit_response_model_exclude_none():
    response = client.get("/jsonl-exclude-none")
    assert response.status_code == 200
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "foo", "secret": "hidden"}]


def test_explicit_response_model_sse():
    response = client.get("/sse")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/event-stream")
    assert '{"name":"foo","optional":null}' in response.text


def test_explicit_response_model_validates_each_item():
    with pytest.raises(Exception):  # noqa: B017 ResponseValidationError
        client.get("/invalid-item")


def test_non_streaming_endpoint_is_unchanged():
    response = client.get("/not-a-stream")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert response.json() == {"name": "foo", "optional": None}


@pytest.mark.parametrize(
    "path",
    [
        "/jsonl-sync",
        "/jsonl-async",
        "/jsonl-iterable",
        "/jsonl-async-iterable",
        "/jsonl-exclude-none",
    ],
)
def test_openapi_item_schema(path):
    content = app.openapi()["paths"][path]["get"]["responses"]["200"]["content"]
    assert content == {
        "application/jsonl": {"itemSchema": {"$ref": "#/components/schemas/Item"}}
    }


def test_openapi_non_streaming_schema_is_unchanged():
    content = app.openapi()["paths"]["/not-a-stream"]["get"]["responses"]["200"][
        "content"
    ]
    assert content == {
        "application/json": {"schema": {"$ref": "#/components/schemas/Item"}}
    }
