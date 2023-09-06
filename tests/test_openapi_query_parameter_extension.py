from typing import Optional

from dirty_equals import IsDict
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get(
    "/",
    openapi_extra={
        "parameters": [
            {
                "required": False,
                "schema": {"title": "Extra Param 1"},
                "name": "extra_param_1",
                "in": "query",
            },
            {
                "required": True,
                "schema": {"title": "Extra Param 2"},
                "name": "extra_param_2",
                "in": "query",
            },
        ]
    },
)
def route_with_extra_query_parameters(standard_query_param: Optional[int] = 50):
    return {}


client = TestClient(app)


def test_get_route():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {}


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "get": {
                    "summary": "Route With Extra Query Parameters",
                    "operationId": "route_with_extra_query_parameters__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": IsDict(
                                {
                                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                                    "default": 50,
                                    "title": "Standard Query Param",
                                }
                            )
                            | IsDict(
                                # TODO: remove when deprecating Pydantic v1
                                {
                                    "title": "Standard Query Param",
                                    "type": "integer",
                                    "default": 50,
                                }
                            ),
                            "name": "standard_query_param",
                            "in": "query",
                        },
                        {
                            "required": False,
                            "schema": {"title": "Extra Param 1"},
                            "name": "extra_param_1",
                            "in": "query",
                        },
                        {
                            "required": True,
                            "schema": {"title": "Extra Param 2"},
                            "name": "extra_param_2",
                            "in": "query",
                        },
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
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
