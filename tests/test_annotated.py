import pytest
from dirty_equals import IsDict
from fastapi import APIRouter, FastAPI, Query
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url
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

foo_is_missing = {
    "detail": [
        IsDict(
            {
                "loc": ["query", "foo"],
                "msg": "Field required",
                "type": "missing",
                "input": None,
                "url": match_pydantic_error_url("missing"),
            }
        )
        # TODO: remove when deprecating Pydantic v1
        | IsDict(
            {
                "loc": ["query", "foo"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        )
    ]
}
foo_is_short = {
    "detail": [
        IsDict(
            {
                "ctx": {"min_length": 1},
                "loc": ["query", "foo"],
                "msg": "String should have at least 1 characters",
                "type": "string_too_short",
                "input": "",
                "url": match_pydantic_error_url("string_too_short"),
            }
        )
        # TODO: remove when deprecating Pydantic v1
        | IsDict(
            {
                "ctx": {"limit_value": 1},
                "loc": ["query", "foo"],
                "msg": "ensure this value has at least 1 characters",
                "type": "value_error.any_str.min_length",
            }
        )
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
    ],
)
def test_get(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_multiple_path():
    app = FastAPI()

    @app.get("/test1")
    @app.get("/test2")
    async def test(var: Annotated[str, Query()] = "bar"):
        return {"foo": var}

    client = TestClient(app)
    response = client.get("/test1")
    assert response.status_code == 200
    assert response.json() == {"foo": "bar"}

    response = client.get("/test1", params={"var": "baz"})
    assert response.status_code == 200
    assert response.json() == {"foo": "baz"}

    response = client.get("/test2")
    assert response.status_code == 200
    assert response.json() == {"foo": "bar"}

    response = client.get("/test2", params={"var": "baz"})
    assert response.status_code == 200
    assert response.json() == {"foo": "baz"}


def test_nested_router():
    app = FastAPI()

    router = APIRouter(prefix="/nested")

    @router.get("/test")
    async def test(var: Annotated[str, Query()] = "bar"):
        return {"foo": var}

    app.include_router(router)

    client = TestClient(app)

    response = client.get("/nested/test")
    assert response.status_code == 200
    assert response.json() == {"foo": "bar"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/default": {
                "get": {
                    "summary": "Default",
                    "operationId": "default_default_get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Foo",
                                "type": "string",
                                "default": "foo",
                            },
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
                            "schema": {
                                "title": "Foo",
                                "minLength": 1,
                                "type": "string",
                            },
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
                            "schema": {
                                "title": "Foo",
                                "minLength": 1,
                                "type": "string",
                            },
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
