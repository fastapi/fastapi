from typing import Optional

from fastapi import Depends, FastAPI, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name_required_with_default: str = Query(
        "name default", description="This is a name_required_with_default field."
    )
    name_required_without_default: str = Query(
        None, description="This is a name_required_without_default field."
    )
    optional_int: Optional[int] = Query(
        None, description="This is a optional_int field"
    )
    optional_str: Optional[str] = Query(
        "default_exists", description="This is a optional_str field"
    )
    model: str
    manufacturer: str
    price: float
    tax: float


@app.get("/item")
async def item_with_query_dependency(item: Item = Depends()):
    return item


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
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
                            "title": "Name Required With Default",
                            "type": "string",
                            "description": "This is a name_required_with_default field.",
                            "default": "name default",
                            "extra": {},
                        },
                        "name": "name_required_with_default",
                        "in": "query",
                    },
                    {
                        "description": "This is a name_required_without_default field.",
                        "required": False,
                        "schema": {
                            "title": "Name Required Without Default",
                            "type": "string",
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
                            "title": "Optional Int",
                            "type": "integer",
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
                            "title": "Optional Str",
                            "type": "string",
                            "description": "This is a optional_str field",
                            "default": "default_exists",
                            "extra": {},
                        },
                        "name": "optional_str",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Model", "type": "string", "extra": {}},
                        "name": "model",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {
                            "title": "Manufacturer",
                            "type": "string",
                            "extra": {},
                        },
                        "name": "manufacturer",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Price", "type": "number", "extra": {}},
                        "name": "price",
                        "in": "query",
                    },
                    {
                        "required": True,
                        "schema": {"title": "Tax", "type": "number", "extra": {}},
                        "name": "tax",
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
                "title": "HTTPValidationError",
                "type": "object",
                "properties": {
                    "detail": {
                        "title": "Detail",
                        "type": "array",
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                    }
                },
            },
            "ValidationError": {
                "title": "ValidationError",
                "required": ["loc", "msg", "type"],
                "type": "object",
                "properties": {
                    "loc": {
                        "title": "Location",
                        "type": "array",
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi_schema_with_query_dependency():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema
