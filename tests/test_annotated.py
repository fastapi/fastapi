import pytest
from fastapi import FastAPI, Query
from fastapi.testclient import TestClient
from typing_extensions import Annotated

app = FastAPI()


@app.get("/default")
async def default(foo: Annotated[str, Query()] = "foo"):
    return {"foo": foo}


@app.get("/required")
async def required(foo: Annotated[str, Query(min_length=1)]):
    return {"foo": foo}


@app.get("/multiple")
async def multiple(foo: Annotated[str, object(), Query(min_length=1)]):
    return {"foo": foo}


@app.get("/unrelated")
async def unrelated(foo: Annotated[str, object()]):
    return {"foo": foo}


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/default": {
            "get": {
                "summary": "Default",
                "operationId": "default_default_get",
                "parameters": [
                    {
                        "required": False,
                        "schema": {"title": "Foo", "type": "string", "default": "foo"},
                        "name": "foo",
                        "in": "query",
                    }
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
        },
        "/required": {
            "get": {
                "summary": "Required",
                "operationId": "required_required_get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Foo", "minLength": 1, "type": "string"},
                        "name": "foo",
                        "in": "query",
                    }
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
        },
        "/multiple": {
            "get": {
                "summary": "Multiple",
                "operationId": "multiple_multiple_get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Foo", "minLength": 1, "type": "string"},
                        "name": "foo",
                        "in": "query",
                    }
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
        },
        "/unrelated": {
            "get": {
                "summary": "Unrelated",
                "operationId": "unrelated_unrelated_get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "Foo", "type": "string"},
                        "name": "foo",
                        "in": "query",
                    }
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
        },
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
                        "items": {"anyOf": [{"type": "string"}, {"type": "integer"}]},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}
foo_is_missing = {
    "detail": [
        {
            "loc": ["query", "foo"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}
foo_is_short = {
    "detail": [
        {
            "ctx": {"limit_value": 1},
            "loc": ["query", "foo"],
            "msg": "ensure this value has at least 1 characters",
            "type": "value_error.any_str.min_length",
        }
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/default", 200, {"foo": "foo"}),
        ("/default?foo=bar", 200, {"foo": "bar"}),
        ("/required?foo=bar", 200, {"foo": "bar"}),
        ("/required", 422, foo_is_missing),
        ("/required?foo=", 422, foo_is_short),
        ("/multiple?foo=bar", 200, {"foo": "bar"}),
        ("/multiple", 422, foo_is_missing),
        ("/multiple?foo=", 422, foo_is_short),
        ("/unrelated?foo=bar", 200, {"foo": "bar"}),
        ("/unrelated", 422, foo_is_missing),
        ("/openapi.json", 200, openapi_schema),
    ],
)
def test_get(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
