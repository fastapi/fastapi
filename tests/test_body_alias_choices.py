from typing import Annotated, Any

import pytest
from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import AliasChoices, AliasPath, BaseModel

app = FastAPI()


@app.post("/embedded")
def read_embedded(
    value: Annotated[
        int,
        Body(
            embed=True,
            alias="ignored",
            validation_alias=AliasChoices("first", "second"),
        ),
    ],
):
    return value


@app.post("/multiple")
def read_multiple(
    items: Annotated[
        list[int],
        Body(default_factory=list, validation_alias=AliasChoices("items", "tags")),
    ],
    value: Annotated[
        int | None,
        Body(alias="ignored", validation_alias=AliasChoices("first", "second")),
    ] = 10,
):
    return {"value": value, "items": items}


client = TestClient(app)


@pytest.mark.parametrize(
    "body, expected",
    [
        ({"first": 1}, 1),
        ({"second": 2}, 2),
        ({"second": 2, "first": 0}, 0),
    ],
)
def test_embedded_body_alias_choices(body: dict[str, int], expected: int):
    response = client.post("/embedded", json=body)
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("path", ["/embedded", "/multiple"])
@pytest.mark.parametrize(
    "body, alias, value",
    [
        ({"first": "invalid", "second": 2}, "first", "invalid"),
        ({"first": "", "second": 2}, "first", ""),
        ({"second": "invalid"}, "second", "invalid"),
    ],
)
def test_invalid_choice_uses_selected_alias(path, body, alias, value):
    response = client.post(path, json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", alias],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": value,
            }
        ]
    }


@pytest.mark.parametrize("body", [{}, {"value": 1}, {"ignored": 1}])
def test_required_body_missing_uses_first_alias(body: dict[str, int]):
    response = client.post("/embedded", json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "missing",
                "loc": ["body", "first"],
                "msg": "Field required",
                "input": None,
            }
        ]
    }


@pytest.mark.parametrize(
    "body, expected",
    [
        ({}, {"value": 10, "items": []}),
        ({"value": 1, "ignored": 2}, {"value": 10, "items": []}),
        ({"first": 1, "items": [2, 3]}, {"value": 1, "items": [2, 3]}),
        ({"second": 2, "tags": [3, 4]}, {"value": 2, "items": [3, 4]}),
        (
            {"second": 2, "first": 0, "tags": [3], "items": []},
            {"value": 0, "items": []},
        ),
        ({"first": None, "second": 2}, {"value": None, "items": []}),
        ({"second": None}, {"value": None, "items": []}),
    ],
)
def test_multiple_body_alias_choices(body: dict[str, Any], expected: dict[str, Any]):
    response = client.post("/multiple", json=body)
    assert response.status_code == 200
    assert response.json() == expected


def test_list_error_uses_selected_alias():
    response = client.post("/multiple", json={"tags": [1, "invalid"]})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "tags", 1],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }


@pytest.mark.parametrize("body", ["null", "[]", "1", '"first"'])
def test_embedded_body_requires_an_object(body: str):
    response = client.post(
        "/multiple", content=body, headers={"content-type": "application/json"}
    )
    assert response.status_code == 422
    assert [(error["type"], error["loc"]) for error in response.json()["detail"]] == [
        ("missing", ["body", "items"]),
        ("missing", ["body", "first"]),
    ]


def test_absent_body_uses_defaults():
    response = client.post("/multiple")
    assert response.status_code == 200
    assert response.json() == {"value": 10, "items": []}


@pytest.mark.parametrize(
    "body, alias",
    [({"first": None, "second": 2}, "first"), ({"second": None}, "second")],
)
def test_explicit_null_does_not_use_another_alias_or_default(body, alias):
    app = FastAPI()
    calls = []

    def default_factory():
        calls.append(True)
        return 10

    @app.post("/")
    def read(
        value: Annotated[
            int,
            Body(
                embed=True,
                default_factory=default_factory,
                validation_alias=AliasChoices("first", "second"),
            ),
        ],
    ):
        return value

    client = TestClient(app)
    response = client.post("/", json=body)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_type",
                "loc": ["body", alias],
                "msg": "Input should be a valid integer",
                "input": None,
            }
        ]
    }
    assert calls == []
    response = client.post("/", json={})
    assert response.status_code == 200
    assert response.json() == 10
    assert calls == [True]


def test_model_body_alias_choice_preserves_nested_errors():
    app = FastAPI()

    class Item(BaseModel):
        count: int

    @app.post("/")
    def read(
        item: Annotated[
            Item, Body(embed=True, validation_alias=AliasChoices("item", "data"))
        ],
    ):
        return item

    client = TestClient(app)
    response = client.post("/", json={"data": {"count": 1}})
    assert response.status_code == 200
    assert response.json() == {"count": 1}
    response = client.post("/", json={"data": {"count": "invalid"}})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["body", "data", "count"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": "invalid",
            }
        ]
    }


def test_unembedded_body_alias_choices_do_not_wrap_the_value():
    app = FastAPI()

    @app.post("/")
    def read(
        value: Annotated[int, Body(validation_alias=AliasChoices("first", "second"))],
    ):
        return value

    client = TestClient(app)
    response = client.post("/", json=1)
    assert response.status_code == 200
    assert response.json() == 1


@pytest.mark.parametrize(
    "validation_alias",
    [AliasPath("nested", "value"), AliasChoices("first", AliasPath("nested", "value"))],
)
def test_alias_path_extraction_is_unchanged(validation_alias):
    app = FastAPI()

    @app.post("/")
    def read(
        value: Annotated[int, Body(embed=True, validation_alias=validation_alias)],
    ):
        return value

    client = TestClient(app)
    response = client.post("/", json={"value": 1, "first": 2, "nested": {"value": 3}})
    assert response.status_code == 200
    assert response.json() == 1


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/embedded": {
                    "post": {
                        "summary": "Read Embedded",
                        "operationId": "read_embedded_embedded_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_embedded_embedded_post"
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
                "/multiple": {
                    "post": {
                        "summary": "Read Multiple",
                        "operationId": "read_multiple_multiple_post",
                        "requestBody": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Body_read_multiple_multiple_post"
                                    }
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
                },
            },
            "components": {
                "schemas": {
                    "Body_read_embedded_embedded_post": {
                        "properties": {"first": {"type": "integer", "title": "First"}},
                        "type": "object",
                        "required": ["first"],
                        "title": "Body_read_embedded_embedded_post",
                    },
                    "Body_read_multiple_multiple_post": {
                        "properties": {
                            "items": {
                                "items": {"type": "integer"},
                                "type": "array",
                                "title": "Items",
                            },
                            "first": {
                                "anyOf": [{"type": "integer"}, {"type": "null"}],
                                "title": "First",
                                "default": 10,
                            },
                        },
                        "type": "object",
                        "title": "Body_read_multiple_multiple_post",
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
