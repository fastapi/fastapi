from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, ConfigDict, Field


@pytest.fixture(name="client")
def get_client():
    app = FastAPI()

    class ModelWithRef(BaseModel):
        ref: str = Field(validation_alias="$ref", serialization_alias="$ref")
        model_config = ConfigDict(validate_by_alias=True, serialize_by_alias=True)

    @app.get("/", response_model=ModelWithRef)
    async def read_root() -> Any:
        return {"$ref": "some-ref"}

    client = TestClient(app)
    return client


def test_get(client: TestClient):
    response = client.get("/")
    assert response.json() == {"$ref": "some-ref"}


def test_openapi_schema(client: TestClient):
    response = client.get("openapi.json")
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "summary": "Read Root",
                        "operationId": "read_root__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ModelWithRef"
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
                    "ModelWithRef": {
                        "properties": {"$ref": {"type": "string", "title": "$Ref"}},
                        "type": "object",
                        "required": ["$ref"],
                        "title": "ModelWithRef",
                    }
                }
            },
        }
    )
