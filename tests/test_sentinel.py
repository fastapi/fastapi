from typing import Union

import pydantic_core
import pytest
from fastapi import Body, Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

try:
    # We support older pydantic versions, so do a safe import
    from pydantic_core import MISSING
except ImportError:

    class MISSING:
        pass


def create_app():
    app = FastAPI()

    class Item(BaseModel):
        data: Union[str, MISSING, None] = MISSING  # pyright: ignore[reportInvalidTypeForm] - requires pyright option: enableExperimentalFeatures = true
        # see https://docs.pydantic.dev/latest/concepts/experimental/#missing-sentinel

    @app.post("/sentinel/")
    def sentinel(
        item: Item = Body(),
    ):
        return item

    @app.get("/query_sentinel/")
    def query_sentinel(
        data: Union[str, MISSING, None] = Query(default=MISSING),  # pyright: ignore[reportInvalidTypeForm]
    ):
        return data

    @app.get("/header_sentinel/")
    def header_sentinel(
        data: Union[str, MISSING, None] = Header(default=MISSING),  # pyright: ignore[reportInvalidTypeForm]
    ):
        return data

    @app.get("/cookie_sentinel/")
    def cookie_sentinel(
        data: Union[str, MISSING, None] = Cookie(default=MISSING),  # pyright: ignore[reportInvalidTypeForm]
    ):
        return data

    return app


@pytest.mark.skipif(
    pydantic_core.__version__ < "2.37.0",
    reason="This pydantic_core version doesn't support MISSING",
)
def test_call_api():
    app = create_app()
    client = TestClient(app)
    response = client.post("/sentinel/", json={})
    assert response.status_code == 200, response.text
    response = client.post("/sentinel/", json={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.get("/query_sentinel/")
    assert response.status_code == 200, response.text
    response = client.get("/query_sentinel/", params={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.get("/header_sentinel/")
    assert response.status_code == 200, response.text
    response = client.get("/header_sentinel/", headers={"data": "Foo"})
    assert response.status_code == 200, response.text
    response = client.get("/cookie_sentinel/")
    assert response.status_code == 200, response.text
    client.cookies = {"data": "Foo"}
    response = client.get("/cookie_sentinel/")
    assert response.status_code == 200, response.text


@pytest.mark.skipif(
    pydantic_core.__version__ < "2.37.0",
    reason="This pydantic_core version doesn't support MISSING",
)
def test_openapi_schema():
    """
    Test that example overrides work:

    * pydantic model schema_extra is included
    * Body(example={}) overrides schema_extra in pydantic model
    * Body(examples{}) overrides Body(example={}) and schema_extra in pydantic model
    """
    app = create_app()
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/sentinel/": {
                "post": {
                    "summary": "Sentinel",
                    "operationId": "sentinel_sentinel__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/Item",
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
            "/query_sentinel/": {
                "get": {
                    "summary": "Query Sentinel",
                    "operationId": "query_sentinel_query_sentinel__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Data",
                            },
                            "name": "data",
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
            "/header_sentinel/": {
                "get": {
                    "summary": "Header Sentinel",
                    "operationId": "header_sentinel_header_sentinel__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Data",
                            },
                            "name": "data",
                            "in": "header",
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
            "/cookie_sentinel/": {
                "get": {
                    "summary": "Cookie Sentinel",
                    "operationId": "cookie_sentinel_cookie_sentinel__get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                                "title": "Data",
                            },
                            "name": "data",
                            "in": "cookie",
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
                "Item": {
                    "title": "Item",
                    "type": "object",
                    "properties": {
                        "data": {
                            "title": "Data",
                            "anyOf": [{"type": "string"}, {"type": "null"}],
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
