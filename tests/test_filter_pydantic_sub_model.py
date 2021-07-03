from typing import Optional

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, ValidationError, validator

app = FastAPI()


class ModelB(BaseModel):
    username: str


class ModelC(ModelB):
    password: str


class ModelA(BaseModel):
    name: str
    description: Optional[str] = None
    model_b: ModelB

    @validator("name")
    def lower_username(cls, name: str, values):
        if not name.endswith("A"):
            raise ValueError("name must end in A")
        return name


async def get_model_c() -> ModelC:
    return ModelC(username="test-user", password="test-password")


@app.get("/model/{name}", response_model=ModelA)
async def get_model_a(name: str, model_c=Depends(get_model_c)):
    return {"name": name, "description": "model-a-desc", "model_b": model_c}


client = TestClient(app)


openapi_schema = {
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
                "required": ["name", "model_b"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "description": {"title": "Description", "type": "string"},
                    "model_b": {"$ref": "#/components/schemas/ModelB"},
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
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_filter_sub_model():
    response = client.get("/model/modelA")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "modelA",
        "description": "model-a-desc",
        "model_b": {"username": "test-user"},
    }


def test_validator_is_cloned():
    with pytest.raises(ValidationError) as err:
        client.get("/model/modelX")
    assert err.value.errors() == [
        {
            "loc": ("response", "name"),
            "msg": "name must end in A",
            "type": "value_error",
        }
    ]
