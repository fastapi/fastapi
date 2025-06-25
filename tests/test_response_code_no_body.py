import typing

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class JsonApiResponse(JSONResponse):
    media_type = "application/vnd.api+json"


class Error(BaseModel):
    status: str
    title: str


class JsonApiError(BaseModel):
    errors: typing.List[Error]


@app.get(
    "/a",
    status_code=204,
    response_class=JsonApiResponse,
    responses={500: {"description": "Error", "model": JsonApiError}},
)
async def a():
    pass


@app.get("/b", responses={204: {"description": "No Content"}})
async def b():
    pass  # pragma: no cover


client = TestClient(app)


def test_get_response():
    response = client.get("/a")
    assert response.status_code == 204, response.text
    assert "content-length" not in response.headers
    assert response.content == b""


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/a": {
                "get": {
                    "responses": {
                        "500": {
                            "description": "Error",
                            "content": {
                                "application/vnd.api+json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/JsonApiError"
                                    }
                                }
                            },
                        },
                        "204": {"description": "Successful Response"},
                    },
                    "summary": "A",
                    "operationId": "a_a_get",
                }
            },
            "/b": {
                "get": {
                    "responses": {
                        "204": {"description": "No Content"},
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                    },
                    "summary": "B",
                    "operationId": "b_b_get",
                }
            },
        },
        "components": {
            "schemas": {
                "Error": {
                    "title": "Error",
                    "required": ["status", "title"],
                    "type": "object",
                    "properties": {
                        "status": {"title": "Status", "type": "string"},
                        "title": {"title": "Title", "type": "string"},
                    },
                },
                "JsonApiError": {
                    "title": "JsonApiError",
                    "required": ["errors"],
                    "type": "object",
                    "properties": {
                        "errors": {
                            "title": "Errors",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Error"},
                        }
                    },
                },
            }
        },
    }
