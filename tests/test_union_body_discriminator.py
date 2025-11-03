from typing import Any, Dict, Union

from dirty_equals import IsDict
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field
from typing_extensions import Annotated, Literal

from .utils import needs_pydanticv2


@needs_pydanticv2
def test_discriminator_pydantic_v2() -> None:
    from pydantic import Tag

    app = FastAPI()

    class FirstItem(BaseModel):
        value: Literal["first"]
        price: int

    class OtherItem(BaseModel):
        value: Literal["other"]
        price: float

    Item = Annotated[
        Union[Annotated[FirstItem, Tag("first")], Annotated[OtherItem, Tag("other")]],
        Field(discriminator="value"),
    ]

    @app.post("/items/")
    def save_union_body_discriminator(
        item: Item, q: Annotated[str, Field(description="Query string")]
    ) -> Dict[str, Any]:
        return {"item": item}

    client = TestClient(app)
    response = client.post("/items/?q=first", json={"value": "first", "price": 100})
    assert response.status_code == 200, response.text
    assert response.json() == {"item": {"value": "first", "price": 100}}

    response = client.post("/items/?q=other", json={"value": "other", "price": 100.5})
    assert response.status_code == 200, response.text
    assert response.json() == {"item": {"value": "other", "price": 100.5}}

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "post": {
                        "summary": "Save Union Body Discriminator",
                        "operationId": "save_union_body_discriminator_items__post",
                        "parameters": [
                            {
                                "name": "q",
                                "in": "query",
                                "required": True,
                                "schema": {
                                    "type": "string",
                                    "description": "Query string",
                                    "title": "Q",
                                },
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "oneOf": [
                                            {"$ref": "#/components/schemas/FirstItem"},
                                            {"$ref": "#/components/schemas/OtherItem"},
                                        ],
                                        "discriminator": {
                                            "propertyName": "value",
                                            "mapping": {
                                                "first": "#/components/schemas/FirstItem",
                                                "other": "#/components/schemas/OtherItem",
                                            },
                                        },
                                        "title": "Item",
                                    }
                                }
                            },
                        },
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": IsDict(
                                            {
                                                # Pydantic 2.10, in Python 3.8
                                                # TODO: remove when dropping support for Python 3.8
                                                "type": "object",
                                                "title": "Response Save Union Body Discriminator Items  Post",
                                            }
                                        )
                                        | IsDict(
                                            {
                                                "type": "object",
                                                "additionalProperties": True,
                                                "title": "Response Save Union Body Discriminator Items  Post",
                                            }
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
                }
            },
            "components": {
                "schemas": {
                    "FirstItem": {
                        "properties": {
                            "value": {
                                "type": "string",
                                "const": "first",
                                "title": "Value",
                            },
                            "price": {"type": "integer", "title": "Price"},
                        },
                        "type": "object",
                        "required": ["value", "price"],
                        "title": "FirstItem",
                    },
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
                    "OtherItem": {
                        "properties": {
                            "value": {
                                "type": "string",
                                "const": "other",
                                "title": "Value",
                            },
                            "price": {"type": "number", "title": "Price"},
                        },
                        "type": "object",
                        "required": ["value", "price"],
                        "title": "OtherItem",
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
