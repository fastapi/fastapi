from typing import Optional

from fastapi import Depends, FastAPI, Query, status
from fastapi.testclient import TestClient
from pydantic import BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

app = FastAPI()


class Item(BaseModel):
    name_required_with_default: str = Query(
        "name default", description="This is a name_required_with_default field."
    )
    name_required_without_default: str = Query(
        description="This is a name_required_without_default field."
    )
    optional_int: Optional[int] = Query(
        default=None, description="This is a optional_int field"
    )
    optional_str: Optional[str] = Query(
        "default_exists", description="This is a optional_str field"
    )
    model: str
    manufacturer: str
    price: float
    tax: float
    extra_optional_attributes: str = Query(
        None,
        description="This is a extra_optional_attributes field",
        alias="extra_optional_attributes_alias",
        max_length=30,
    )


@app.get("/item")
async def item_with_query_dependency(item: Item = Depends()):
    return item


client = TestClient(app)

openapi_schema_with_not_omitted_description_pydantic_v1 = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/item": {
            "get": {
                "summary": "Item With Query Dependency",
                "operationId": "item_with_query_dependency_item_get",
                "parameters": [
                    {
                        "description": "This is a name_required_with_default field.",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": "Name Required With Default",
                            "description": "This is a name_required_with_default field.",
                            "default": "name default",
                            "extra": {},
                        },
                        "name": "name_required_with_default",
                        "in": "query",
                    },
                    {
                        "description": "This is a name_required_without_default field.",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "title": "Name Required Without Default",
                            "description": "This is a name_required_without_default field.",
                            "extra": {},
                        },
                        "name": "name_required_without_default",
                        "in": "query",
                    },
                    {
                        "description": "This is a optional_int field",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "title": "Optional Int",
                            "description": "This is a optional_int field",
                            "extra": {},
                        },
                        "name": "optional_int",
                        "in": "query",
                    },
                    {
                        "description": "This is a optional_str field",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "title": "Optional Str",
                            "description": "This is a optional_str field",
                            "default": "default_exists",
                            "extra": {},
                        },
                        "name": "optional_str",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"type": "string", "title": "Model", "extra": {}},
                        "name": "model",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {
                            "type": "string",
                            "title": "Manufacturer",
                            "extra": {},
                        },
                        "name": "manufacturer",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"type": "number", "title": "Price", "extra": {}},
                        "name": "price",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"type": "number", "title": "Tax", "extra": {}},
                        "name": "tax",
                        "in": "query",
                    },
                    {
                        "description": "This is a extra_optional_attributes field",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "maxLength": 30,
                            "title": "Extra Optional Attributes Alias",
                            "description": "This is a extra_optional_attributes field",
                            "extra": {},
                        },
                        "name": "extra_optional_attributes_alias",
                        "in": "query",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
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
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "type": "array",
                        "title": "Detail",
                    }
                },
                "type": "object",
                "title": "HTTPValidationError",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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

openapi_schema_with_not_omitted_description_pydantic_v2 = {
    "openapi": "3.1.0",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/item": {
            "get": {
                "summary": "Item With Query Dependency",
                "operationId": "item_with_query_dependency_item_get",
                "parameters": [
                    {
                        "name": "name_required_with_default",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "description": "This is a name_required_with_default field.",
                            "required": False,
                            "default": "name default",
                            "title": "Name Required With Default",
                        },
                        "description": "This is a name_required_with_default field.",
                    },
                    {
                        "name": "name_required_without_default",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "description": "This is a name_required_without_default field.",
                            "required": True,
                            "title": "Name Required Without Default",
                        },
                        "description": "This is a name_required_without_default field.",
                    },
                    {
                        "name": "optional_int",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "integer"}, {"type": "null"}],
                            "description": "This is a optional_int field",
                            "required": False,
                            "title": "Optional Int",
                        },
                        "description": "This is a optional_int field",
                    },
                    {
                        "name": "optional_str",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "anyOf": [{"type": "string"}, {"type": "null"}],
                            "description": "This is a optional_str field",
                            "required": False,
                            "default": "default_exists",
                            "title": "Optional Str",
                        },
                        "description": "This is a optional_str field",
                    },
                    {
                        "name": "model",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "required": True,
                            "title": "Model",
                        },
                    },
                    {
                        "name": "manufacturer",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "string",
                            "required": True,
                            "title": "Manufacturer",
                        },
                    },
                    {
                        "name": "price",
                        "in": "query",
                        "required": True,
                        "schema": {
                            "type": "number",
                            "required": True,
                            "title": "Price",
                        },
                    },
                    {
                        "name": "tax",
                        "in": "query",
                        "required": True,
                        "schema": {"type": "number", "required": True, "title": "Tax"},
                    },
                    {
                        "name": "extra_optional_attributes_alias",
                        "in": "query",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "description": "This is a extra_optional_attributes field",
                            "required": False,
                            "metadata": [{"max_length": 30}],
                            "title": "Extra Optional Attributes Alias",
                        },
                        "description": "This is a extra_optional_attributes field",
                    },
                ],
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
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
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "type": "array",
                        "title": "Detail",
                    }
                },
                "type": "object",
                "title": "HTTPValidationError",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
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


def test_openapi_schema_with_query_dependency():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    if PYDANTIC_V2:
        assert (
            response.json() == openapi_schema_with_not_omitted_description_pydantic_v2
        )
    else:
        assert (
            response.json() == openapi_schema_with_not_omitted_description_pydantic_v1
        )


def test_response():
    expected_response = {
        "name_required_with_default": "name default",
        "name_required_without_default": "default",
        "optional_int": None,
        "optional_str": "default_exists",
        "model": "model",
        "manufacturer": "manufacturer",
        "price": 100.0,
        "tax": 9.0,
        "extra_optional_attributes": "alias_query",
    }
    if not PYDANTIC_V2:
        expected_response.pop("extra_optional_attributes")
        expected_response["extra_optional_attributes_alias"] = None
    response = client.get(
        "/item",
        params={
            "name_required_with_default": "name default",
            "name_required_without_default": "default",
            "optional_str": "default_exists",
            "model": "model",
            "manufacturer": "manufacturer",
            "price": 100,
            "tax": 9,
            "extra_optional_attributes_alias": "alias_query",
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response

    expected_response = {
        "name_required_with_default": "name default",
        "name_required_without_default": "default",
        "optional_int": None,
        "optional_str": "",
        "model": "model",
        "manufacturer": "manufacturer",
        "price": 100.0,
        "tax": 9.0,
        "extra_optional_attributes": "alias_query",
    }
    if not PYDANTIC_V2:
        expected_response.pop("extra_optional_attributes")
        expected_response["extra_optional_attributes_alias"] = None
    response = client.get(
        "/item",
        params={
            "name_required_with_default": "name default",
            "name_required_without_default": "default",
            "optional_str": None,
            "model": "model",
            "manufacturer": "manufacturer",
            "price": 100,
            "tax": 9,
            "extra_optional_attributes_alias": "alias_query",
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response

    expected_response = {
        "name_required_with_default": "name default",
        "name_required_without_default": "default",
        "optional_int": None,
        "optional_str": "default_exists",
        "model": "model",
        "manufacturer": "manufacturer",
        "price": 100.0,
        "tax": 9.0,
        "extra_optional_attributes": "alias_query",
    }
    if not PYDANTIC_V2:
        expected_response.pop("extra_optional_attributes")
        expected_response["extra_optional_attributes_alias"] = None
    response = client.get(
        "/item",
        params={
            "name_required_with_default": "name default",
            "name_required_without_default": "default",
            "model": "model",
            "manufacturer": "manufacturer",
            "price": 100,
            "tax": 9,
            "extra_optional_attributes_alias": "alias_query",
        },
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == expected_response
