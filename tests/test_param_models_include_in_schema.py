from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class QueryModel(BaseModel):
    visible: str = "visible"
    hidden: str = Query("hidden", include_in_schema=False)


class HeaderModel(BaseModel):
    x_visible: str = "visible"
    x_hidden: str = Header("hidden", include_in_schema=False)


class CookieModel(BaseModel):
    visible: str = "visible"
    hidden: str = Cookie("hidden", include_in_schema=False)


@app.get("/query")
async def read_query(data: QueryModel = Query()):
    return data


@app.get("/header")
async def read_header(data: HeaderModel = Header()):
    return data


@app.get("/cookie")
async def read_cookie(data: CookieModel = Cookie()):
    return data


client = TestClient(app)


def test_query_hidden_field_still_works():
    response = client.get("/query", params={"visible": "foo", "hidden": "bar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"visible": "foo", "hidden": "bar"}


def test_header_hidden_field_still_works():
    response = client.get("/header", headers={"x-visible": "foo", "x-hidden": "bar"})
    assert response.status_code == 200, response.text
    assert response.json() == {"x_visible": "foo", "x_hidden": "bar"}


def test_cookie_hidden_field_still_works():
    with TestClient(app, cookies={"visible": "foo", "hidden": "bar"}) as c:
        response = c.get("/cookie")
    assert response.status_code == 200, response.text
    assert response.json() == {"visible": "foo", "hidden": "bar"}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/query": {
                "get": {
                    "summary": "Read Query",
                    "operationId": "read_query_query_get",
                    "parameters": [
                        {
                            "name": "visible",
                            "in": "query",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "visible",
                                "title": "Visible",
                            },
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
                            "name": "x-visible",
                            "in": "header",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "visible",
                                "title": "X Visible",
                            },
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
                            "name": "visible",
                            "in": "cookie",
                            "required": False,
                            "schema": {
                                "type": "string",
                                "default": "visible",
                                "title": "Visible",
                            },
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
