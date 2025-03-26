"""
This test is about the possibility of superimposing an additional response's media_type
over the default route's response class's media_type.
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

app = FastAPI()
client = TestClient(app)


class Error(BaseModel):
    status: str
    title: str


@app.get(
    "/a",
    responses={
        HTTP_200_OK: {"superimpose": True, "content": {"text/event-stream": {}}},
        HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Error", "model": Error},
    },
)
def a():
    pass  # pragma: no cover


@app.get(
    "/b",
    responses={
        str(HTTP_200_OK): {"content": {"text/event-stream": {}}},
        HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Error", "model": Error},
    },
)
def b():
    pass  # pragma: no cover


@app.get(
    "/c",
    responses={
        HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Error", "model": Error}
    },
)
def c():
    pass  # pragma: no cover


@app.get("/d")
def d():
    pass  # pragma: no cover


def test_openapi_schema():
    response = client.get("/openapi.json")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/a": {
                "get": {
                    "summary": "A",
                    "operationId": "a_a_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"text/event-stream": {}},
                        },
                        "500": {
                            "description": "Error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                    },
                }
            },
            "/b": {
                "get": {
                    "summary": "B",
                    "operationId": "b_b_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {"schema": {}},
                                "text/event-stream": {},
                            },
                        },
                        "500": {
                            "description": "Error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                    },
                }
            },
            "/c": {
                "get": {
                    "summary": "C",
                    "operationId": "c_c_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "500": {
                            "description": "Error",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            },
                        },
                    },
                }
            },
            "/d": {
                "get": {
                    "summary": "D",
                    "operationId": "d_d_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
        },
        "components": {
            "schemas": {
                "Error": {
                    "properties": {
                        "status": {"type": "string", "title": "Status"},
                        "title": {"type": "string", "title": "Title"},
                    },
                    "type": "object",
                    "required": ["status", "title"],
                    "title": "Error",
                }
            }
        },
    }
