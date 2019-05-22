from typing import List, Optional

import pytest
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError
from starlette.testclient import TestClient

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float = None
    owner_ids: List[int] = None
    store: Optional[str]


@app.get("/items/invalid", response_model=Item)
def get_invalid():
    return {"name": "invalid", "price": "foo"}


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


@app.get("/items/noskip", response_model=Item)
def get_noskip():
    item = Item(name="noskip")
    return item


@app.get("/items/skip", response_model=Item, skip_defaults=True)
def get_skip():
    item = Item(name="skip")
    return item


client = TestClient(app)


def test_invalid():
    with pytest.raises(ValidationError):
        client.get("/items/invalid")


def test_double_invalid():
    with pytest.raises(ValidationError):
        client.get("/items/innerinvalid")


def test_invalid_list():
    with pytest.raises(ValidationError):
        client.get("/items/invalidlist")


def test_confirm_pydantic_skip():
    """Confirming pydantic dict() skip_defaults"""

    item = Item(name="testme")

    assert item.dict() == {
        "name": "testme",
        "store": None,
        "price": None,
        "owner_ids": None,
    }
    assert item.dict(skip_defaults=True) == {"name": "testme"}


def test_noskip():
    r = client.get("/items/noskip")
    print("NoSkip", r.json())
    assert r.json() == {
        "name": "noskip",
        "store": None,
        "price": None,
        "owner_ids": None,
    }


def test_skip():
    r = client.get("/items/skip")
    print("Skip", r.json())

    assert r.json() == {"name": "skip"}
