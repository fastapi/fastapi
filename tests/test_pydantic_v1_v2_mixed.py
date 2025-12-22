import sys
import warnings
from typing import Any, Union

from tests.utils import skip_module_if_py_gte_314

if sys.version_info >= (3, 14):
    skip_module_if_py_gte_314()

from fastapi import FastAPI
from fastapi._compat.v1 import BaseModel
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel as NewBaseModel


class SubItem(BaseModel):
    name: str


class Item(BaseModel):
    title: str
    size: int
    description: Union[str, None] = None
    sub: SubItem
    multi: list[SubItem] = []


class NewSubItem(NewBaseModel):
    new_sub_name: str


class NewItem(NewBaseModel):
    new_title: str
    new_size: int
    new_description: Union[str, None] = None
    new_sub: NewSubItem
    new_multi: list[NewSubItem] = []


app = FastAPI()

with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")

    @app.post("/v1-to-v2/item")
    def handle_v1_item_to_v2(data: Item) -> NewItem:
        return NewItem(
            new_title=data.title,
            new_size=data.size,
            new_description=data.description,
            new_sub=NewSubItem(new_sub_name=data.sub.name),
            new_multi=[NewSubItem(new_sub_name=s.name) for s in data.multi],
        )

    @app.post("/v1-to-v2/item-filter", response_model=NewItem)
    def handle_v1_item_to_v2_filter(data: Item) -> Any:
        result = {
            "new_title": data.title,
            "new_size": data.size,
            "new_description": data.description,
            "new_sub": {
                "new_sub_name": data.sub.name,
                "new_sub_secret": "sub_hidden",
            },
            "new_multi": [
                {"new_sub_name": s.name, "new_sub_secret": "sub_hidden"}
                for s in data.multi
            ],
            "secret": "hidden_v1_to_v2",
        }
        return result

    @app.post("/v2-to-v1/item")
    def handle_v2_item_to_v1(data: NewItem) -> Item:
        return Item(
            title=data.new_title,
            size=data.new_size,
            description=data.new_description,
            sub=SubItem(name=data.new_sub.new_sub_name),
            multi=[SubItem(name=s.new_sub_name) for s in data.new_multi],
        )

    @app.post("/v2-to-v1/item-filter", response_model=Item)
    def handle_v2_item_to_v1_filter(data: NewItem) -> Any:
        result = {
            "title": data.new_title,
            "size": data.new_size,
            "description": data.new_description,
            "sub": {"name": data.new_sub.new_sub_name, "sub_secret": "sub_hidden"},
            "multi": [
                {"name": s.new_sub_name, "sub_secret": "sub_hidden"}
                for s in data.new_multi
            ],
            "secret": "hidden_v2_to_v1",
        }
        return result

    @app.post("/v1-to-v2/item-to-list")
    def handle_v1_item_to_v2_list(data: Item) -> list[NewItem]:
        converted = NewItem(
            new_title=data.title,
            new_size=data.size,
            new_description=data.description,
            new_sub=NewSubItem(new_sub_name=data.sub.name),
            new_multi=[NewSubItem(new_sub_name=s.name) for s in data.multi],
        )
        return [converted, converted]

    @app.post("/v1-to-v2/list-to-list")
    def handle_v1_list_to_v2_list(data: list[Item]) -> list[NewItem]:
        result = []
        for item in data:
            result.append(
                NewItem(
                    new_title=item.title,
                    new_size=item.size,
                    new_description=item.description,
                    new_sub=NewSubItem(new_sub_name=item.sub.name),
                    new_multi=[NewSubItem(new_sub_name=s.name) for s in item.multi],
                )
            )
        return result

    @app.post("/v1-to-v2/list-to-list-filter", response_model=list[NewItem])
    def handle_v1_list_to_v2_list_filter(data: list[Item]) -> Any:
        result = []
        for item in data:
            converted = {
                "new_title": item.title,
                "new_size": item.size,
                "new_description": item.description,
                "new_sub": {
                    "new_sub_name": item.sub.name,
                    "new_sub_secret": "sub_hidden",
                },
                "new_multi": [
                    {"new_sub_name": s.name, "new_sub_secret": "sub_hidden"}
                    for s in item.multi
                ],
                "secret": "hidden_v2_to_v1",
            }
            result.append(converted)
        return result

    @app.post("/v1-to-v2/list-to-item")
    def handle_v1_list_to_v2_item(data: list[Item]) -> NewItem:
        if data:
            item = data[0]
            return NewItem(
                new_title=item.title,
                new_size=item.size,
                new_description=item.description,
                new_sub=NewSubItem(new_sub_name=item.sub.name),
                new_multi=[NewSubItem(new_sub_name=s.name) for s in item.multi],
            )
        return NewItem(new_title="", new_size=0, new_sub=NewSubItem(new_sub_name=""))

    @app.post("/v2-to-v1/item-to-list")
    def handle_v2_item_to_v1_list(data: NewItem) -> list[Item]:
        converted = Item(
            title=data.new_title,
            size=data.new_size,
            description=data.new_description,
            sub=SubItem(name=data.new_sub.new_sub_name),
            multi=[SubItem(name=s.new_sub_name) for s in data.new_multi],
        )
        return [converted, converted]

    @app.post("/v2-to-v1/list-to-list")
    def handle_v2_list_to_v1_list(data: list[NewItem]) -> list[Item]:
        result = []
        for item in data:
            result.append(
                Item(
                    title=item.new_title,
                    size=item.new_size,
                    description=item.new_description,
                    sub=SubItem(name=item.new_sub.new_sub_name),
                    multi=[SubItem(name=s.new_sub_name) for s in item.new_multi],
                )
            )
        return result

    @app.post("/v2-to-v1/list-to-list-filter", response_model=list[Item])
    def handle_v2_list_to_v1_list_filter(data: list[NewItem]) -> Any:
        result = []
        for item in data:
            converted = {
                "title": item.new_title,
                "size": item.new_size,
                "description": item.new_description,
                "sub": {
                    "name": item.new_sub.new_sub_name,
                    "sub_secret": "sub_hidden",
                },
                "multi": [
                    {"name": s.new_sub_name, "sub_secret": "sub_hidden"}
                    for s in item.new_multi
                ],
                "secret": "hidden_v2_to_v1",
            }
            result.append(converted)
        return result

    @app.post("/v2-to-v1/list-to-item")
    def handle_v2_list_to_v1_item(data: list[NewItem]) -> Item:
        if data:
            item = data[0]
            return Item(
                title=item.new_title,
                size=item.new_size,
                description=item.new_description,
                sub=SubItem(name=item.new_sub.new_sub_name),
                multi=[SubItem(name=s.new_sub_name) for s in item.new_multi],
            )
        return Item(title="", size=0, sub=SubItem(name=""))


client = TestClient(app)


def test_v1_to_v2_item():
    response = client.post(
        "/v1-to-v2/item",
        json={
            "title": "Old Item",
            "size": 100,
            "description": "V1 description",
            "sub": {"name": "V1 Sub"},
            "multi": [{"name": "M1"}, {"name": "M2"}],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "new_title": "Old Item",
        "new_size": 100,
        "new_description": "V1 description",
        "new_sub": {"new_sub_name": "V1 Sub"},
        "new_multi": [{"new_sub_name": "M1"}, {"new_sub_name": "M2"}],
    }


def test_v1_to_v2_item_minimal():
    response = client.post(
        "/v1-to-v2/item",
        json={"title": "Minimal", "size": 50, "sub": {"name": "MinSub"}},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "new_title": "Minimal",
        "new_size": 50,
        "new_description": None,
        "new_sub": {"new_sub_name": "MinSub"},
        "new_multi": [],
    }


def test_v1_to_v2_item_filter():
    response = client.post(
        "/v1-to-v2/item-filter",
        json={
            "title": "Filtered Item",
            "size": 50,
            "sub": {"name": "Sub"},
            "multi": [{"name": "Multi1"}],
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == snapshot(
        {
            "new_title": "Filtered Item",
            "new_size": 50,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub"},
            "new_multi": [{"new_sub_name": "Multi1"}],
        }
    )
    # Verify secret fields are filtered out
    assert "secret" not in result
    assert "new_sub_secret" not in result["new_sub"]
    assert "new_sub_secret" not in result["new_multi"][0]


def test_v2_to_v1_item():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "New Item",
            "new_size": 200,
            "new_description": "V2 description",
            "new_sub": {"new_sub_name": "V2 Sub"},
            "new_multi": [{"new_sub_name": "N1"}, {"new_sub_name": "N2"}],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "New Item",
        "size": 200,
        "description": "V2 description",
        "sub": {"name": "V2 Sub"},
        "multi": [{"name": "N1"}, {"name": "N2"}],
    }


def test_v2_to_v1_item_minimal():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "MinimalNew",
            "new_size": 75,
            "new_sub": {"new_sub_name": "MinNewSub"},
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "MinimalNew",
        "size": 75,
        "description": None,
        "sub": {"name": "MinNewSub"},
        "multi": [],
    }


def test_v2_to_v1_item_filter():
    response = client.post(
        "/v2-to-v1/item-filter",
        json={
            "new_title": "Filtered New",
            "new_size": 75,
            "new_sub": {"new_sub_name": "NewSub"},
            "new_multi": [],
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == snapshot(
        {
            "title": "Filtered New",
            "size": 75,
            "description": None,
            "sub": {"name": "NewSub"},
            "multi": [],
        }
    )
    # Verify secret fields are filtered out
    assert "secret" not in result
    assert "sub_secret" not in result["sub"]


def test_v1_item_to_v2_list():
    response = client.post(
        "/v1-to-v2/item-to-list",
        json={
            "title": "Single to List",
            "size": 150,
            "description": "Convert to list",
            "sub": {"name": "Sub1"},
            "multi": [],
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == [
        {
            "new_title": "Single to List",
            "new_size": 150,
            "new_description": "Convert to list",
            "new_sub": {"new_sub_name": "Sub1"},
            "new_multi": [],
        },
        {
            "new_title": "Single to List",
            "new_size": 150,
            "new_description": "Convert to list",
            "new_sub": {"new_sub_name": "Sub1"},
            "new_multi": [],
        },
    ]


def test_v1_list_to_v2_list():
    response = client.post(
        "/v1-to-v2/list-to-list",
        json=[
            {"title": "Item1", "size": 10, "sub": {"name": "Sub1"}},
            {
                "title": "Item2",
                "size": 20,
                "description": "Second item",
                "sub": {"name": "Sub2"},
                "multi": [{"name": "M1"}, {"name": "M2"}],
            },
            {"title": "Item3", "size": 30, "sub": {"name": "Sub3"}},
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "new_title": "Item1",
            "new_size": 10,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub1"},
            "new_multi": [],
        },
        {
            "new_title": "Item2",
            "new_size": 20,
            "new_description": "Second item",
            "new_sub": {"new_sub_name": "Sub2"},
            "new_multi": [{"new_sub_name": "M1"}, {"new_sub_name": "M2"}],
        },
        {
            "new_title": "Item3",
            "new_size": 30,
            "new_description": None,
            "new_sub": {"new_sub_name": "Sub3"},
            "new_multi": [],
        },
    ]


def test_v1_list_to_v2_list_filter():
    response = client.post(
        "/v1-to-v2/list-to-list-filter",
        json=[{"title": "FilterMe", "size": 30, "sub": {"name": "SubF"}}],
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == snapshot(
        [
            {
                "new_title": "FilterMe",
                "new_size": 30,
                "new_description": None,
                "new_sub": {"new_sub_name": "SubF"},
                "new_multi": [],
            }
        ]
    )
    # Verify secret fields are filtered out
    assert "secret" not in result[0]
    assert "new_sub_secret" not in result[0]["new_sub"]


def test_v1_list_to_v2_item():
    response = client.post(
        "/v1-to-v2/list-to-item",
        json=[
            {"title": "First", "size": 100, "sub": {"name": "FirstSub"}},
            {"title": "Second", "size": 200, "sub": {"name": "SecondSub"}},
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "new_title": "First",
        "new_size": 100,
        "new_description": None,
        "new_sub": {"new_sub_name": "FirstSub"},
        "new_multi": [],
    }


def test_v1_list_to_v2_item_empty():
    response = client.post("/v1-to-v2/list-to-item", json=[])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "new_title": "",
        "new_size": 0,
        "new_description": None,
        "new_sub": {"new_sub_name": ""},
        "new_multi": [],
    }


def test_v2_item_to_v1_list():
    response = client.post(
        "/v2-to-v1/item-to-list",
        json={
            "new_title": "Single New",
            "new_size": 250,
            "new_description": "New to list",
            "new_sub": {"new_sub_name": "NewSub"},
            "new_multi": [],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "title": "Single New",
            "size": 250,
            "description": "New to list",
            "sub": {"name": "NewSub"},
            "multi": [],
        },
        {
            "title": "Single New",
            "size": 250,
            "description": "New to list",
            "sub": {"name": "NewSub"},
            "multi": [],
        },
    ]


def test_v2_list_to_v1_list():
    response = client.post(
        "/v2-to-v1/list-to-list",
        json=[
            {"new_title": "New1", "new_size": 15, "new_sub": {"new_sub_name": "NS1"}},
            {
                "new_title": "New2",
                "new_size": 25,
                "new_description": "Second new",
                "new_sub": {"new_sub_name": "NS2"},
                "new_multi": [{"new_sub_name": "NM1"}],
            },
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "title": "New1",
            "size": 15,
            "description": None,
            "sub": {"name": "NS1"},
            "multi": [],
        },
        {
            "title": "New2",
            "size": 25,
            "description": "Second new",
            "sub": {"name": "NS2"},
            "multi": [{"name": "NM1"}],
        },
    ]


def test_v2_list_to_v1_list_filter():
    response = client.post(
        "/v2-to-v1/list-to-list-filter",
        json=[
            {
                "new_title": "FilterNew",
                "new_size": 35,
                "new_sub": {"new_sub_name": "NSF"},
            }
        ],
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == snapshot(
        [
            {
                "title": "FilterNew",
                "size": 35,
                "description": None,
                "sub": {"name": "NSF"},
                "multi": [],
            }
        ]
    )
    # Verify secret fields are filtered out
    assert "secret" not in result[0]
    assert "sub_secret" not in result[0]["sub"]


def test_v2_list_to_v1_item():
    response = client.post(
        "/v2-to-v1/list-to-item",
        json=[
            {
                "new_title": "FirstNew",
                "new_size": 300,
                "new_sub": {"new_sub_name": "FNS"},
            },
            {
                "new_title": "SecondNew",
                "new_size": 400,
                "new_sub": {"new_sub_name": "SNS"},
            },
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "FirstNew",
        "size": 300,
        "description": None,
        "sub": {"name": "FNS"},
        "multi": [],
    }


def test_v2_list_to_v1_item_empty():
    response = client.post("/v2-to-v1/list-to-item", json=[])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "",
        "size": 0,
        "description": None,
        "sub": {"name": ""},
        "multi": [],
    }


def test_v1_to_v2_validation_error():
    response = client.post("/v1-to-v2/item", json={"title": "Missing fields"})
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "size"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "sub"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_v1_to_v2_nested_validation_error():
    response = client.post(
        "/v1-to-v2/item",
        json={"title": "Bad sub", "size": 100, "sub": {"wrong_field": "value"}},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "sub", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_v1_to_v2_type_validation_error():
    response = client.post(
        "/v1-to-v2/item",
        json={"title": "Bad type", "size": "not_a_number", "sub": {"name": "Sub"}},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", "size"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_v2_to_v1_validation_error():
    response = client.post(
        "/v2-to-v1/item",
        json={"new_title": "Missing fields"},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "new_size"],
                    "msg": "Field required",
                    "input": {"new_title": "Missing fields"},
                },
                {
                    "type": "missing",
                    "loc": ["body", "new_sub"],
                    "msg": "Field required",
                    "input": {"new_title": "Missing fields"},
                },
            ]
        }
    )


def test_v2_to_v1_nested_validation_error():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "Bad sub",
            "new_size": 200,
            "new_sub": {"wrong_field": "value"},
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "new_sub", "new_sub_name"],
                    "msg": "Field required",
                    "input": {"wrong_field": "value"},
                }
            ]
        }
    )


def test_v1_list_validation_error():
    response = client.post(
        "/v1-to-v2/list-to-list",
        json=[
            {"title": "Valid", "size": 10, "sub": {"name": "S"}},
            {"title": "Invalid"},
        ],
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", 1, "size"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", 1, "sub"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


def test_v2_list_validation_error():
    response = client.post(
        "/v2-to-v1/list-to-list",
        json=[
            {"new_title": "Valid", "new_size": 10, "new_sub": {"new_sub_name": "NS"}},
            {"new_title": "Invalid"},
        ],
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", 1, "new_size"],
                    "msg": "Field required",
                    "input": {"new_title": "Invalid"},
                },
                {
                    "type": "missing",
                    "loc": ["body", 1, "new_sub"],
                    "msg": "Field required",
                    "input": {"new_title": "Invalid"},
                },
            ]
        }
    )


def test_invalid_list_structure_v1():
    response = client.post(
        "/v1-to-v2/list-to-list",
        json={"title": "Not a list", "size": 100, "sub": {"name": "Sub"}},
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "value is not a valid list",
                    "type": "type_error.list",
                }
            ]
        }
    )


def test_invalid_list_structure_v2():
    response = client.post(
        "/v2-to-v1/list-to-list",
        json={
            "new_title": "Not a list",
            "new_size": 100,
            "new_sub": {"new_sub_name": "Sub"},
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "type": "list_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid list",
                    "input": {
                        "new_title": "Not a list",
                        "new_size": 100,
                        "new_sub": {"new_sub_name": "Sub"},
                    },
                }
            ]
        }
    )


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/v1-to-v2/item": {
                    "post": {
                        "summary": "Handle V1 Item To V2",
                        "operationId": "handle_v1_item_to_v2_v1_to_v2_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/NewItem"
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v1-to-v2/item-filter": {
                    "post": {
                        "summary": "Handle V1 Item To V2 Filter",
                        "operationId": "handle_v1_item_to_v2_filter_v1_to_v2_item_filter_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/NewItem"
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v2-to-v1/item": {
                    "post": {
                        "summary": "Handle V2 Item To V1",
                        "operationId": "handle_v2_item_to_v1_v2_to_v1_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/NewItem"}
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v2-to-v1/item-filter": {
                    "post": {
                        "summary": "Handle V2 Item To V1 Filter",
                        "operationId": "handle_v2_item_to_v1_filter_v2_to_v1_item_filter_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/NewItem"}
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v1-to-v2/item-to-list": {
                    "post": {
                        "summary": "Handle V1 Item To V2 List",
                        "operationId": "handle_v1_item_to_v2_list_v1_to_v2_item_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "allOf": [
                                            {"$ref": "#/components/schemas/Item"}
                                        ],
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {
                                                "$ref": "#/components/schemas/NewItem"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V1 Item To V2 List V1 To V2 Item To List Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v1-to-v2/list-to-list": {
                    "post": {
                        "summary": "Handle V1 List To V2 List",
                        "operationId": "handle_v1_list_to_v2_list_v1_to_v2_list_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {"$ref": "#/components/schemas/Item"},
                                        "type": "array",
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {
                                                "$ref": "#/components/schemas/NewItem"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V1 List To V2 List V1 To V2 List To List Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v1-to-v2/list-to-list-filter": {
                    "post": {
                        "summary": "Handle V1 List To V2 List Filter",
                        "operationId": "handle_v1_list_to_v2_list_filter_v1_to_v2_list_to_list_filter_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {"$ref": "#/components/schemas/Item"},
                                        "type": "array",
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {
                                                "$ref": "#/components/schemas/NewItem"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V1 List To V2 List Filter V1 To V2 List To List Filter Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v1-to-v2/list-to-item": {
                    "post": {
                        "summary": "Handle V1 List To V2 Item",
                        "operationId": "handle_v1_list_to_v2_item_v1_to_v2_list_to_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {"$ref": "#/components/schemas/Item"},
                                        "type": "array",
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/NewItem"
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v2-to-v1/item-to-list": {
                    "post": {
                        "summary": "Handle V2 Item To V1 List",
                        "operationId": "handle_v2_item_to_v1_list_v2_to_v1_item_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/NewItem"}
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V2 Item To V1 List V2 To V1 Item To List Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v2-to-v1/list-to-list": {
                    "post": {
                        "summary": "Handle V2 List To V1 List",
                        "operationId": "handle_v2_list_to_v1_list_v2_to_v1_list_to_list_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/NewItem"
                                        },
                                        "type": "array",
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V2 List To V1 List V2 To V1 List To List Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v2-to-v1/list-to-list-filter": {
                    "post": {
                        "summary": "Handle V2 List To V1 List Filter",
                        "operationId": "handle_v2_list_to_v1_list_filter_v2_to_v1_list_to_list_filter_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/NewItem"
                                        },
                                        "type": "array",
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "items": {
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle V2 List To V1 List Filter V2 To V1 List To List Filter Post",
                                        }
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
                "/v2-to-v1/list-to-item": {
                    "post": {
                        "summary": "Handle V2 List To V1 Item",
                        "operationId": "handle_v2_list_to_v1_item_v2_to_v1_list_to_item_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/NewItem"
                                        },
                                        "type": "array",
                                        "title": "Data",
                                    }
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {"$ref": "#/components/schemas/Item"}
                                    }
                                },
                            },
                            "422": {
                                "description": "Validation Error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/HTTPValidationError"
                                        }
                                    }
                                },
                            },
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                                "type": "array",
                                "title": "Detail",
                            }
                        },
                        "type": "object",
                        "title": "HTTPValidationError",
                    },
                    "Item": {
                        "properties": {
                            "title": {"type": "string", "title": "Title"},
                            "size": {"type": "integer", "title": "Size"},
                            "description": {"type": "string", "title": "Description"},
                            "sub": {"$ref": "#/components/schemas/SubItem"},
                            "multi": {
                                "items": {"$ref": "#/components/schemas/SubItem"},
                                "type": "array",
                                "title": "Multi",
                                "default": [],
                            },
                        },
                        "type": "object",
                        "required": ["title", "size", "sub"],
                        "title": "Item",
                    },
                    "NewItem": {
                        "properties": {
                            "new_title": {"type": "string", "title": "New Title"},
                            "new_size": {"type": "integer", "title": "New Size"},
                            "new_description": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "New Description",
                            },
                            "new_sub": {"$ref": "#/components/schemas/NewSubItem"},
                            "new_multi": {
                                "items": {"$ref": "#/components/schemas/NewSubItem"},
                                "type": "array",
                                "title": "New Multi",
                                "default": [],
                            },
                        },
                        "type": "object",
                        "required": ["new_title", "new_size", "new_sub"],
                        "title": "NewItem",
                    },
                    "NewSubItem": {
                        "properties": {
                            "new_sub_name": {"type": "string", "title": "New Sub Name"}
                        },
                        "type": "object",
                        "required": ["new_sub_name"],
                        "title": "NewSubItem",
                    },
                    "SubItem": {
                        "properties": {"name": {"type": "string", "title": "Name"}},
                        "type": "object",
                        "required": ["name"],
                        "title": "SubItem",
                    },
                    "ValidationError": {
                        "properties": {
                            "loc": {
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                                "type": "array",
                                "title": "Location",
                            },
                            "msg": {"type": "string", "title": "Message"},
                            "type": {"type": "string", "title": "Error Type"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
