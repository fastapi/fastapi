from typing import Optional

import pytest
from dirty_equals import IsDict
from fastapi import Depends, FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url

from .utils import needs_pydanticv2


@pytest.fixture(name="client")
def get_client():
    from pydantic import BaseModel, FieldValidationInfo, field_validator

    app = FastAPI()

    class ModelB(BaseModel):
        username: str

    class ModelC(ModelB):
        password: str

    class ModelA(BaseModel):
        name: str
        description: Optional[str] = None
        foo: ModelB

        @field_validator("name")
        def lower_username(cls, name: str, info: FieldValidationInfo):
            if not name.endswith("A"):
                raise ValueError("name must end in A")
            return name

    async def get_model_c() -> ModelC:
        return ModelC(username="test-user", password="test-password")

    @app.get("/model/{name}", response_model=ModelA)
    async def get_model_a(name: str, model_c=Depends(get_model_c)):
        return {"name": name, "description": "model-a-desc", "foo": model_c}

    client = TestClient(app)
    return client


@needs_pydanticv2
def test_filter_sub_model(client: TestClient):
    response = client.get("/model/modelA")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "modelA",
        "description": "model-a-desc",
        "foo": {"username": "test-user"},
    }


@needs_pydanticv2
def test_validator_is_cloned(client: TestClient):
    with pytest.raises(ResponseValidationError) as err:
        client.get("/model/modelX")
    assert err.value.errors() == [
        IsDict(
            {
                "type": "value_error",
                "loc": ("response", "name"),
                "msg": "Value error, name must end in A",
                "input": "modelX",
                "ctx": {"error": "name must end in A"},
                "url": match_pydantic_error_url("value_error"),
            }
        )
        | IsDict(
            # TODO remove when deprecating Pydantic v1
            {
                "loc": ("response", "name"),
                "msg": "name must end in A",
                "type": "value_error",
            }
        )
    ]


@needs_pydanticv2
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
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
                                    "schema": {"$ref": "#/components/schemas/ModelA"}
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
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
                "ModelA": {
                    "title": "ModelA",
                    "required": ["name", "foo"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "description": IsDict(
                            {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        |
                        # TODO remove when deprecating Pydantic v1
                        IsDict({"title": "Description", "type": "string"}),
                        "foo": {"$ref": "#/components/schemas/ModelB"},
                    },
                },
                "ModelB": {
                    "title": "ModelB",
                    "required": ["username"],
                    "type": "object",
                    "properties": {"username": {"title": "Username", "type": "string"}},
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
