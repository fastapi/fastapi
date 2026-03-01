from typing import Annotated, Literal, Union

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(name="client")
def get_client():
    from pydantic import BaseModel, Field, RootModel

    class Base(BaseModel):
        type: Literal["BASE"] = "BASE"
        value: str

    class MyModel(RootModel[Annotated[Union[Base], Field(discriminator="type")]]):
        pass

    app = FastAPI()

    @app.get("/")
    def test() -> MyModel:
        return MyModel.model_validate(Base(value="test"))

    client = TestClient(app)
    return client


def test_get(client: TestClient):
    response = client.get("/")
    assert response.json() == {"value": "test", "type": "BASE"}


def test_openapi_schema(client: TestClient):
    response = client.get("openapi.json")
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "summary": "Test",
                        "operationId": "test__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/MyModel"
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "Base": {
                        "properties": {
                            "type": {
                                "type": "string",
                                "const": "BASE",
                                "title": "Type",
                                "default": "BASE",
                            },
                            "value": {"type": "string", "title": "Value"},
                        },
                        "type": "object",
                        "required": ["value"],
                        "title": "Base",
                    },
                    "MyModel": {
                        "oneOf": [{"$ref": "#/components/schemas/Base"}],
                        "title": "MyModel",
                        "discriminator": {
                            "propertyName": "type",
                            "mapping": {"BASE": "#/components/schemas/Base"},
                        },
                    },
                }
            },
        }
    )
