import re
from typing import Annotated

import pytest
from fastapi import Body, Cookie, FastAPI, File, Form, Header, Path, Query, UploadFile
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import Field


@pytest.mark.parametrize("parameter", [Path, Query, Header, Cookie, Body, Form])
@pytest.mark.parametrize(
    "mode,expected", [(None, "123"), ("smart", "123"), ("left_to_right", 123)]
)
def test_union_mode(parameter, mode, expected):
    app = FastAPI()

    @app.post("/{value}" if parameter is Path else "/")
    def read_value(value: Annotated[int | str, parameter(union_mode=mode)]):
        return value

    client = TestClient(app)
    if parameter is Path:
        response = client.post("/123")
    elif parameter is Query:
        response = client.post("/", params={"value": "123"})
    elif parameter is Header:
        response = client.post("/", headers={"value": "123"})
    elif parameter is Cookie:
        response = client.post("/", headers={"cookie": "value=123"})
    elif parameter is Body:
        response = client.post("/", json="123")
    else:
        response = client.post("/", data={"value": "123"})
    assert response.status_code == 200
    assert response.json() == expected


@pytest.mark.parametrize("parameter", [Query, Header, Body, Form])
@pytest.mark.parametrize("fail_fast,error_count", [(True, 1), (False, 2)])
def test_fail_fast(parameter, fail_fast, error_count):
    app = FastAPI()

    @app.post("/")
    def read_values(value: Annotated[list[int], parameter(fail_fast=fail_fast)]):
        return value

    client = TestClient(app)
    if parameter is Query:
        response = client.post("/", params={"value": ["invalid", "also-invalid"]})
    elif parameter is Header:
        response = client.post(
            "/", headers=[("value", "invalid"), ("value", "also-invalid")]
        )
    elif parameter is Body:
        response = client.post("/", json=["invalid", "also-invalid"])
    else:
        response = client.post("/", data={"value": ["invalid", "also-invalid"]})
    assert response.status_code == 422
    assert len(response.json()["detail"]) == error_count
    assert response.json()["detail"][0]["type"] == "int_parsing"
    assert response.json()["detail"][0]["loc"][-1] == 0

    if parameter is Query:
        response = client.post("/", params={"value": ["1", "2"]})
    elif parameter is Header:
        response = client.post("/", headers=[("value", "1"), ("value", "2")])
    elif parameter is Body:
        response = client.post("/", json=[1, 2])
    else:
        response = client.post("/", data={"value": ["1", "2"]})
    assert response.status_code == 200
    assert response.json() == [1, 2]


def test_omitted_options_preserve_pydantic_validation_metadata():
    app = FastAPI()

    @app.post("/")
    def read_values(
        number: Annotated[int | str, Field(union_mode="left_to_right"), Query()],
        values: Annotated[list[int], Field(fail_fast=True), Body()],
    ):
        return {"number": number, "values": values}

    client = TestClient(app)
    response = client.post("/?number=123", json=[1, 2])
    assert response.status_code == 200
    assert response.json() == {"number": 123, "values": [1, 2]}

    response = client.post("/?number=123", json=["invalid", "also-invalid"])
    assert response.status_code == 422
    assert len(response.json()["detail"]) == 1


def test_explicit_options_override_pydantic_validation_metadata():
    app = FastAPI()

    @app.post("/")
    def read_values(
        number: Annotated[
            int | str, Field(union_mode="left_to_right"), Query(union_mode="smart")
        ],
        values: Annotated[list[int], Field(fail_fast=True), Body(fail_fast=False)],
    ):
        return {"number": number, "values": values}

    client = TestClient(app)
    response = client.post("/?number=123", json=[1, 2])
    assert response.status_code == 200
    assert response.json() == {"number": "123", "values": [1, 2]}

    response = client.post("/?number=123", json=["invalid", "also-invalid"])
    assert response.status_code == 422
    assert [error["loc"] for error in response.json()["detail"]] == [
        ["body", 0],
        ["body", 1],
    ]


@pytest.mark.parametrize("parameter", [Path, Query, Header, Cookie, Body, Form])
@pytest.mark.parametrize("value,expected_status", [("ABC", 200), ("xyz", 422)])
def test_compiled_pattern(parameter, value, expected_status):
    app = FastAPI()

    @app.post("/{value}" if parameter is Path else "/")
    def read_value(
        value: Annotated[str, parameter(pattern=re.compile("^abc$", re.IGNORECASE))],
    ):
        return value

    client = TestClient(app)
    if parameter is Path:
        response = client.post(f"/{value}")
    elif parameter is Query:
        response = client.post("/", params={"value": value})
    elif parameter is Header:
        response = client.post("/", headers={"value": value})
    elif parameter is Cookie:
        response = client.post("/", headers={"cookie": f"value={value}"})
    elif parameter is Body:
        response = client.post("/", json=value)
    else:
        response = client.post("/", data={"value": value})
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.json() == value
    else:
        assert response.json()["detail"][0]["type"] == "string_pattern_mismatch"


@pytest.mark.parametrize("fail_fast,error_count", [(True, 1), (False, 2)])
def test_file_list_fail_fast(fail_fast, error_count):
    app = FastAPI()

    @app.post("/")
    def upload(files: Annotated[list[UploadFile], File(fail_fast=fail_fast)]):
        return [file.filename for file in files]

    client = TestClient(app)
    response = client.post(
        "/",
        files=[("files", (None, "not-a-file")), ("files", (None, "also-not-a-file"))],
    )
    assert response.status_code == 422
    assert len(response.json()["detail"]) == error_count
    assert response.json()["detail"][0]["loc"] == ["body", "files", 0]

    response = client.post("/", files={"files": ("example.txt", b"hello")})
    assert response.status_code == 200
    assert response.json() == ["example.txt"]


app = FastAPI()


def customize_schema(schema):
    schema["x-custom"] = "preserved"


@app.get("/query")
def read_query(
    value: Annotated[int | str, Query(union_mode="left_to_right")],
    items: Annotated[list[int], Query(fail_fast=True)],
    count: Annotated[int, Query(validate_default=True)] = 1,
    label: Annotated[
        str,
        Query(
            pattern=re.compile("^abc$", re.IGNORECASE),
            json_schema_extra=customize_schema,
        ),
    ] = "ABC",
):
    return {"value": value, "items": items, "count": count, "label": label}


@app.post("/body")
def read_body(
    items: Annotated[list[int], Body(fail_fast=True)],
    number: Annotated[int | str, Body(union_mode="left_to_right")],
    count: Annotated[
        int, Body(validate_default=True, json_schema_extra=customize_schema)
    ] = 1,
):
    return {"items": items, "number": number, "count": count}


client = TestClient(app)


def test_query_options():
    response = client.get("/query", params={"value": "123", "items": ["1", "2"]})
    assert response.status_code == 200
    assert response.json() == {
        "value": 123,
        "items": [1, 2],
        "count": 1,
        "label": "ABC",
    }


def test_body_options():
    response = client.post("/body", json={"items": [1, 2], "number": "123"})
    assert response.status_code == 200
    assert response.json() == {
        "items": [1, 2],
        "number": 123,
        "count": 1,
    }


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
                                "name": "value",
                                "in": "query",
                                "required": True,
                                "schema": {
                                    "anyOf": [{"type": "integer"}, {"type": "string"}],
                                    "title": "Value",
                                },
                            },
                            {
                                "name": "items",
                                "in": "query",
                                "required": True,
                                "schema": {
                                    "type": "array",
                                    "items": {"type": "integer"},
                                    "title": "Items",
                                },
                            },
                            {
                                "name": "count",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "default": 1,
                                    "title": "Count",
                                },
                            },
                            {
                                "name": "label",
                                "in": "query",
                                "required": False,
                                "schema": {
                                    "type": "string",
                                    "pattern": "^abc$",
                                    "x-custom": "preserved",
                                    "default": "ABC",
                                    "title": "Label",
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
            },
            "components": {
                "schemas": {
                    "Body_read_body_body_post": {
                        "properties": {
                            "items": {
                                "items": {"type": "integer"},
                                "type": "array",
                                "title": "Items",
                            },
                            "number": {
                                "anyOf": [{"type": "integer"}, {"type": "string"}],
                                "title": "Number",
                            },
                            "count": {
                                "type": "integer",
                                "title": "Count",
                                "default": 1,
                                "x-custom": "preserved",
                            },
                        },
                        "type": "object",
                        "required": ["items", "number"],
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
