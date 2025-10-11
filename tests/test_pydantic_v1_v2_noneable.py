import sys
from typing import Any, List, Union

from tests.utils import pydantic_snapshot, skip_module_if_py_gte_314

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
    multi: List[SubItem] = []


class NewSubItem(NewBaseModel):
    new_sub_name: str


class NewItem(NewBaseModel):
    new_title: str
    new_size: int
    new_description: Union[str, None] = None
    new_sub: NewSubItem
    new_multi: List[NewSubItem] = []


app = FastAPI()


@app.post("/v1-to-v2/")
def handle_v1_item_to_v2(data: Item) -> Union[NewItem, None]:
    if data.size < 0:
        return None
    return NewItem(
        new_title=data.title,
        new_size=data.size,
        new_description=data.description,
        new_sub=NewSubItem(new_sub_name=data.sub.name),
        new_multi=[NewSubItem(new_sub_name=s.name) for s in data.multi],
    )


@app.post("/v1-to-v2/item-filter", response_model=Union[NewItem, None])
def handle_v1_item_to_v2_filter(data: Item) -> Any:
    if data.size < 0:
        return None
    result = {
        "new_title": data.title,
        "new_size": data.size,
        "new_description": data.description,
        "new_sub": {"new_sub_name": data.sub.name, "new_sub_secret": "sub_hidden"},
        "new_multi": [
            {"new_sub_name": s.name, "new_sub_secret": "sub_hidden"} for s in data.multi
        ],
        "secret": "hidden_v1_to_v2",
    }
    return result


@app.post("/v2-to-v1/item")
def handle_v2_item_to_v1(data: NewItem) -> Union[Item, None]:
    if data.new_size < 0:
        return None
    return Item(
        title=data.new_title,
        size=data.new_size,
        description=data.new_description,
        sub=SubItem(name=data.new_sub.new_sub_name),
        multi=[SubItem(name=s.new_sub_name) for s in data.new_multi],
    )


@app.post("/v2-to-v1/item-filter", response_model=Union[Item, None])
def handle_v2_item_to_v1_filter(data: NewItem) -> Any:
    if data.new_size < 0:
        return None
    result = {
        "title": data.new_title,
        "size": data.new_size,
        "description": data.new_description,
        "sub": {"name": data.new_sub.new_sub_name, "sub_secret": "sub_hidden"},
        "multi": [
            {"name": s.new_sub_name, "sub_secret": "sub_hidden"} for s in data.new_multi
        ],
        "secret": "hidden_v2_to_v1",
    }
    return result


client = TestClient(app)


def test_v1_to_v2_item_success():
    response = client.post(
        "/v1-to-v2/",
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


def test_v1_to_v2_item_returns_none():
    response = client.post(
        "/v1-to-v2/",
        json={"title": "Invalid Item", "size": -10, "sub": {"name": "Sub"}},
    )
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_v1_to_v2_item_minimal():
    response = client.post(
        "/v1-to-v2/", json={"title": "Minimal", "size": 50, "sub": {"name": "MinSub"}}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "new_title": "Minimal",
        "new_size": 50,
        "new_description": None,
        "new_sub": {"new_sub_name": "MinSub"},
        "new_multi": [],
    }


def test_v1_to_v2_item_filter_success():
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
    assert result["new_title"] == "Filtered Item"
    assert result["new_size"] == 50
    assert result["new_sub"]["new_sub_name"] == "Sub"
    assert result["new_multi"][0]["new_sub_name"] == "Multi1"
    # Verify secret fields are filtered out
    assert "secret" not in result
    assert "new_sub_secret" not in result["new_sub"]
    assert "new_sub_secret" not in result["new_multi"][0]


def test_v1_to_v2_item_filter_returns_none():
    response = client.post(
        "/v1-to-v2/item-filter",
        json={"title": "Invalid", "size": -1, "sub": {"name": "Sub"}},
    )
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_v2_to_v1_item_success():
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


def test_v2_to_v1_item_returns_none():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "Invalid New",
            "new_size": -5,
            "new_sub": {"new_sub_name": "NewSub"},
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() is None


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


def test_v2_to_v1_item_filter_success():
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
    assert result["title"] == "Filtered New"
    assert result["size"] == 75
    assert result["sub"]["name"] == "NewSub"
    # Verify secret fields are filtered out
    assert "secret" not in result
    assert "sub_secret" not in result["sub"]


def test_v2_to_v1_item_filter_returns_none():
    response = client.post(
        "/v2-to-v1/item-filter",
        json={
            "new_title": "Invalid Filtered",
            "new_size": -100,
            "new_sub": {"new_sub_name": "Sub"},
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() is None


def test_v1_to_v2_validation_error():
    response = client.post("/v1-to-v2/", json={"title": "Missing fields"})
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
        "/v1-to-v2/",
        json={"title": "Bad sub", "size": 100, "sub": {"wrong_field": "value"}},
    )
    assert response.status_code == 422, response.text
    error_detail = response.json()["detail"]
    assert len(error_detail) == 1
    assert error_detail[0]["loc"] == ["body", "sub", "name"]


def test_v1_to_v2_type_validation_error():
    response = client.post(
        "/v1-to-v2/",
        json={"title": "Bad type", "size": "not_a_number", "sub": {"name": "Sub"}},
    )
    assert response.status_code == 422, response.text
    error_detail = response.json()["detail"]
    assert len(error_detail) == 1
    assert error_detail[0]["loc"] == ["body", "size"]


def test_v2_to_v1_validation_error():
    response = client.post("/v2-to-v1/item", json={"new_title": "Missing fields"})
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": pydantic_snapshot(
                v2=snapshot(
                    [
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
                ),
                v1=snapshot(
                    [
                        {
                            "loc": ["body", "new_size"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                        {
                            "loc": ["body", "new_sub"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                    ]
                ),
            )
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
                pydantic_snapshot(
                    v2=snapshot(
                        {
                            "type": "missing",
                            "loc": ["body", "new_sub", "new_sub_name"],
                            "msg": "Field required",
                            "input": {"wrong_field": "value"},
                        }
                    ),
                    v1=snapshot(
                        {
                            "loc": ["body", "new_sub", "new_sub_name"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        }
                    ),
                )
            ]
        }
    )


def test_v2_to_v1_type_validation_error():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "Bad type",
            "new_size": "not_a_number",
            "new_sub": {"new_sub_name": "Sub"},
        },
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                pydantic_snapshot(
                    v2=snapshot(
                        {
                            "type": "int_parsing",
                            "loc": ["body", "new_size"],
                            "msg": "Input should be a valid integer, unable to parse string as an integer",
                            "input": "not_a_number",
                        }
                    ),
                    v1=snapshot(
                        {
                            "loc": ["body", "new_size"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ),
                )
            ]
        }
    )


def test_v1_to_v2_with_multi_items():
    response = client.post(
        "/v1-to-v2/",
        json={
            "title": "Complex Item",
            "size": 300,
            "description": "Item with multiple sub-items",
            "sub": {"name": "Main Sub"},
            "multi": [{"name": "Sub1"}, {"name": "Sub2"}, {"name": "Sub3"}],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "new_title": "Complex Item",
            "new_size": 300,
            "new_description": "Item with multiple sub-items",
            "new_sub": {"new_sub_name": "Main Sub"},
            "new_multi": [
                {"new_sub_name": "Sub1"},
                {"new_sub_name": "Sub2"},
                {"new_sub_name": "Sub3"},
            ],
        }
    )


def test_v2_to_v1_with_multi_items():
    response = client.post(
        "/v2-to-v1/item",
        json={
            "new_title": "Complex New Item",
            "new_size": 400,
            "new_description": "New item with multiple sub-items",
            "new_sub": {"new_sub_name": "Main New Sub"},
            "new_multi": [{"new_sub_name": "NewSub1"}, {"new_sub_name": "NewSub2"}],
        },
    )
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "title": "Complex New Item",
            "size": 400,
            "description": "New item with multiple sub-items",
            "sub": {"name": "Main New Sub"},
            "multi": [{"name": "NewSub1"}, {"name": "NewSub2"}],
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
                "/v1-to-v2/": {
                    "post": {
                        "summary": "Handle V1 Item To V2",
                        "operationId": "handle_v1_item_to_v2_v1_to_v2__post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": pydantic_snapshot(
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Item"
                                                    }
                                                ],
                                                "title": "Data",
                                            }
                                        ),
                                        v1=snapshot(
                                            {"$ref": "#/components/schemas/Item"}
                                        ),
                                    )
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": pydantic_snapshot(
                                            v2=snapshot(
                                                {
                                                    "anyOf": [
                                                        {
                                                            "$ref": "#/components/schemas/NewItem"
                                                        },
                                                        {"type": "null"},
                                                    ],
                                                    "title": "Response Handle V1 Item To V2 V1 To V2  Post",
                                                }
                                            ),
                                            v1=snapshot(
                                                {"$ref": "#/components/schemas/NewItem"}
                                            ),
                                        )
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
                                    "schema": pydantic_snapshot(
                                        v2=snapshot(
                                            {
                                                "allOf": [
                                                    {
                                                        "$ref": "#/components/schemas/Item"
                                                    }
                                                ],
                                                "title": "Data",
                                            }
                                        ),
                                        v1=snapshot(
                                            {"$ref": "#/components/schemas/Item"}
                                        ),
                                    )
                                }
                            },
                            "required": True,
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": pydantic_snapshot(
                                            v2=snapshot(
                                                {
                                                    "anyOf": [
                                                        {
                                                            "$ref": "#/components/schemas/NewItem"
                                                        },
                                                        {"type": "null"},
                                                    ],
                                                    "title": "Response Handle V1 Item To V2 Filter V1 To V2 Item Filter Post",
                                                }
                                            ),
                                            v1=snapshot(
                                                {"$ref": "#/components/schemas/NewItem"}
                                            ),
                                        )
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
                            "new_description": pydantic_snapshot(
                                v2=snapshot(
                                    {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "New Description",
                                    }
                                ),
                                v1=snapshot(
                                    {"type": "string", "title": "New Description"}
                                ),
                            ),
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
