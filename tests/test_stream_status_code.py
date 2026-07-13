import json
from collections.abc import AsyncIterable
from typing import Any, cast

from fastapi import Depends, FastAPI, Response
from fastapi.responses import EventSourceResponse, StreamingResponse
from fastapi.testclient import TestClient

app = FastAPI()


def set_accepted(response: Response) -> None:
    response.status_code = 202


@app.post("/sse-created", response_class=EventSourceResponse, status_code=201)
async def sse_created() -> AsyncIterable[dict[str, str]]:
    yield {"message": "created"}


@app.post("/jsonl-created", status_code=201)
async def jsonl_created() -> AsyncIterable[dict[str, str]]:
    yield {"message": "created"}


@app.get("/sse-dependency", response_class=EventSourceResponse)
async def sse_dependency(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "accepted"}


@app.get("/jsonl-dependency")
async def jsonl_dependency(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "accepted"}


@app.get("/raw-dependency", response_class=StreamingResponse)
async def raw_dependency(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[str]:
    yield "accepted"


@app.post("/sse-created-override", response_class=EventSourceResponse, status_code=201)
async def sse_created_override(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "overridden"}


@app.post("/jsonl-created-override", status_code=201)
async def jsonl_created_override(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[dict[str, str]]:
    yield {"message": "overridden"}


@app.post("/raw-created-override", response_class=StreamingResponse, status_code=201)
async def raw_created_override(
    accepted: None = Depends(set_accepted),
) -> AsyncIterable[str]:
    yield "overridden"


client = TestClient(app)


def get_sse_data(response_text: str) -> list[dict[str, str]]:
    data_lines = [
        line.removeprefix("data: ")
        for line in response_text.splitlines()
        if line.startswith("data: ")
    ]
    return [json.loads(line) for line in data_lines]


def get_jsonl_data(response_text: str) -> list[dict[str, str]]:
    return [json.loads(line) for line in response_text.splitlines()]


def test_sse_stream_honors_declared_status_code() -> None:
    response = client.post("/sse-created")

    assert response.status_code == 201
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    assert get_sse_data(response.text) == [{"message": "created"}]


def test_jsonl_stream_honors_declared_status_code() -> None:
    response = client.post("/jsonl-created")

    assert response.status_code == 201
    assert response.headers["content-type"] == "application/jsonl"
    assert get_jsonl_data(response.text) == [{"message": "created"}]


def test_sse_stream_honors_dependency_status_code() -> None:
    response = client.get("/sse-dependency")

    assert response.status_code == 202
    assert get_sse_data(response.text) == [{"message": "accepted"}]


def test_jsonl_stream_honors_dependency_status_code() -> None:
    response = client.get("/jsonl-dependency")

    assert response.status_code == 202
    assert get_jsonl_data(response.text) == [{"message": "accepted"}]


def test_raw_stream_still_honors_dependency_status_code() -> None:
    response = client.get("/raw-dependency")

    assert response.status_code == 202
    assert response.text == "accepted"


def test_sse_stream_dependency_overrides_declared_status_code() -> None:
    response = client.post("/sse-created-override")

    assert response.status_code == 202
    assert get_sse_data(response.text) == [{"message": "overridden"}]


def test_jsonl_stream_dependency_overrides_declared_status_code() -> None:
    response = client.post("/jsonl-created-override")

    assert response.status_code == 202
    assert get_jsonl_data(response.text) == [{"message": "overridden"}]


def test_raw_stream_dependency_overrides_declared_status_code() -> None:
    response = client.post("/raw-created-override")

    assert response.status_code == 202
    assert response.text == "overridden"


def test_stream_status_codes_match_openapi() -> None:
    schema = client.get("/openapi.json").json()

    assert response_status_codes(schema, "/sse-created", "post") == ["201"]
    assert response_status_codes(schema, "/jsonl-created", "post") == ["201"]

    assert response_status_codes(schema, "/sse-created-override", "post") == ["201"]
    assert response_status_codes(schema, "/jsonl-created-override", "post") == ["201"]
    assert response_status_codes(schema, "/raw-created-override", "post") == ["201"]


def response_status_codes(schema: dict[str, Any], path: str, method: str) -> list[str]:
    paths = cast(dict[str, Any], schema["paths"])
    route = cast(dict[str, Any], paths[path])
    operation = cast(dict[str, Any], route[method])
    responses = cast(dict[str, Any], operation["responses"])
    return sorted(responses)
