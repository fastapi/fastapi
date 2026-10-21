from typing import Annotated, Literal

import pytest
from dirty_equals import IsOneOf
from fastapi import Body, Cookie, FastAPI, File, Form, Header, Path, Query, UploadFile
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, Field


@pytest.mark.parametrize("parameter", [Path, Query, Header, Cookie, Body, Form])
@pytest.mark.parametrize(
    "metadata",
    [Field(alias="wire"), Field(alias="unused", validation_alias="wire")],
)
def test_field_alias_is_preserved(parameter, metadata):
    app = FastAPI()
    field = Body(embed=True) if parameter is Body else parameter()

    @app.post("/{wire}" if parameter is Path else "/")
    def read_value(value: Annotated[int, metadata, field]):
        return value

    client = TestClient(app)
    if parameter is Path:
        response = client.post("/5")
    elif parameter is Query:
        response = client.post("/", params={"wire": "5"})
    elif parameter is Header:
        response = client.post("/", headers={"wire": "5"})
    elif parameter is Cookie:
        response = client.post("/", headers={"cookie": "wire=5"})
    elif parameter is Body:
        response = client.post("/", json={"wire": 5})
    else:
        response = client.post("/", data={"wire": "5"})
    assert response.status_code == 200
    assert response.json() == 5


def test_file_field_alias_is_preserved():
    app = FastAPI()

    @app.post("/")
    def read_file(value: Annotated[bytes, Field(alias="upload"), File()]):
        return value

    client = TestClient(app)
    response = client.post("/", files={"upload": ("example.txt", b"hello")})
    assert response.status_code == 200
    assert response.json() == "hello"


def test_inferred_body_aliases_are_preserved():
    app = FastAPI()

    @app.post("/")
    def read_values(
        first: Annotated[list[int], Field(alias="numbers")],
        second: Annotated[
            list[int], Field(alias="unused", validation_alias="more_numbers")
        ],
    ):
        return {"first": first, "second": second}

    client = TestClient(app)
    response = client.post("/", json={"numbers": [1], "more_numbers": [2]})
    assert response.status_code == 200
    assert response.json() == {"first": [1], "second": [2]}


def test_inferred_file_alias_is_preserved():
    app = FastAPI()

    @app.post("/")
    async def read_file(value: Annotated[UploadFile, Field(alias="upload")]):
        return await value.read()

    client = TestClient(app)
    response = client.post("/", files={"upload": ("example.txt", b"hello")})
    assert response.status_code == 200
    assert response.json() == "hello"


def test_field_discriminator_is_preserved():
    class Cat(BaseModel):
        kind: Literal["cat"]

    class Dog(BaseModel):
        kind: Literal["dog"]

    Pet = Annotated[Cat | Dog, Field(discriminator="kind")]
    app = FastAPI()

    @app.post("/")
    def read_pet(pet: Annotated[Pet, Body()]):
        return pet

    client = TestClient(app)
    response = client.post("/", json={"kind": "cat"})
    assert response.status_code == 200
    assert response.json() == {"kind": "cat"}

    response = client.post("/", json={"kind": "unknown"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "union_tag_invalid",
                "loc": ["body"],
                "msg": "Input tag 'unknown' found using 'kind' does not match any of the expected tags: 'cat', 'dog'",
                "input": {"kind": "unknown"},
                "ctx": {
                    "discriminator": "'kind'",
                    "tag": "unknown",
                    "expected_tags": "'cat', 'dog'",
                },
            }
        ]
    }


Count = Annotated[
    int,
    Field(
        alias="original",
        title="Original",
        description="From Field",
        examples=[1],
        deprecated=True,
        json_schema_extra={"x-source": "field", "x-retained": True},
    ),
]
app = FastAPI()


@app.get("/query")
def read_query(
    preserved: Annotated[Count, Query()],
    replaced: Annotated[
        Count,
        Query(
            alias="replacement",
            title="Replacement",
            description="From Query",
            examples=[2],
            deprecated=False,
            json_schema_extra={"x-source": "query"},
        ),
    ],
    cleared: Annotated[
        Count,
        Query(
            alias=None,
            title=None,
            description=None,
            examples=None,
            deprecated=None,
            json_schema_extra=None,
        ),
    ],
):
    return {"preserved": preserved, "replaced": replaced, "cleared": cleared}


@app.post("/body")
def read_body(
    preserved: Annotated[Count, Body()],
    replaced: Annotated[
        Count,
        Body(
            alias="replacement",
            title="Replacement",
            description="From Body",
            examples=[2],
            deprecated=False,
            json_schema_extra={"x-source": "body"},
        ),
    ],
    cleared: Annotated[
        Count,
        Body(
            alias=None,
            title=None,
            description=None,
            examples=None,
            deprecated=None,
            json_schema_extra=None,
        ),
    ],
):
    return {"preserved": preserved, "replaced": replaced, "cleared": cleared}


@app.get("/inferred")
@app.get("/inferred/{item_id}")
def read_inferred(
    item_id: Annotated[
        int,
        Field(
            default_factory=lambda: 5, title="Item ID", description="The item to read"
        ),
    ],
    count: Annotated[
        int, Field(alias="n", title="Count", description="Number of items")
    ] = 10,
):
    return {"item_id": item_id, "count": count}


client = TestClient(app)


def test_query_alias_overrides():
    response = client.get(
        "/query", params={"original": "1", "replacement": "2", "cleared": "3"}
    )
    assert response.status_code == 200
    assert response.json() == {"preserved": 1, "replaced": 2, "cleared": 3}


def test_body_alias_overrides():
    response = client.post(
        "/body", json={"original": 1, "replacement": 2, "cleared": 3}
    )
    assert response.status_code == 200
    assert response.json() == {"preserved": 1, "replaced": 2, "cleared": 3}


def test_inferred_query_alias_is_preserved():
    response = client.get("/inferred/1", params={"n": "2"})
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "count": 2}

    response = client.get("/inferred/1")
    assert response.status_code == 200
    assert response.json() == {"item_id": 1, "count": 10}

    response = client.get("/inferred")
    assert response.status_code == 200
    assert response.json() == {"item_id": 5, "count": 10}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/query": {
                    "get": {
                        "summary": "Read Query",
                        "operationId": "read_query_query_get",
                        "parameters": [
                            {
                                "name": "original",
                                "in": "query",
                                "required": True,
                                "schema": IsOneOf(
                                    {
                                        "type": "integer",
                                        "title": "Original",
                                        "description": "From Field",
                                        "deprecated": True,
                                        "examples": [1],
                                        "x-source": "field",
                                        "x-retained": True,
                                    },
                                    # Pydantic < 2.10 omits deprecated in this schema.
                                    {
                                        "type": "integer",
                                        "title": "Original",
                                        "description": "From Field",
                                        "examples": [1],
                                        "x-source": "field",
                                        "x-retained": True,
                                    },
                                ),
                                "description": "From Field",
                                "deprecated": True,
                            },
                            {
                                "name": "replacement",
                                "in": "query",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "title": "Replacement",
                                    "description": "From Query",
                                    "examples": [2],
                                    "x-source": "query",
                                    "x-retained": True,
                                },
                                "description": "From Query",
                            },
                            {
                                "name": "cleared",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "integer", "title": "Cleared"},
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
                },
                "/body": {
                    "post": {
                        "summary": "Read Body",
                        "operationId": "read_body_body_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_body_body_post"
                                    }
                                }
                            },
                            "required": True,
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
                },
                "/inferred/{item_id}": {
                    "get": {
                        "summary": "Read Inferred",
                        "operationId": "read_inferred_inferred__item_id__get",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "path",
                                "required": True,
                                "schema": {
                                    "type": "integer",
                                    "title": "Item ID",
                                    "description": "The item to read",
                                },
                                "description": "The item to read",
                            },
                            {
                                "name": "n",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "title": "Count",
                                    "description": "Number of items",
                                    "default": 10,
                                },
                                "description": "Number of items",
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
                },
                "/inferred": {
                    "get": {
                        "summary": "Read Inferred",
                        "operationId": "read_inferred_inferred_get",
                        "parameters": [
                            {
                                "name": "item_id",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "title": "Item ID",
                                    "description": "The item to read",
                                },
                                "description": "The item to read",
                            },
                            {
                                "name": "n",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "title": "Count",
                                    "description": "Number of items",
                                    "default": 10,
                                },
                                "description": "Number of items",
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
                },
            },
            "components": {
                "schemas": {
                    "Body_read_body_body_post": {
                        "properties": {
                            "original": {
                                "type": "integer",
                                "title": "Original",
                                "description": "From Field",
                                "deprecated": True,
                                "examples": [1],
                                "x-retained": True,
                                "x-source": "field",
                            },
                            "replacement": {
                                "type": "integer",
                                "title": "Replacement",
                                "description": "From Body",
                                "examples": [2],
                                "x-retained": True,
                                "x-source": "body",
                            },
                            "cleared": {"type": "integer", "title": "Cleared"},
                        },
                        "type": "object",
                        "required": ["original", "replacement", "cleared"],
                        "title": "Body_read_body_body_post",
                    },
                    "HTTPValidationError": {
                        "properties": {
                            "detail": {
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
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
                            "input": {"title": "Input"},
                            "ctx": {"type": "object", "title": "Context"},
                        },
                        "type": "object",
                        "required": ["loc", "msg", "type"],
                        "title": "ValidationError",
                    },
                }
            },
        }
    )
