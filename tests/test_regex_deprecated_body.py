import pytest
from dirty_equals import IsDict
from fastapi import FastAPI, Form
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url
from typing_extensions import Annotated

from .utils import needs_py310


def get_client():
    app = FastAPI()
    with pytest.warns(DeprecationWarning):

        @app.post("/items/")
        async def read_items(
            q: Annotated[str | None, Form(regex="^fixedquery$")] = None
        ):
            if q:
                return f"Hello {q}"
            else:
                return "Hello World"

    client = TestClient(app)
    return client


@needs_py310
def test_no_query():
    client = get_client()
    response = client.post("/items/")
    assert response.status_code == 200
    assert response.json() == "Hello World"


@needs_py310
def test_q_fixedquery():
    client = get_client()
    response = client.post("/items/", data={"q": "fixedquery"})
    assert response.status_code == 200
    assert response.json() == "Hello fixedquery"


@needs_py310
def test_query_nonregexquery():
    client = get_client()
    response = client.post("/items/", data={"q": "nonregexquery"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "string_pattern_mismatch",
                    "loc": ["body", "q"],
                    "msg": "String should match pattern '^fixedquery$'",
                    "input": "nonregexquery",
                    "ctx": {"pattern": "^fixedquery$"},
                    "url": match_pydantic_error_url("string_pattern_mismatch"),
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "ctx": {"pattern": "^fixedquery$"},
                    "loc": ["body", "q"],
                    "msg": 'string does not match regex "^fixedquery$"',
                    "type": "value_error.str.regex",
                }
            ]
        }
    )


@needs_py310
def test_openapi_schema():
    client = get_client()
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    # insert_assert(response.json())
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
                    "summary": "Read Items",
                    "operationId": "read_items_items__post",
                    "requestBody": {
                        "content": {
                            "application/x-www-form-urlencoded": {
                                "schema": IsDict(
                                    {
                                        "allOf": [
                                            {
                                                "$ref": "#/components/schemas/Body_read_items_items__post"
                                            }
                                        ],
                                        "title": "Body",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {
                                        "$ref": "#/components/schemas/Body_read_items_items__post"
                                    }
                                )
                            }
                        }
                    },
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
                "Body_read_items_items__post": {
                    "properties": {
                        "q": IsDict(
                            {
                                "anyOf": [
                                    {"type": "string", "pattern": "^fixedquery$"},
                                    {"type": "null"},
                                ],
                                "title": "Q",
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"type": "string", "pattern": "^fixedquery$", "title": "Q"}
                        )
                    },
                    "type": "object",
                    "title": "Body_read_items_items__post",
                },
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            }
        },
    }
