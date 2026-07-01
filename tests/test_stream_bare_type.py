import json
from typing import AsyncIterable, Iterable  # noqa: UP035 to test coverage

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str


app = FastAPI()


@app.get("/items/stream-bare-async")
async def stream_bare_async() -> AsyncIterable:
    yield {"name": "foo"}


@app.get("/items/stream-bare-sync")
def stream_bare_sync() -> Iterable:
    yield {"name": "bar"}


router = APIRouter()


@router.get("/events-jsonl")
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
