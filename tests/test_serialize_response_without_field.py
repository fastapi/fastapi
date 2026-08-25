import pytest
from fastapi import FastAPI
from fastapi.routing import serialize_response
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(alias="item_name")
    price: float = 10.0
    description: str | None = None
    secret: str = "top_secret"


@pytest.mark.anyio
async def test_serialize_response_direct_exclude_none():
    item = Item(item_name="foo", price=10.0, description=None)
    result = await serialize_response(response_content=item, exclude_none=True)
    assert result == {"item_name": "foo", "price": 10.0, "secret": "top_secret"}

    dict_item = {"name": "foo", "description": None}
    dict_result = await serialize_response(
        response_content=dict_item, exclude_none=True
    )
    assert dict_result == {"name": "foo"}


@pytest.mark.anyio
async def test_serialize_response_direct_exclude_defaults():
    item = Item(item_name="foo")
    result = await serialize_response(response_content=item, exclude_defaults=True)
    assert result == {"item_name": "foo"}


@pytest.mark.anyio
async def test_serialize_response_direct_exclude_unset():
    item = Item(item_name="foo")
    result = await serialize_response(response_content=item, exclude_unset=True)
    assert result == {"item_name": "foo"}


@pytest.mark.anyio
async def test_serialize_response_direct_exclude():
    item = Item(item_name="foo")
    result = await serialize_response(response_content=item, exclude={"secret"})
    assert result == {"item_name": "foo", "price": 10.0, "description": None}


@pytest.mark.anyio
async def test_serialize_response_direct_include():
    item = Item(item_name="foo")
    result = await serialize_response(response_content=item, include={"name"})
    assert result == {"item_name": "foo"}


@pytest.mark.anyio
async def test_serialize_response_direct_by_alias():
    item = Item(item_name="foo")
    result = await serialize_response(response_content=item, by_alias=False)
    assert result == {
        "name": "foo",
        "price": 10.0,
        "description": None,
        "secret": "top_secret",
    }


def test_endpoint_without_response_model_exclude_none():
    app = FastAPI()

    @app.get("/items/exclude-none", response_model_exclude_none=True)
    def read_items():
        return Item(item_name="foo", description=None)

    client = TestClient(app)
    response = client.get("/items/exclude-none")
    assert response.status_code == 200
    assert response.json() == {
        "item_name": "foo",
        "price": 10.0,
        "secret": "top_secret",
    }


def test_endpoint_without_response_model_exclude():
    app = FastAPI()

    @app.get("/items/exclude", response_model_exclude={"secret"})
    def read_items():
        return {"name": "foo", "secret": "hidden"}

    client = TestClient(app)
    response = client.get("/items/exclude")
    assert response.status_code == 200
    assert response.json() == {"name": "foo"}


def test_endpoint_without_response_model_include():
    app = FastAPI()

    @app.get("/items/include", response_model_include={"name"})
    def read_items():
        return Item(item_name="foo", price=10.0)

    client = TestClient(app)
    response = client.get("/items/include")
    assert response.status_code == 200
    assert response.json() == {"item_name": "foo"}


def test_endpoint_without_response_model_exclude_unset():
    app = FastAPI()

    @app.get("/items/exclude-unset", response_model_exclude_unset=True)
    def read_items():
        return Item(item_name="foo")

    client = TestClient(app)
    response = client.get("/items/exclude-unset")
    assert response.status_code == 200
    assert response.json() == {"item_name": "foo"}


def test_endpoint_without_response_model_exclude_defaults():
    app = FastAPI()

    @app.get("/items/exclude-defaults", response_model_exclude_defaults=True)
    def read_items():
        return Item(item_name="foo")

    client = TestClient(app)
    response = client.get("/items/exclude-defaults")
    assert response.status_code == 200
    assert response.json() == {"item_name": "foo"}


def test_endpoint_without_response_model_by_alias():
    app = FastAPI()

    @app.get("/items/by-alias", response_model_by_alias=False)
    def read_items():
        return Item(item_name="foo")

    client = TestClient(app)
    response = client.get("/items/by-alias")
    assert response.status_code == 200
    assert response.json() == {
        "name": "foo",
        "price": 10.0,
        "description": None,
        "secret": "top_secret",
    }


def test_jsonl_streaming_untyped_exclude_none():
    app = FastAPI()

    @app.get("/stream/jsonl", response_model_exclude_none=True)
    def stream_jsonl():
        yield {"name": "foo", "description": None}
        yield {"name": "bar", "description": None}

    client = TestClient(app)
    response = client.get("/stream/jsonl")
    assert response.status_code == 200
    assert response.text == '{"name": "foo"}\n{"name": "bar"}\n'


def test_sse_streaming_untyped_exclude():
    app = FastAPI()

    @app.get(
        "/stream/sse",
        response_class=EventSourceResponse,
        response_model_exclude={"secret"},
    )
    def stream_sse():
        yield {"name": "foo", "secret": "hidden"}

    client = TestClient(app)
    response = client.get("/stream/sse")
    assert response.status_code == 200
    assert "data: " in response.text
    assert "secret" not in response.text
    assert '"name": "foo"' in response.text


def test_sse_streaming_serversentevent_dict_exclude():
    app = FastAPI()

    @app.get(
        "/stream/sse-event",
        response_class=EventSourceResponse,
        response_model_exclude={"secret"},
    )
    def stream_sse_event():
        yield ServerSentEvent(data={"name": "foo", "secret": "hidden"})

    client = TestClient(app)
    response = client.get("/stream/sse-event")
    assert response.status_code == 200
    assert "data: " in response.text
    assert "secret" not in response.text
    assert '"name": "foo"' in response.text
