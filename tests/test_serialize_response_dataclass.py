from typing import List, Optional, Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError
from pydantic.dataclasses import dataclass

app = FastAPI()


@dataclass
class Item:
    name: str
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None


@dataclass
class ItemDataclass:
    item: Item
    option: Optional[bool] = None


class ItemModel(BaseModel):
    item: Item
    item_list: list[Item]
    item_dict: dict[str, Item]
    item_dataclass: ItemDataclass


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


def _test_item_model() -> ItemModel:
    item = Item(name='foo', price=1.0, owner_ids=[1, 2, 3])
    return ItemModel(
        item=item,
        item_list=[item, item],
        item_dict={'foo': item, 'bar': item},
        item_dataclass=ItemDataclass(item=item)
    )


@app.get("/items/response-model-nested-dataclass/invalid", response_model=ItemModel)
def get_response_model_nested_enum_invalid():
    return _test_item_model()


@app.get(
    "/items/response-model-nested-dataclass/valid",
    response_model=ItemModel,
    reconcile_nested_dataclasses=True,
)
def get_response_model_nested_enum_valid():
    return _test_item_model()


def none_filtering_dict_factory(d: list[tuple[str, Any]]):
    return {k: v for k, v in d if v is not None}


@app.get(
    "/items/response-model-nested-dataclass/specify-dataclass-dict-factory",
    response_model=ItemModel,
    reconcile_nested_dataclasses=True,
    dataclass_dict_factory=none_filtering_dict_factory,
)
def get_response_model_nested_enum_specify_dataclass_dict_factory():
    return _test_item_model()


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


def test_response_model_nested_dataclass_invalid():
    with pytest.raises(ValidationError):
        client.get("/items/response-model-nested-dataclass/invalid")


def test_response_model_nested_dataclass_valid():
    response = client.get("/items/response-model-nested-dataclass/valid")
    assert response.json() == {
        'item': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
        'item_list': [
            {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
            {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0}
        ],
        'item_dict': {
            'bar': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
            'foo': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0}
        },
        'item_dataclass': {
            'item': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
            'option': None
        },
    }


def test_response_model_nested_dataclass_specify_dataclass_dict_factory():
    response = client.get("/items/response-model-nested-dataclass/specify-dataclass-dict-factory")
    assert response.json() == {
        'item': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
        'item_list': [
            {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
            {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0}
        ],
        'item_dict': {
            'bar': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0},
            'foo': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0}
        },
        'item_dataclass': {
            'item': {'name': 'foo', 'owner_ids': [1, 2, 3], 'price': 1.0}
        },
    }
