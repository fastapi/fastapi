from typing import List, Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic.dataclasses import dataclass

app = FastAPI()


@dataclass
class Item:
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None


@app.get("/items/valid", response_model=Item)
def get_valid():
    return {"name": "valid", "price": 1.0}


@app.get("/items/object", response_model=Item)
def get_object():
    return Item(name="object", price=1.0, owner_ids=[1, 2, 3])


@app.get("/items/coerce", response_model=Item)
def get_coerce():
    return {"name": "coerce", "price": "1.0"}


@app.get("/items/validlist", response_model=List[Item])
def get_validlist():
    return [
        {"name": "foo"},
        {"name": "bar", "price": 1.0},
        {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]


@app.get("/items/objectlist", response_model=List[Item])
def get_objectlist():
    return [
        Item(name="foo"),
        Item(name="bar", price=1.0),
        Item(name="baz", price=2.0, owner_ids=[1, 2, 3]),
    ]


@app.get("/items/no-response-model/object")
def get_no_response_model_object():
    return Item(name="object", price=1.0, owner_ids=[1, 2, 3])


@app.get("/items/no-response-model/objectlist")
def get_no_response_model_objectlist():
    return [
        Item(name="foo"),
        Item(name="bar", price=1.0),
        Item(name="baz", price=2.0, owner_ids=[1, 2, 3]),
    ]


client = TestClient(app)


def test_valid():
    response = client.get("/items/valid")
    response.raise_for_status()
    assert response.json() == {"name": "valid", "price": 1.0, "owner_ids": None}


def test_object():
    response = client.get("/items/object")
    response.raise_for_status()
    assert response.json() == {"name": "object", "price": 1.0, "owner_ids": [1, 2, 3]}


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


def test_objectlist():
    response = client.get("/items/objectlist")
    response.raise_for_status()
    assert response.json() == [
        {"name": "foo", "price": None, "owner_ids": None},
        {"name": "bar", "price": 1.0, "owner_ids": None},
        {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]


def test_no_response_model_object():
    response = client.get("/items/no-response-model/object")
    response.raise_for_status()
    assert response.json() == {"name": "object", "price": 1.0, "owner_ids": [1, 2, 3]}


def test_no_response_model_objectlist():
    response = client.get("/items/no-response-model/objectlist")
    response.raise_for_status()
    assert response.json() == [
        {"name": "foo", "price": None, "owner_ids": None},
        {"name": "bar", "price": 1.0, "owner_ids": None},
        {"name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]
