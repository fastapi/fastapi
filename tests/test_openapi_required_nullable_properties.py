from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class RequiredNullableFieldModel(BaseModel):
    required: str = Field(...)
    optional: Optional[str] = Field(None)
    required_nullable: Optional[str] = Field(...)


@app.get("/", response_model=RequiredNullableFieldModel)
def route() -> RequiredNullableFieldModel:
    return RequiredNullableFieldModel(required="", required_nullable=None)


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/RequiredNullableFieldModel"
                                }
                            }
                        },
                    },
                },
                "summary": "Route",
                "operationId": "route__get",
            }
        },
    },
    "components": {
        "schemas": {
            "RequiredNullableFieldModel": {
                "properties": {
                    "optional": {
                        "title": "Optional",
                        "type": "string",
                    },
                    "required": {
                        "title": "Required",
                        "type": "string",
                    },
                    "required_nullable": {
                        "nullable": True,
                        "title": "Required Nullable",
                        "type": "string",
                    },
                },
                "required": ["required", "required_nullable"],
                "title": "RequiredNullableFieldModel",
                "type": "object",
            },
        }
    },
}


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_get_route():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == RequiredNullableFieldModel(
        required="", required_nullable=None
    )
