from typing import Annotated

import pytest
from fastapi import Cookie, FastAPI, Header, Path
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

app = FastAPI()


@app.get("/header")
def read_header(
    x_value: Annotated[
        int,
        Header(alias="ignored", validation_alias=AliasChoices("X-First", "X-Second")),
    ],
    item_values: Annotated[
        list[str], Header(validation_alias=AliasChoices("item_values", "X-Tag"))
    ] = ["default"],  # noqa: B006
):
    return {"value": x_value, "items": item_values}


class HeaderModel(BaseModel):
    x_value: Annotated[
        int,
        Field(alias="ignored", validation_alias=AliasChoices("X-First", "X-Second")),
    ]
    item_values: Annotated[
        list[str], Field(validation_alias=AliasChoices("item_values", "X-Tag"))
    ] = ["default"]


@app.get("/header-model")
def read_header_model(data: Annotated[HeaderModel, Header()]):
    return {"value": data.x_value, "items": data.item_values}


@app.get("/cookie")
def read_cookie(
    value: Annotated[
        int,
        Cookie(
            alias="ignored", validation_alias=AliasChoices("session", "legacy_session")
        ),
    ],
):
    return {"value": value}


class CookieModel(BaseModel):
    value: Annotated[
        int,
        Field(
            alias="ignored", validation_alias=AliasChoices("session", "legacy_session")
        ),
    ]


@app.get("/cookie-model")
def read_cookie_model(data: Annotated[CookieModel, Cookie()]):
    return {"value": data.value}


@app.get("/path/{value}")
def read_path(
    value: Annotated[int, Path(validation_alias=AliasChoices("first", "second"))],
):
    return value


client = TestClient(app)


@pytest.mark.parametrize("path", ["/header", "/header-model"])
@pytest.mark.parametrize("alias", ["x-first", "X-SECOND"])
def test_header_choices_are_case_insensitive(path: str, alias: str):
    response = client.get(path, headers={alias: "1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": ["default"]}


@pytest.mark.parametrize("path", ["/header", "/header-model"])
@pytest.mark.parametrize("alias", ["ITEM_VALUES", "x-tag"])
@pytest.mark.parametrize("items", [["one"], ["one", "two"], [""]])
def test_header_list_choices_preserve_items(path: str, alias: str, items: list[str]):
    headers = [("x-first", "1")] + [(alias, item) for item in items]
    response = client.get(path, headers=headers)
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": items}


@pytest.mark.parametrize("path", ["/header", "/header-model"])
def test_repeated_scalar_header_uses_first_value(path: str):
    response = client.get(path, headers=[("X-Second", "1"), ("x-second", "2")])
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": ["default"]}


@pytest.mark.parametrize("path", ["/header", "/header-model"])
def test_header_choices_follow_declaration_order(path: str):
    response = client.get(
        path,
        headers=[
            ("x-second", "2"),
            ("x-first", "1"),
            ("x-tag", "unused"),
            ("item_values", "one"),
            ("item_values", "two"),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {"value": 1, "items": ["one", "two"]}


@pytest.mark.parametrize("path", ["/header", "/header-model"])
@pytest.mark.parametrize(
    "headers, alias, value",
    [
        ({"x-first": "invalid", "x-second": "2"}, "X-First", "invalid"),
        ({"x-first": "", "x-second": "2"}, "X-First", ""),
        ({"x-second": "invalid"}, "X-Second", "invalid"),
    ],
)
def test_invalid_header_choice_uses_selected_alias(path, headers, alias, value):
    response = client.get(path, headers=headers)
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["header", alias],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": value,
            }
        ]
    }


@pytest.mark.parametrize("path", ["/header", "/header-model"])
def test_header_missing_uses_first_choice(path: str):
    response = client.get(path, headers={"ignored": "1", "x-value": "1"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"] == ["header", "X-First"]


@pytest.mark.parametrize("path", ["/cookie", "/cookie-model"])
@pytest.mark.parametrize("alias", ["session", "legacy_session"])
def test_cookie_choices(path: str, alias: str):
    response = client.get(path, headers={"cookie": f"{alias}=1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1}


@pytest.mark.parametrize("path", ["/cookie", "/cookie-model"])
def test_cookie_choices_follow_declaration_order(path: str):
    response = client.get(path, headers={"cookie": "legacy_session=2; session=1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1}


@pytest.mark.parametrize("path", ["/cookie", "/cookie-model"])
def test_repeated_cookie_uses_last_value(path: str):
    response = client.get(
        path, headers={"cookie": "legacy_session=1; legacy_session=2"}
    )
    assert response.status_code == 200
    assert response.json() == {"value": 2}


@pytest.mark.parametrize("path", ["/cookie", "/cookie-model"])
@pytest.mark.parametrize(
    "cookie, alias, value",
    [
        ("session=invalid; legacy_session=2", "session", "invalid"),
        ("session=; legacy_session=2", "session", ""),
        ("legacy_session=invalid", "legacy_session", "invalid"),
    ],
)
def test_invalid_cookie_choice_uses_selected_alias(path, cookie, alias, value):
    response = client.get(path, headers={"cookie": cookie})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["cookie", alias],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": value,
            }
        ]
    }


@pytest.mark.parametrize("path", ["/cookie", "/cookie-model"])
@pytest.mark.parametrize("cookie", ["", "value=1; ignored=1", "Session=1"])
def test_cookie_missing_and_unaccepted_names(path: str, cookie: str):
    response = client.get(path, headers={"cookie": cookie})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    assert response.json()["detail"][0]["loc"] == ["cookie", "session"]


@pytest.mark.parametrize("path", ["/", "/model"])
def test_cookie_default(path: str):
    app = FastAPI()

    class Model(BaseModel):
        value: Annotated[
            int, Field(validation_alias=AliasChoices("first", "second"))
        ] = 10

    @app.get("/model")
    def read_model(data: Annotated[Model, Cookie()]):
        return data.value

    @app.get("/")
    def read(
        value: Annotated[
            int, Cookie(validation_alias=AliasChoices("first", "second"))
        ] = 10,
    ):
        return value

    client = TestClient(app)
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == 10


def test_header_model_does_not_duplicate_lowercase_alias_as_extra():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        host: str
        value: Annotated[
            int, Field(validation_alias=AliasChoices("X-First", "X-Second"))
        ]

    @app.get("/")
    def read(data: Annotated[Model, Header()]):
        return data

    client = TestClient(app)
    client.headers.clear()
    response = client.get("/", headers={"x-second": "1"})
    assert response.status_code == 200
    assert response.json() == {"host": "testserver", "value": 1}
    response = client.get("/", headers={"x-first": "1", "x-second": "2"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "extra_forbidden",
                "loc": ["header", "x-second"],
                "msg": "Extra inputs are not permitted",
                "input": "2",
            }
        ]
    }


def test_header_model_fields_can_share_an_unused_alias_choice():
    app = FastAPI()

    class Model(BaseModel):
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("Names", "Legacy"))
        ]
        text: Annotated[str, Field(validation_alias=AliasChoices("Text", "Legacy"))]

    @app.get("/")
    def read(data: Annotated[Model, Header()]):
        return data

    client = TestClient(app)
    response = client.get(
        "/", headers=[("legacy", "one"), ("legacy", "two"), ("text", "hello")]
    )
    assert response.status_code == 200
    assert response.json() == {"names": ["one", "two"], "text": "hello"}


def test_header_model_unused_alias_choice_keeps_extra_value_shape():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="allow")
        host: str
        names: Annotated[
            list[str], Field(validation_alias=AliasChoices("Names", "Legacy"))
        ]

    @app.get("/")
    def read(data: Annotated[Model, Header()]):
        return data

    client = TestClient(app)
    client.headers.clear()
    response = client.get(
        "/", headers=[("names", "one"), ("names", "two"), ("legacy", "unused")]
    )
    assert response.status_code == 200
    assert response.json() == {
        "host": "testserver",
        "names": ["one", "two"],
        "legacy": "unused",
    }


def test_cookie_model_preserves_unused_choice_as_extra():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(extra="forbid")
        value: Annotated[int, Field(validation_alias=AliasChoices("first", "second"))]

    @app.get("/")
    def read(data: Annotated[Model, Cookie()]):
        return data

    client = TestClient(app)
    response = client.get("/", headers={"cookie": "second=1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1}
    response = client.get("/", headers={"cookie": "first=1; second=2"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "extra_forbidden",
                "loc": ["cookie", "second"],
                "msg": "Extra inputs are not permitted",
                "input": "2",
            }
        ]
    }


@pytest.mark.parametrize(
    "config, expected_value",
    [
        (ConfigDict(populate_by_name=True), 2),
        pytest.param(
            ConfigDict(validate_by_alias=False),
            1,
            marks=pytest.mark.skipif(
                PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
                reason="validate_by_alias requires Pydantic 2.11",
            ),
        ),
    ],
)
@pytest.mark.parametrize(
    "convert_underscores, name, rejected_name",
    [(True, "x-values", "x_values"), (False, "x_values", "x-values")],
)
@pytest.mark.parametrize(
    "field_info",
    [
        Field(alias="X-Second"),
        Field(validation_alias="X-Second"),
        Field(validation_alias=AliasChoices("X-First", "X-Second")),
    ],
)
def test_header_model_name_fallback(
    config, expected_value, convert_underscores, name, rejected_name, field_info
):
    app = FastAPI()

    class Model(BaseModel):
        model_config = config
        x_values: Annotated[list[int], field_info]

    @app.get("/")
    def read(data: Annotated[Model, Header(convert_underscores=convert_underscores)]):
        return {"x_values": data.x_values}

    client = TestClient(app)
    response = client.get("/", headers={name: "1"})
    assert response.status_code == 200
    assert response.json() == {"x_values": [1]}
    response = client.get("/", headers={rejected_name: "1"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == "missing"
    response = client.get("/", headers={name: "1", "x-second": "2"})
    assert response.status_code == 200
    assert response.json() == {"x_values": [expected_value]}
    response = client.get("/", headers={name: "invalid"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["header", name, 0]


@pytest.mark.parametrize(
    "config, expected_value",
    [
        (ConfigDict(populate_by_name=True), 2),
        pytest.param(
            ConfigDict(validate_by_alias=False),
            1,
            marks=pytest.mark.skipif(
                PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
                reason="validate_by_alias requires Pydantic 2.11",
            ),
        ),
    ],
)
@pytest.mark.parametrize(
    "field_info",
    [
        Field(alias="second"),
        Field(validation_alias="second"),
        Field(validation_alias=AliasChoices("first", "second")),
    ],
)
def test_cookie_model_name_fallback(config, expected_value, field_info):
    app = FastAPI()

    class Model(BaseModel):
        model_config = config
        value: Annotated[int, field_info]

    @app.get("/")
    def read(data: Annotated[Model, Cookie()]):
        return {"value": data.value}

    client = TestClient(app)
    response = client.get("/", headers={"cookie": "value=1"})
    assert response.status_code == 200
    assert response.json() == {"value": 1}
    response = client.get("/", headers={"cookie": "value=1; second=2"})
    assert response.status_code == 200
    assert response.json() == {"value": expected_value}


def test_unmatched_path_alias_choices_preserve_parameter_name():
    response = client.get("/path/1")
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
                "/header": {
                    "get": {
                        "summary": "Read Header",
                        "operationId": "read_header_header_get",
                        "parameters": [
                            {
                                "name": "X-First",
                                "in": "header",
                                "required": True,
                                "schema": {"type": "integer", "title": "X-First"},
                            },
                            {
                                "name": "item_values",
                                "in": "header",
                                "required": False,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "default": ["default"],
                                    "title": "Item Values",
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
                "/header-model": {
                    "get": {
                        "summary": "Read Header Model",
                        "operationId": "read_header_model_header_model_get",
                        "parameters": [
                            {
                                "name": "X-First",
                                "in": "header",
                                "required": True,
                                "schema": {"type": "integer", "title": "X-First"},
                            },
                            {
                                "name": "item_values",
                                "in": "header",
                                "required": False,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "default": ["default"],
                                    "title": "Item Values",
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
                "/cookie": {
                    "get": {
                        "summary": "Read Cookie",
                        "operationId": "read_cookie_cookie_get",
                        "parameters": [
                            {
                                "name": "session",
                                "in": "cookie",
                                "required": True,
                                "schema": {"type": "integer", "title": "Session"},
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
                "/cookie-model": {
                    "get": {
                        "summary": "Read Cookie Model",
                        "operationId": "read_cookie_model_cookie_model_get",
                        "parameters": [
                            {
                                "name": "session",
                                "in": "cookie",
                                "required": True,
                                "schema": {"type": "integer", "title": "Session"},
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
                "/path/{value}": {
                    "get": {
                        "summary": "Read Path",
                        "operationId": "read_path_path__value__get",
                        "parameters": [
                            {
                                "name": "value",
                                "in": "path",
                                "required": True,
                                "schema": {"type": "integer", "title": "Value"},
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
