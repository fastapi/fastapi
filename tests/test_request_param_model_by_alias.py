from typing import Annotated

import pytest
from dirty_equals import IsPartialDict
from fastapi import Cookie, FastAPI, Header, Query
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


class Model(BaseModel):
    param: str = Field(alias="param_alias")


@app.get("/query")
async def query_model(data: Model = Query()):
    return {"param": data.param}


@app.get("/header")
async def header_model(data: Model = Header()):
    return {"param": data.param}


@app.get("/cookie")
async def cookie_model(data: Model = Cookie()):
    return {"param": data.param}


def test_query_model_with_alias():
    client = TestClient(app)
    response = client.get("/query", params={"param_alias": "value"})
    assert response.status_code == 200, response.text
    assert response.json() == {"param": "value"}


def test_header_model_with_alias():
    client = TestClient(app)
    response = client.get("/header", headers={"param_alias": "value"})
    assert response.status_code == 200, response.text
    assert response.json() == {"param": "value"}


def test_cookie_model_with_alias():
    client = TestClient(app)
    client.cookies.set("param_alias", "value")
    response = client.get("/cookie")
    assert response.status_code == 200, response.text
    assert response.json() == {"param": "value"}


def test_query_model_with_alias_by_name():
    client = TestClient(app)
    response = client.get("/query", params={"param": "value"})
    assert response.status_code == 422, response.text
    details = response.json()
    assert details["detail"][0]["input"] == {"param": "value"}


def test_header_model_with_alias_by_name():
    client = TestClient(app)
    response = client.get("/header", headers={"param": "value"})
    assert response.status_code == 422, response.text
    details = response.json()
    assert details["detail"][0]["input"] == IsPartialDict({"param": "value"})


def test_cookie_model_with_alias_by_name():
    client = TestClient(app)
    client.cookies.set("param", "value")
    response = client.get("/cookie")
    assert response.status_code == 422, response.text
    details = response.json()
    assert details["detail"][0]["input"] == {"param": "value"}


@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 11),
    reason="validate_by_alias requires Pydantic 2.11",
)
def test_openapi_with_validation_by_alias_disabled():
    app = FastAPI()

    class Model(BaseModel):
        model_config = ConfigDict(validate_by_alias=False)
        int_value: Annotated[int, Field(alias="legacy")]

    @app.get("/query")
    def read_query(data: Annotated[Model, Query()]):
        return data

    @app.get("/header")
    def read_header(data: Annotated[Model, Header()]):
        return data

    @app.get("/cookie")
    def read_cookie(data: Annotated[Model, Cookie()]):
        return data

    client = TestClient(app)
    response = client.get("/query", params={"int_value": "1"})
    assert response.status_code == 200
    assert response.json() == {"legacy": 1}
    response = client.get("/header", headers={"int-value": "1"})
    assert response.status_code == 200
    assert response.json() == {"legacy": 1}
    response = client.get("/cookie", headers={"cookie": "int_value=1"})
    assert response.status_code == 200
    assert response.json() == {"legacy": 1}
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
                                "name": "int_value",
                                "in": "query",
                                "required": True,
                                "schema": {"type": "integer", "title": "Int Value"},
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
                "/header": {
                    "get": {
                        "summary": "Read Header",
                        "operationId": "read_header_header_get",
                        "parameters": [
                            {
                                "name": "int-value",
                                "in": "header",
                                "required": True,
                                "schema": {"type": "integer", "title": "Int Value"},
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
                "/cookie": {
                    "get": {
                        "summary": "Read Cookie",
                        "operationId": "read_cookie_cookie_get",
                        "parameters": [
                            {
                                "name": "int_value",
                                "in": "cookie",
                                "required": True,
                                "schema": {"type": "integer", "title": "Int Value"},
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
