import json
from collections.abc import AsyncIterable, Iterable

import pytest
from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel


class UserIn(BaseModel):
    name: str
    password: str


class UserOut(BaseModel):
    name: str


class Item(BaseModel):
    name: str
    price: float


app = FastAPI()


@app.get("/users", response_model=UserOut)
async def users() -> AsyncIterable[UserIn]:
    yield UserIn(name="john", password="secret")


@app.get("/users-sync", response_model=UserOut)
def users_sync() -> Iterable[UserIn]:
    yield UserIn(name="jane", password="secret")


@app.get("/items-invalid", response_model=Item)
async def items_invalid() -> AsyncIterable[dict]:
    yield {"name": "valid", "price": 1.0}
    yield {"name": "invalid", "price": "not-a-number"}


@app.get("/items-options", response_model=UserOut, response_model_exclude_none=True)
async def items_options() -> AsyncIterable[dict]:
    yield {"name": "john", "password": "secret"}


client = TestClient(app)


def test_jsonl_explicit_response_model_filters_fields():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "john"}]


def test_jsonl_explicit_response_model_filters_fields_sync():
    response = client.get("/users-sync")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/jsonl"
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "jane"}]


def test_jsonl_explicit_response_model_validates_items():
    with pytest.raises(ResponseValidationError):
        client.get("/items-invalid")


def test_jsonl_explicit_response_model_honors_options():
    response = client.get("/items-options")
    assert response.status_code == 200
    lines = [json.loads(line) for line in response.text.strip().splitlines()]
    assert lines == [{"name": "john"}]


def test_openapi_uses_explicit_response_model_as_stream_schema():
    schema = client.get("/openapi.json").json()
    content = schema["paths"]["/users"]["get"]["responses"]["200"]["content"]
    stream_schema = content["application/jsonl"]["itemSchema"]
    assert stream_schema["$ref"].endswith("/UserOut")
    assert "password" not in schema["components"]["schemas"]["UserOut"]["properties"]
