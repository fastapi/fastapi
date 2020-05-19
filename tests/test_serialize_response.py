from decimal import Decimal
from typing import List

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float = None
    owner_ids: List[int] = None


@app.get("/items/no_response_model")
def get_no_response_model():
    return {"name": "valid", "price": Decimal("1.0")}


@app.get("/items/valid", response_model=Item)
def get_valid():
    return {"name": "valid", "price": 1.0}


@app.get("/items/item", response_model=Item)
def get_item():
    return Item(name="valid", price=1.0)


@app.get("/items/coerce", response_model=Item)
def get_coerce():
    return {"name": "coerce", "price": "1.0"}


@app.get("/items/validlist", response_model=List[Item])
def get_validlist():
    return [
        {"name": "foo"},
        {"name": "bar", "price": 1.0},
        {"name": "baz", "price": "2.0", "owner_ids": [1, "2", 3]},
    ]


@app.get("/items/itemlist", response_model=List[Item])
def get_itemlist():
    return [
        Item(name="foo"),
        Item(name="bar", price=1.0),
        Item(name="baz", price="2.0", owner_ids=[1, "2", 3]),
    ]


client = TestClient(app)


def test_no_response_model():
    response = client.get("/items/no_response_model")
    response.raise_for_status()
    assert response.json() == {"name": "valid", "price": 1.0}


def test_valid():
    response = client.get("/items/valid")
    response.raise_for_status()
    assert response.json() == {"name": "valid", "price": 1.0, "owner_ids": None}


def test_item():
    response = client.get("/items/item")
    response.raise_for_status()
    assert response.json() == {"name": "valid", "price": 1.0, "owner_ids": None}


def test_coerce():
    response = client.get("/items/coerce")
    response.raise_for_status()
    assert response.json() == {"name": "coerce", "price": 1.0, "owner_ids": None}


def test_validlist():
    response = client.get("/items/validlist")
    response.raise_for_status()
    assert response.json() == [
        {"name": "foo", "price": None, "owner_ids": None},
        {"name": "bar", "price": 1.0, "owner_ids": None},
        {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]


def test_itemlist():
    response = client.get("/items/itemlist")
    response.raise_for_status()
    assert response.json() == [
        {"name": "foo", "price": None, "owner_ids": None},
        {"name": "bar", "price": 1.0, "owner_ids": None},
        {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]
