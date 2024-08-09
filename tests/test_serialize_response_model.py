from typing import Dict, List, Optional

import pytest
from fastapi import FastAPI
from fastapi._compat import PYDANTIC_V2, PYDANTIC_VERSION
from pydantic import BaseModel, Field
from starlette.testclient import TestClient

app = FastAPI()


class Item(BaseModel):
    name: str = Field(alias="aliased_name")
    price: Optional[float] = None
    owner_ids: Optional[List[int]] = None


@app.get("/items/valid", response_model=Item)
def get_valid():
    return Item(aliased_name="valid", price=1.0)


@app.get("/items/coerce", response_model=Item)
def get_coerce():
    return Item(aliased_name="coerce", price="1.0")


@app.get("/items/validlist", response_model=List[Item])
def get_validlist():
    return [
        Item(aliased_name="foo"),
        Item(aliased_name="bar", price=1.0),
        Item(aliased_name="baz", price=2.0, owner_ids=[1, 2, 3]),
    ]


@app.get("/items/validdict", response_model=Dict[str, Item])
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
    response_model=List[Item],
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
    response_model=Dict[str, Item],
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


if PYDANTIC_V2:
    from pydantic import SerializationInfo, model_serializer

    class MultiUseItem(BaseModel):
        name: str = Field(alias="aliased_name")
        secret: Optional[str] = None
        owner_ids: Optional[List[int]] = None

        @model_serializer(mode="wrap")
        def _serialize(self, handler, info: SerializationInfo):
            data = handler(self)
            if info.context and info.context.get("mode") == "FASTAPI":
                if "secret" in data:
                    data.pop("secret")
            return data

    app_v2 = FastAPI()

    @app_v2.get(
        "/items/validdict-with-context",
        response_model=Dict[str, MultiUseItem],
        response_model_context={"mode": "FASTAPI"},
    )
    async def get_validdict_with_context():
        return {
            "k1": MultiUseItem(aliased_name="foo"),
            "k2": MultiUseItem(aliased_name="bar", secret="sEcReT"),
            "k3": MultiUseItem(
                aliased_name="baz", secret="sEcReT", owner_ids=[1, 2, 3]
            ),
        }

    client_v2 = TestClient(app_v2)

    @pytest.mark.skipif(PYDANTIC_VERSION < "2.8", reason="requires Pydantic v2.8+")
    def test_validdict_with_context__pydantic_supported():
        response = client_v2.get("/items/validdict-with-context")
        response.raise_for_status()

        expected_response = {
            "k1": {"aliased_name": "foo", "owner_ids": None},
            "k2": {"aliased_name": "bar", "owner_ids": None},
            "k3": {"aliased_name": "baz", "owner_ids": [1, 2, 3]},
        }

        assert response.json() == expected_response

    @pytest.mark.skipif(
        PYDANTIC_VERSION >= "2.8",
        reason="Pydantic supports the feature from this point on",
    )
    def test_validdict_with_context__pre_pydantic_support():
        response = client_v2.get("/items/validdict-with-context")
        response.raise_for_status()

        expected_response = {
            "k1": {"aliased_name": "foo", "owner_ids": None, "secret": None},
            "k2": {"aliased_name": "bar", "owner_ids": None, "secret": "sEcReT"},
            "k3": {"aliased_name": "baz", "owner_ids": [1, 2, 3], "secret": "sEcReT"},
        }

        assert response.json() == expected_response
