from typing import List, Optional

import pytest
from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError

app = FastAPI()


class Item(BaseModel):
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None


@app.get("/items/invalid", response_model=Item)
def get_invalid():
    return {"name": "invalid", "price": "foo"}


@app.get("/items/invalidqs", response_model=Item)
def get_invalid_qs(a: int, b: float):
    return {"name": "invalid", "price": "foo", "a": a, "b": b}


@app.post("/items/invalidbody", response_model=Item)
def post_invalid_body(item: Item):
    return {"name": item.name, "price": "foo"}


@app.get("/items/innerinvalid", response_model=Item)
def get_innerinvalid():
    return {"name": "double invalid", "price": "foo", "owner_ids": ["foo", "bar"]}


@app.get("/items/invalidlist", response_model=List[Item])
def get_invalidlist():
    return [
        {"name": "foo"},
        {"name": "bar", "price": "bar"},
        {"name": "baz", "price": "baz"},
    ]


client = TestClient(app)


def test_invalid():
    with pytest.raises(ResponseValidationError) as excinfo:
        client.get("/items/invalid")

    exception = excinfo.value
    assert exception.request_body is None
    assert exception.response_body == get_invalid()


def test_invalid_qs():
    req_qs = {"a": 1, "b": 3.14}
    with pytest.raises(ResponseValidationError) as excinfo:
        client.get("/items/invalidqs", params=req_qs)

    exception = excinfo.value
    assert exception.request_body is None  # FIXME: capture query string params somehow?
    assert exception.response_body == get_invalid_qs(**req_qs)


def test_invalid_body():
    req_item = {"name": "test"}
    with pytest.raises(ResponseValidationError) as excinfo:
        client.post("/items/invalidbody", json=req_item)

    exception = excinfo.value
    assert exception.request_body == req_item
    assert exception.response_body == post_invalid_body(Item(**req_item))


def test_double_invalid():
    with pytest.raises(ResponseValidationError) as excinfo:
        client.get("/items/innerinvalid")

    exception = excinfo.value
    assert exception.request_body is None
    assert exception.response_body == get_innerinvalid()


def test_invalid_list():
    with pytest.raises(ResponseValidationError) as excinfo:
        client.get("/items/invalidlist")

    exception = excinfo.value
    assert exception.request_body is None
    assert exception.response_body == get_invalidlist()


def test_invalid_backward_compat():
    with pytest.raises(ValidationError):
        client.get("/items/invalid")


def test_invalid_qs_backward_compat():
    req_qs = {"a": 1, "b": 3.14}
    with pytest.raises(ValidationError):
        client.get("/items/invalidqs", params=req_qs)


def test_invalid_body_backward_compat():
    req_item = {"name": "test"}
    with pytest.raises(ValidationError):
        client.post("/items/invalidbody", json=req_item)


def test_double_invalid_backward_compat():
    with pytest.raises(ValidationError):
        client.get("/items/innerinvalid")


def test_invalid_list_backward_compat():
    with pytest.raises(ValidationError):
        client.get("/items/invalidlist")
