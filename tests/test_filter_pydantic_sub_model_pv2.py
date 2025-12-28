from typing import Optional

import pytest
from dirty_equals import HasRepr
from fastapi import Depends, FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(name="client")
def get_client():
    from pydantic import BaseModel, ValidationInfo, field_validator

    app = FastAPI()

    class ModelB(BaseModel):
        username: str

    class ModelC(ModelB):
        password: str

    class ModelA(BaseModel):
        name: str
        description: Optional[str] = None
        foo: ModelB
        tags: dict[str, str] = {}

        @field_validator("name")
        def lower_username(cls, name: str, info: ValidationInfo):
            if not name.endswith("A"):
                raise ValueError("name must end in A")
            return name

    async def get_model_c() -> ModelC:
        return ModelC(username="test-user", password="test-password")

    @app.get("/model/{name}", response_model=ModelA)
    async def get_model_a(name: str, model_c=Depends(get_model_c)):
        return {
            "name": name,
            "description": "model-a-desc",
            "foo": model_c,
            "tags": {"key1": "value1", "key2": "value2"},
        }

    client = TestClient(app)
    return client


def test_filter_sub_model(client: TestClient):
    response = client.get("/model/modelA")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "modelA",
        "description": "model-a-desc",
        "foo": {"username": "test-user"},
        "tags": {"key1": "value1", "key2": "value2"},
    }


def test_validator_is_cloned(client: TestClient):
    with pytest.raises(ResponseValidationError) as err:
        client.get("/model/modelX")
    assert err.value.errors() == [
        {
            "type": "value_error",
            "loc": ("response", "name"),
            "msg": "Value error, name must end in A",
            "input": "modelX",
            "ctx": {"error": HasRepr("ValueError('name must end in A')")},
        }
    ]


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/model/{name}": {
                    "get": {
                        "summary": "Get Model A",
                        "operationId": "get_model_a_model__name__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Name", "type": "string"},
                                "name": "name",
                                "in": "path",
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ModelA"
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
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                    "ModelA": {
                        "title": "ModelA",
                        "required": ["name", "foo"],
                        "type": "object",
                        "properties": {
                            "name": {"title": "Name", "type": "string"},
                            "description": {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            },
                            "foo": {"$ref": "#/components/schemas/ModelB"},
                            "tags": {
                                "additionalProperties": {"type": "string"},
                                "type": "object",
                                "title": "Tags",
                                "default": {},
                            },
                        },
                    },
                    "ModelB": {
                        "title": "ModelB",
                        "required": ["username"],
                        "type": "object",
                        "properties": {
                            "username": {"title": "Username", "type": "string"}
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
                                "items": {
                                    "anyOf": [{"type": "string"}, {"type": "integer"}]
                                },
                            },
                            "msg": {"title": "Message", "type": "string"},
                            "type": {"title": "Error Type", "type": "string"},
                        },
                    },
                }
            },
        }
    )
