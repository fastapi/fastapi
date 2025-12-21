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


class SubItem(BaseModel):
    name: str


class Item(BaseModel):
    title: str
    size: int
    description: Union[str, None] = None
    sub: SubItem
    multi: list[SubItem] = []


app = FastAPI()


with warnings.catch_warnings(record=True):
    warnings.simplefilter("always")

    @app.post("/item")
    def handle_item(data: Item) -> list[Item]:
        return [data, data]

    @app.post("/item-filter", response_model=list[Item])
    def handle_item_filter(data: Item) -> Any:
        extended_data = data.dict()
        extended_data.update({"secret_data": "classified", "internal_id": 12345})
        extended_data["sub"].update({"internal_id": 67890})
        return [extended_data, extended_data]

    @app.post("/item-list")
    def handle_item_list(data: list[Item]) -> Item:
        if data:
            return data[0]
        return Item(title="", size=0, sub=SubItem(name=""))

    @app.post("/item-list-filter", response_model=Item)
    def handle_item_list_filter(data: list[Item]) -> Any:
        if data:
            extended_data = data[0].dict()
            extended_data.update({"secret_data": "classified", "internal_id": 12345})
            extended_data["sub"].update({"internal_id": 67890})
            return extended_data
        return Item(title="", size=0, sub=SubItem(name=""))

    @app.post("/item-list-to-list")
    def handle_item_list_to_list(data: list[Item]) -> list[Item]:
        return data

    @app.post("/item-list-to-list-filter", response_model=list[Item])
    def handle_item_list_to_list_filter(data: list[Item]) -> Any:
        if data:
            extended_data = data[0].dict()
            extended_data.update({"secret_data": "classified", "internal_id": 12345})
            extended_data["sub"].update({"internal_id": 67890})
            return [extended_data, extended_data]
        return []


client = TestClient(app)


def test_item_to_list():
    response = client.post(
        "/item",
        json={
            "title": "Test Item",
            "size": 100,
            "description": "This is a test item",
            "sub": {"name": "SubItem1"},
            "multi": [{"name": "Multi1"}, {"name": "Multi2"}],
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    for item in result:
        assert item == {
            "title": "Test Item",
            "size": 100,
            "description": "This is a test item",
            "sub": {"name": "SubItem1"},
            "multi": [{"name": "Multi1"}, {"name": "Multi2"}],
        }


def test_item_to_list_filter():
    response = client.post(
        "/item-filter",
        json={
            "title": "Filtered Item",
            "size": 200,
            "description": "Test filtering",
            "sub": {"name": "SubFiltered"},
            "multi": [],
        },
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    for item in result:
        assert item == {
            "title": "Filtered Item",
            "size": 200,
            "description": "Test filtering",
            "sub": {"name": "SubFiltered"},
            "multi": [],
        }
        # Verify secret fields are filtered out
        assert "secret_data" not in item
        assert "internal_id" not in item
        assert "internal_id" not in item["sub"]


def test_list_to_item():
    response = client.post(
        "/item-list",
        json=[
            {"title": "First Item", "size": 50, "sub": {"name": "First Sub"}},
            {"title": "Second Item", "size": 75, "sub": {"name": "Second Sub"}},
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "First Item",
        "size": 50,
        "description": None,
        "sub": {"name": "First Sub"},
        "multi": [],
    }


def test_list_to_item_empty():
    response = client.post(
        "/item-list",
        json=[],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "",
        "size": 0,
        "description": None,
        "sub": {"name": ""},
        "multi": [],
    }


def test_list_to_item_filter():
    response = client.post(
        "/item-list-filter",
        json=[
            {
                "title": "First Item",
                "size": 100,
                "sub": {"name": "First Sub"},
                "multi": [{"name": "Multi1"}],
            },
            {"title": "Second Item", "size": 200, "sub": {"name": "Second Sub"}},
        ],
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert result == {
        "title": "First Item",
        "size": 100,
        "description": None,
        "sub": {"name": "First Sub"},
        "multi": [{"name": "Multi1"}],
    }
    # Verify secret fields are filtered out
    assert "secret_data" not in result
    assert "internal_id" not in result


def test_list_to_item_filter_no_data():
    response = client.post("/item-list-filter", json=[])
    assert response.status_code == 200, response.text
    assert response.json() == {
        "title": "",
        "size": 0,
        "description": None,
        "sub": {"name": ""},
        "multi": [],
    }


def test_list_to_list():
    input_items = [
        {"title": "Item 1", "size": 10, "sub": {"name": "Sub1"}},
        {
            "title": "Item 2",
            "size": 20,
            "description": "Second item",
            "sub": {"name": "Sub2"},
            "multi": [{"name": "M1"}, {"name": "M2"}],
        },
        {"title": "Item 3", "size": 30, "sub": {"name": "Sub3"}},
    ]
    response = client.post(
        "/item-list-to-list",
        json=input_items,
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0] == {
        "title": "Item 1",
        "size": 10,
        "description": None,
        "sub": {"name": "Sub1"},
        "multi": [],
    }
    assert result[1] == {
        "title": "Item 2",
        "size": 20,
        "description": "Second item",
        "sub": {"name": "Sub2"},
        "multi": [{"name": "M1"}, {"name": "M2"}],
    }
    assert result[2] == {
        "title": "Item 3",
        "size": 30,
        "description": None,
        "sub": {"name": "Sub3"},
        "multi": [],
    }


def test_list_to_list_filter():
    response = client.post(
        "/item-list-to-list-filter",
        json=[{"title": "Item 1", "size": 100, "sub": {"name": "Sub1"}}],
    )
    assert response.status_code == 200, response.text
    result = response.json()
    assert isinstance(result, list)
    assert len(result) == 2
    for item in result:
        assert item == {
            "title": "Item 1",
            "size": 100,
            "description": None,
            "sub": {"name": "Sub1"},
            "multi": [],
        }
        # Verify secret fields are filtered out
        assert "secret_data" not in item
        assert "internal_id" not in item


def test_list_to_list_filter_no_data():
    response = client.post(
        "/item-list-to-list-filter",
        json=[],
    )
    assert response.status_code == 200, response.text
    assert response.json() == []


def test_list_validation_error():
    response = client.post(
        "/item-list",
        json=[
            {"title": "Valid Item", "size": 100, "sub": {"name": "Sub1"}},
            {
                "title": "Invalid Item"
                # Missing required fields: size and sub
            },
        ],
    )
    assert response.status_code == 422, response.text
    error_detail = response.json()["detail"]
    assert len(error_detail) == 2
    assert {
        "loc": ["body", 1, "size"],
        "msg": "field required",
        "type": "value_error.missing",
    } in error_detail
    assert {
        "loc": ["body", 1, "sub"],
        "msg": "field required",
        "type": "value_error.missing",
    } in error_detail


def test_list_nested_validation_error():
    response = client.post(
        "/item-list",
        json=[
            {"title": "Item with bad sub", "size": 100, "sub": {"wrong_field": "value"}}
        ],
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", 0, "sub", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


def test_list_type_validation_error():
    response = client.post(
        "/item-list",
        json=[{"title": "Item", "size": "not_a_number", "sub": {"name": "Sub"}}],
    )
    assert response.status_code == 422, response.text
    assert response.json() == snapshot(
        {
            "detail": [
                {
                    "loc": ["body", 0, "size"],
                    "msg": "value is not a valid integer",
                    "type": "type_error.integer",
                }
            ]
        }
    )


def test_invalid_list_structure():
    response = client.post(
        "/item-list",
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/item": {
                    "post": {
                        "summary": "Handle Item",
                        "operationId": "handle_item_item_post",
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
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle Item Item Post",
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
                "/item-filter": {
                    "post": {
                        "summary": "Handle Item Filter",
                        "operationId": "handle_item_filter_item_filter_post",
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
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle Item Filter Item Filter Post",
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
                "/item-list": {
                    "post": {
                        "summary": "Handle Item List",
                        "operationId": "handle_item_list_item_list_post",
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
                "/item-list-filter": {
                    "post": {
                        "summary": "Handle Item List Filter",
                        "operationId": "handle_item_list_filter_item_list_filter_post",
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
                "/item-list-to-list": {
                    "post": {
                        "summary": "Handle Item List To List",
                        "operationId": "handle_item_list_to_list_item_list_to_list_post",
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
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle Item List To List Item List To List Post",
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
                "/item-list-to-list-filter": {
                    "post": {
                        "summary": "Handle Item List To List Filter",
                        "operationId": "handle_item_list_to_list_filter_item_list_to_list_filter_post",
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
                                                "$ref": "#/components/schemas/Item"
                                            },
                                            "type": "array",
                                            "title": "Response Handle Item List To List Filter Item List To List Filter Post",
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
