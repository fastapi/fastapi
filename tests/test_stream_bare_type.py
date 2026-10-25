import json
from collections import abc
from typing import Any, AsyncIterable, Iterable  # noqa: UP035 to test coverage

import pytest
from fastapi import APIRouter, FastAPI
from fastapi.datastructures import Default
from fastapi.responses import EventSourceResponse, JSONResponse
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    optional: str | None = None


app = FastAPI()


@app.get("/items/stream-bare-async")
async def stream_bare_async() -> AsyncIterable:
    yield {"name": "foo"}


@app.get("/items/stream-bare-sync")
def stream_bare_sync() -> Iterable:
    yield {"name": "bar"}


router = APIRouter()


@router.get("/events-jsonl", response_model_exclude_none=True)
async def stream_events_jsonl() -> AsyncIterable[Item]:
    yield Item(name="foo")


app.include_router(router, prefix="/api")

client = TestClient(app)


def test_stream_bare_async_iterable():
    response = client.get("/items/stream-bare-async")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "foo"}]


def test_stream_bare_sync_iterable():
    response = client.get("/items/stream-bare-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "bar"}]


def test_jsonl_router_typed_stream():
    response = client.get("/api/events-jsonl")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "foo"}]


def test_jsonl_router_typed_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    jsonl_response = paths["/api/events-jsonl"]["get"]["responses"]["200"]
    assert jsonl_response == {
        "description": "Successful Response",
        "content": {
            "application/jsonl": {"itemSchema": {"$ref": "#/components/schemas/Item"}}
        },
    }


@pytest.mark.parametrize(
    "annotation,is_async",
    [
        (abc.Iterable, False),
        (abc.Iterator, False),
        (abc.Generator, False),
        (abc.AsyncIterable, True),
        (abc.AsyncIterator, True),
        (abc.AsyncGenerator, True),
    ],
)
@pytest.mark.parametrize("response_class", [Default(JSONResponse), EventSourceResponse])
def test_stream_bare_collections_abc(annotation, is_async, response_class):
    app = FastAPI()

    def stream_sync():
        yield {"name": "foo"}

    async def stream_async():
        yield {"name": "foo"}

    endpoint = stream_async if is_async else stream_sync
    endpoint.__annotations__["return"] = annotation
    app.add_api_route("/stream", endpoint, response_class=response_class)
    route = app.routes[-1]
    assert isinstance(route, APIRoute)
    assert route.stream_item_type is Any

    with TestClient(app) as client:
        response = client.get("/stream")
        assert response.status_code == 200
        content = client.get("/openapi.json").json()["paths"]["/stream"]["get"][
            "responses"
        ]["200"]["content"]
    if response_class is EventSourceResponse:
        assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
        assert response.text.startswith("data: ")
        assert json.loads(response.text.removeprefix("data: ")) == {"name": "foo"}
        item_schema = content["text/event-stream"]["itemSchema"]["properties"]["data"][
            "contentSchema"
        ]
    else:
        assert response.headers["content-type"] == "application/jsonl"
        assert json.loads(response.text) == {"name": "foo"}
        item_schema = content["application/jsonl"]["itemSchema"]
    assert "type" not in item_schema
