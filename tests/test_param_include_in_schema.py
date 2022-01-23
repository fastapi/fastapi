from typing import Optional

import pytest
from fastapi import Cookie, FastAPI, Header, Path, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/hidden_cookie")
async def hidden_cookie(
    hidden_cookie: Optional[str] = Cookie(None, include_in_schema=False)
):
    return {"hidden_cookie": hidden_cookie}


@app.get("/hidden_header")
async def hidden_header(
    hidden_header: Optional[str] = Header(None, include_in_schema=False)
):
    return {"hidden_header": hidden_header}


@app.get("/hidden_path/{hidden_path}")
async def hidden_path(hidden_path: str = Path(..., include_in_schema=False)):
    return {"hidden_path": hidden_path}


@app.get("/hidden_query")
async def hidden_query(
    hidden_query: Optional[str] = Query(None, include_in_schema=False)
):
    return {"hidden_query": hidden_query}


client = TestClient(app)

openapi_shema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/hidden_cookie": {
            "get": {
                "summary": "Hidden Cookie",
                "operationId": "hidden_cookie_hidden_cookie_get",
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
        "/hidden_header": {
            "get": {
                "summary": "Hidden Header",
                "operationId": "hidden_header_hidden_header_get",
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
        "/hidden_path/{hidden_path}": {
            "get": {
                "summary": "Hidden Path",
                "operationId": "hidden_path_hidden_path__hidden_path__get",
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
        "/hidden_query": {
            "get": {
                "summary": "Hidden Query",
                "operationId": "hidden_query_hidden_query_get",
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
                        "items": {"type": "string"},
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
            },
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_shema


@pytest.mark.parametrize(
    "path,cookies,expected_status,expected_response",
    [
        (
            "/hidden_cookie",
            {},
            200,
            {"hidden_cookie": None},
        ),
        (
            "/hidden_cookie",
            {"hidden_cookie": "somevalue"},
            200,
            {"hidden_cookie": "somevalue"},
        ),
    ],
)
def test_hidden_cookie(path, cookies, expected_status, expected_response):
    response = client.get(path, cookies=cookies)
    assert response.status_code == expected_status
    assert response.json() == expected_response


@pytest.mark.parametrize(
    "path,headers,expected_status,expected_response",
    [
        (
            "/hidden_header",
            {},
            200,
            {"hidden_header": None},
        ),
        (
            "/hidden_header",
            {"Hidden-Header": "somevalue"},
            200,
            {"hidden_header": "somevalue"},
        ),
    ],
)
def test_hidden_header(path, headers, expected_status, expected_response):
    response = client.get(path, headers=headers)
    assert response.status_code == expected_status
    assert response.json() == expected_response


def test_hidden_path():
    response = client.get("/hidden_path/hidden_path")
    assert response.status_code == 200
    assert response.json() == {"hidden_path": "hidden_path"}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        (
            "/hidden_query",
            200,
            {"hidden_query": None},
        ),
        (
            "/hidden_query?hidden_query=somevalue",
            200,
            {"hidden_query": "somevalue"},
        ),
    ],
)
def test_hidden_query(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
