from typing import Optional

from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2
from pydantic import BaseModel, Field
from starlette.testclient import TestClient

app = FastAPI()


class Item(BaseModel):
    name: str = Field(alias="aliased_name")
    price: Optional[float] = None
    owner_ids: Optional[list[int]] = None


@app.get("/items/valid", response_model=Item)
def get_valid():
    return Item(aliased_name="valid", price=1.0)


@app.get("/items/coerce", response_model=Item)
def get_coerce():
    return Item(aliased_name="coerce", price="1.0")


@app.get("/items/validlist", response_model=list[Item])
def get_validlist():
    return [
        Item(aliased_name="foo"),
        Item(aliased_name="bar", price=1.0),
        Item(aliased_name="baz", price=2.0, owner_ids=[1, 2, 3]),
    ]


@app.get("/items/validdict", response_model=dict[str, Item])
def get_validdict():
    return {
        "k1": Item(aliased_name="foo"),
        "k2": Item(aliased_name="bar", price=1.0),
        "k3": Item(aliased_name="baz", price=2.0, owner_ids=[1, 2, 3]),
    }


@app.get(
    "/items/valid-exclude-unset", response_model=Item, response_model_exclude_unset=True
)
def get_valid_exclude_unset():
    return Item(aliased_name="valid", price=1.0)


@app.get(
    "/items/coerce-exclude-unset",
    response_model=Item,
    response_model_exclude_unset=True,
)
def get_coerce_exclude_unset():
    return Item(aliased_name="coerce", price="1.0")


@app.get(
    "/items/validlist-exclude-unset",
    response_model=list[Item],
    response_model_exclude_unset=True,
)
def get_validlist_exclude_unset():
    return [
        Item(aliased_name="foo"),
        Item(aliased_name="bar", price=1.0),
        Item(aliased_name="baz", price=2.0, owner_ids=[1, 2, 3]),
    ]


@app.get(
    "/items/validdict-exclude-unset",
    response_model=dict[str, Item],
    response_model_exclude_unset=True,
)
def get_validdict_exclude_unset():
    return {
        "k1": Item(aliased_name="foo"),
        "k2": Item(aliased_name="bar", price=1.0),
        "k3": Item(aliased_name="baz", price=2.0, owner_ids=[1, 2, 3]),
    }


client = TestClient(app)


def test_valid():
    response = client.get("/items/valid")
    response.raise_for_status()
    assert response.json() == {"aliased_name": "valid", "price": 1.0, "owner_ids": None}


def test_coerce():
    response = client.get("/items/coerce")
    response.raise_for_status()
    assert response.json() == {
        "aliased_name": "coerce",
        "price": 1.0,
        "owner_ids": None,
    }


def test_validlist():
    response = client.get("/items/validlist")
    response.raise_for_status()
    assert response.json() == [
        {"aliased_name": "foo", "price": None, "owner_ids": None},
        {"aliased_name": "bar", "price": 1.0, "owner_ids": None},
        {"aliased_name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]


def test_validdict():
    response = client.get("/items/validdict")
    response.raise_for_status()
    assert response.json() == {
        "k1": {"aliased_name": "foo", "price": None, "owner_ids": None},
        "k2": {"aliased_name": "bar", "price": 1.0, "owner_ids": None},
        "k3": {"aliased_name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    }


def test_valid_exclude_unset():
    response = client.get("/items/valid-exclude-unset")
    response.raise_for_status()
    assert response.json() == {"aliased_name": "valid", "price": 1.0}


def test_coerce_exclude_unset():
    response = client.get("/items/coerce-exclude-unset")
    response.raise_for_status()
    assert response.json() == {"aliased_name": "coerce", "price": 1.0}


def test_validlist_exclude_unset():
    response = client.get("/items/validlist-exclude-unset")
    response.raise_for_status()
    assert response.json() == [
        {"aliased_name": "foo"},
        {"aliased_name": "bar", "price": 1.0},
        {"aliased_name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    ]


def test_validdict_exclude_unset():
    response = client.get("/items/validdict-exclude-unset")
    response.raise_for_status()
    assert response.json() == {
        "k1": {"aliased_name": "foo"},
        "k2": {"aliased_name": "bar", "price": 1.0},
        "k3": {"aliased_name": "baz", "price": 2.0, "owner_ids": [1, 2, 3]},
    }


if not PYDANTIC_V2:
    from pydantic import validator

    class AutoIncrement(BaseModel):
        count: int

        @validator("count")
        def auto_increment(cls, count: int):
            return count + 1

    @app.post("/increment", response_model=AutoIncrement)
    async def increment():
        return AutoIncrement(count=0)

    def test_response_model_should_not_revalidate_response_content_if_they_had_same_type():
        response = client.post("/increment")
        response.raise_for_status()
        assert response.json() == {"count": 1}
