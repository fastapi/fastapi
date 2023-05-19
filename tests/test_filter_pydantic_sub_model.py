from typing import Optional

import pytest
from dirty_equals import IsDict, IsStr
from fastapi import Depends, FastAPI
from fastapi.exceptions import ResponseValidationError
from fastapi.testclient import TestClient
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


def test_filter_sub_model():
    response = client.get("/model/modelA")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "modelA",
        "description": "model-a-desc",
        "foo": {"username": "test-user"},
    }


def test_validator_is_cloned():
    with pytest.raises(ResponseValidationError) as err:
        client.get("/model/modelX")
    assert err.value.pydantic_validation_error.errors() == [
        IsDict(
            {
                "type": "value_error",
                "loc": ("name",),
                "msg": "Value error, name must end in A",
                "input": "modelX",
                "ctx": {"error": "name must end in A"},
                "url": IsStr(regex=r"^https://errors\.pydantic\.dev/.*/v/value_error$"),
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.0.2",
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
