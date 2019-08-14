import typing

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

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
    response_class=JsonApiResponse,
    responses={500: {"description": "Error", "model": JsonApiError}},
)
async def a():
    pass  # pragma: no cover


@app.get("/b", responses={500: {"description": "Error", "model": Error}})
async def b():
    pass  # pragma: no cover


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/a": {
            "get": {
                "responses": {
                    "500": {
                        "description": "Error",
                        "content": {
                            "application/vnd.api+json": {
                                "schema": {"$ref": "#/components/schemas/JsonApiError"}
                            }
                        },
                    },
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/vnd.api+json": {"schema": {}}},
                    },
                },
                "summary": "A",
                "operationId": "a_a_get",
            }
        },
        "/b": {
            "get": {
                "responses": {
                    "500": {
                        "description": "Error",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Error"}
                            }
                        },
                    },
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


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema
