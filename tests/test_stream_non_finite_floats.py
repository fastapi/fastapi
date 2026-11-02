import json
from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict


class Item(BaseModel):
    value: float


@pytest.mark.parametrize("path", ["/jsonl", "/sse", "/sse-events"])
def test_untyped_stream_non_finite_floats(path: str):
    app = FastAPI()
    values = [float("nan"), float("inf"), float("-inf")]
    items = [
        *values,
        {"nested": [values, {"value": values[0]}]},
        *(Item(value=value) for value in values),
        {
            "finite": 1.5,
            "integer": 1,
            "boolean": True,
            "null": None,
            "text": "NaN Infinity -Infinity",
            "keys": {None: "null key", float("inf"): "infinite key"},
        },
    ]

    @app.get("/jsonl")
    @app.get("/sse", response_class=EventSourceResponse)
    async def stream():
        for item in items:
            yield item

    @app.get("/sse-events", response_class=EventSourceResponse)
    async def stream_events():
        for item in items:
            yield ServerSentEvent(data=item)

    with TestClient(app) as client:
        response = client.get(path)
    assert response.status_code == 200
    lines = [line.removeprefix("data: ") for line in response.text.splitlines() if line]
    assert [json.loads(line) for line in lines] == [
        None,
        None,
        None,
        {"nested": [[None, None, None], {"value": None}]},
        {"value": None},
        {"value": None},
        {"value": None},
        {
            "finite": 1.5,
            "integer": 1,
            "boolean": True,
            "null": None,
            "text": "NaN Infinity -Infinity",
            "keys": {"null": "null key", "Infinity": "infinite key"},
        },
    ]


def test_stream_preserves_model_serialization_and_raw_data():
    app = FastAPI()

    class ConfiguredItem(BaseModel):
        model_config = ConfigDict(ser_json_inf_nan="strings")
        value: float

    @app.get("/jsonl")
    @app.get("/sse", response_class=EventSourceResponse)
    async def stream() -> AsyncIterator[ConfiguredItem]:
        yield ConfiguredItem(value=float("nan"))

    @app.get("/sse-events", response_class=EventSourceResponse)
    async def stream_events():
        yield ServerSentEvent(data=ConfiguredItem(value=float("nan")))
        yield ServerSentEvent(raw_data="NaN")

    with TestClient(app) as client:
        assert client.get("/jsonl").text == '{"value":"NaN"}\n'
        assert client.get("/sse").text == 'data: {"value":"NaN"}\n\n'
        assert client.get("/sse-events").text == (
            'data: {"value":"NaN"}\n\ndata: NaN\n\n'
        )
