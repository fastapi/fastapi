from typing import Annotated

import pytest
from fastapi import FastAPI, Header, Query
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import AliasChoices, AliasPath, BaseModel, ConfigDict, Field

app = FastAPI()


@app.get("/individual")
def read_individual(
    value: Annotated[
        int, Query(alias="ignored", validation_alias=AliasChoices("first", "second"))
    ],
    items: Annotated[
        list[str],
        Query(validation_alias=AliasChoices("item", "tag"), title="Chosen items"),
    ] = ["default"],  # noqa: B006
):
    return {"value": value, "items": items}


class QueryModel(BaseModel):
    value: Annotated[
        int, Field(alias="ignored", validation_alias=AliasChoices("first", "second"))
    ]
    items: Annotated[
        list[str],
        Field(validation_alias=AliasChoices("item", "tag"), title="Chosen items"),
    ] = ["default"]


@app.get("/model")
def read_model(data: Annotated[QueryModel, Query()]):
    return {"value": data.value, "items": data.items}


# Reusing a model across sources must preserve its aliases and schema.
@app.get("/headers")
def read_headers(data: Annotated[QueryModel, Header()]):
    return data


client = TestClient(app)


@pytest.mark.parametrize("path", ["/individual", "/model"])
@pytest.mark.parametrize("alias", ["first", "second"])
def test_scalar_choices_and_list_default(path: str, alias: str):
    response = client.get(path, params={alias: "1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": ["default"]}


@pytest.mark.parametrize("path", ["/individual", "/model"])
@pytest.mark.parametrize("alias", ["item", "tag"])
@pytest.mark.parametrize("items", [["one"], ["one", "two"], [""]])
def test_list_choices_preserve_items(path: str, alias: str, items: list[str]):
    response = client.get(path, params={"first": "1", alias: items})
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": items}


@pytest.mark.parametrize("path", ["/individual", "/model"])
def test_repeated_scalar_uses_last_value(path: str):
    response = client.get(f"{path}?second=1&second=2")
    assert response.status_code == 200
    assert response.json() == {"value": 2, "items": ["default"]}


@pytest.mark.parametrize("path", ["/individual", "/model"])
def test_choices_follow_declaration_order(path: str):
    response = client.get(f"{path}?second=2&first=1&tag=ignored&item=one&item=two")
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": ["one", "two"]}


@pytest.mark.parametrize("path", ["/individual", "/model"])
@pytest.mark.parametrize(
    "params, alias, value",
    [
        ({"first": "invalid", "second": "2"}, "first", "invalid"),
        ({"first": "", "second": "2"}, "first", ""),
        ({"second": "invalid"}, "second", "invalid"),
    ],
)
def test_invalid_choice_uses_selected_alias(path, params, alias, value):
    response = client.get(path, params=params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["query", alias],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": value,
            }
        ]
    }


@pytest.mark.parametrize("params", [{}, {"value": "1"}, {"ignored": "1"}])
def test_individual_missing_uses_first_alias(params: dict[str, str]):
    response = client.get("/individual", params=params)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["query", "first"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }


def test_inferred_query_keeps_field_alias_choices():
    app = FastAPI()

    @app.get("/")
    def read(
        value: Annotated[int, Field(validation_alias=AliasChoices("first", "second"))],
    ):
        return value

    client = TestClient(app)
    response = client.get("/", params={"second": "1"})
    assert response.status_code == 200
    assert response.json() == 1


def test_model_preserves_unused_choices_for_extra_validation():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: Annotated[int, Field(validation_alias=AliasChoices("first", "second"))]

    @app.get("/")
    def read(data: Annotated[Model, Query()]):
        return data

    client = TestClient(app)
    response = client.get("/", params={"second": "1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1}
    response = client.get("/", params={"first": "1", "second": "2"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "extra_forbidden",
                "loc": ["query", "second"],
                "msg": "Extra inputs are not permitted",
                "input": "2",
            }
        ]
    }


def test_model_fields_can_share_an_unused_alias_choice():
    app = FastAPI()

    class Model(BaseModel):
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("names", "legacy"))
        ]
        text: Annotated[str, Field(validation_alias=AliasChoices("text", "legacy"))]

    @app.get("/")
    def read(data: Annotated[Model, Query()]):
        return data

    client = TestClient(app)
    response = client.get("/", params={"legacy": ["one", "two"], "text": "hello"})
    assert response.status_code == 200
    assert response.json() == {"names": ["one", "two"], "text": "hello"}


def test_model_unused_alias_choice_keeps_extra_value_shape():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("names", "legacy"))
        ]

    @app.get("/")
    def read(data: Annotated[Model, Query()]):
        return data

    client = TestClient(app)
    response = client.get("/", params={"names": ["one", "two"], "legacy": "unused"})
    assert response.status_code == 200
    assert response.json() == {"names": ["one", "two"], "legacy": "unused"}


@pytest.mark.parametrize(
    "field_info",
    [
        Field(alias="item"),
        Field(validation_alias="item"),
        Field(validation_alias=AliasChoices("item", "tag")),
        Field(validation_alias=AliasChoices("item", "items")),
    ],
)
@pytest.mark.parametrize(
    "config",
    [
        ConfigDict(populate_by_name=True),
        pytest.param(
            ConfigDict(validate_by_name=True),
            marks=pytest.mark.skipif(
                PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
                reason="validate_by_name requires Pydantic 2.11",
            ),
        ),
    ],
)
def test_model_list_populated_by_name(field_info, config):
    app = FastAPI()

    class Model(BaseModel):
        model_config = config
        items: Annotated[list[int], field_info]

    @app.get("/")
    def read(data: Annotated[Model, Query()]):
        return {"items": data.items}

    client = TestClient(app)
    response = client.get("/", params={"items": "1"})
    assert response.status_code == 200
    assert response.json() == {"items": [1]}
    response = client.get("/", params={"items": "1", "item": "2"})
    assert response.status_code == 200
    assert response.json() == {"items": [2]}
    response = client.get("/", params={"items": "invalid"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["query", "items", 0],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }
    response = client.get("/", params={"items": "1", "item": "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "item", 0]


@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
    reason="validate_by_name and validate_by_alias require Pydantic 2.11",
)
@pytest.mark.parametrize(
    "field_info",
    [
        Field(alias="tag"),
        Field(validation_alias="tag"),
        Field(validation_alias=AliasChoices("item", "tag")),
    ],
)
def test_model_can_disable_validation_by_alias(field_info):
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(validate_by_alias=False, extra="forbid")
        items: Annotated[list[str], field_info]

    @app.get("/")
    def read(data: Annotated[Model, Query()]):
        return {"items": data.items}

    client = TestClient(app)
    response = client.get("/", params={"items": "one"})
    assert response.status_code == 200
    assert response.json() == {"items": ["one"]}
    response = client.get("/", params={"items": "one", "tag": "two"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "extra_forbidden",
                "loc": ["query", "tag"],
                "msg": "Extra inputs are not permitted",
                "input": "two",
            }
        ]
    }


def test_empty_string_alias():
    app = FastAPI()

    @app.get("/")
    def read(value: Annotated[int, Query(validation_alias=AliasChoices("", "other"))]):
        return value

    client = TestClient(app)
    response = client.get("/?=1&other=2")
    assert response.status_code == 200
    assert response.json() == 1


@pytest.mark.parametrize(
    "validation_alias",
    [AliasPath("items", 0), AliasChoices("first", AliasPath("items", 0))],
)
def test_model_alias_path_is_unchanged(validation_alias: AliasPath | AliasChoices):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[int, Field(validation_alias=validation_alias)]

    @app.get("/")
    def read(data: Annotated[Model, Query()]):
        return data

    client = TestClient(app)
    response = client.get("/?items=1&items=2")
    assert response.status_code == 200
    assert response.json() == {"value": 1}


def test_reused_model_still_accepts_headers():
    response = client.get("/headers", headers={"second": "1"})
    assert response.status_code == 200
    assert response.json() == {"ignored": 1, "items": ["default"]}


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/individual": {
                    "get": {
                        "summary": "Read Individual",
                        "operationId": "read_individual_individual_get",
                        "parameters": [
                            {
                                "name": "first",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "integer", "title": "First"},
                            },
                            {
                                "name": "item",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "title": "Chosen items",
                                    "default": ["default"],
                                },
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
                "/model": {
                    "get": {
                        "summary": "Read Model",
                        "operationId": "read_model_model_get",
                        "parameters": [
                            {
                                "name": "first",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "integer", "title": "First"},
                            },
                            {
                                "name": "item",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "title": "Chosen items",
                                    "default": ["default"],
                                },
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
                "/headers": {
                    "get": {
                        "summary": "Read Headers",
                        "operationId": "read_headers_headers_get",
                        "parameters": [
                            {
                                "name": "first",
                                "in": "header",
                                "required": True,
                                "schema": {"type": "integer", "title": "First"},
                            },
                            {
                                "name": "item",
                                "in": "header",
                                "required": False,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "title": "Chosen items",
                                    "default": ["default"],
                                },
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
