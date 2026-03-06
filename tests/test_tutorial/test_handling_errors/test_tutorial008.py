from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from docs_src.handling_errors.tutorial008_py310 import app

client = TestClient(app)


def test_get_magic():
    response = client.get("/magic/unicorns/shinny")
    assert response.status_code == 200, response.text
    assert response.json() == {"unicorn_name": "shinny"}


def test_get_magic_exception():
    response = client.get("/magic/unicorns/yolo")
    assert response.status_code == 418, response.text
    assert response.json() == {"message": "Global handler: yolo did something."}


def test_get_special():
    response = client.get("/special/unicorns/shinny")
    assert response.status_code == 200, response.text
    assert response.json() == {"unicorn_name": "shinny"}


def test_get_special_exception():
    response = client.get("/special/unicorns/yolo")
    assert response.status_code == 418, response.text
    assert response.json() == {
        "message": "Special handler: yolo did something magical!"
    }


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/magic/unicorns/{name}": {
                    "get": {
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
                        "summary": "Read Magic Unicorn",
                        "operationId": "read_magic_unicorn_magic_unicorns__name__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Name", "type": "string"},
                                "name": "name",
                                "in": "path",
                            }
                        ],
                    }
                },
                "/special/unicorns/{name}": {
                    "get": {
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
                        "summary": "Read Special Unicorn",
                        "operationId": "read_special_unicorn_special_unicorns__name__get",
                        "parameters": [
                            {
                                "required": True,
                                "schema": {"title": "Name", "type": "string"},
                                "name": "name",
                                "in": "path",
                            }
                        ],
                    }
                },
            },
            "components": {
                "schemas": {
                    "ValidationError": {
                        "title": "ValidationError",
                        "required": ["loc", "msg", "type"],
                        "type": "object",
                        "properties": {
                            "loc": {
                                "title": "Location",
                                "type": "array",
                                "items": {
                                    "anyOf": [
                                        {"type": "string"},
                                        {"type": "integer"},
                                    ]
                                },
                            },
                            "msg": {"title": "Message", "type": "string"},
                            "type": {"title": "Error Type", "type": "string"},
                            "input": {"title": "Input"},
                            "ctx": {"title": "Context", "type": "object"},
                        },
                    },
                    "HTTPValidationError": {
                        "title": "HTTPValidationError",
                        "type": "object",
                        "properties": {
                            "detail": {
                                "title": "Detail",
                                "type": "array",
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
                            }
                        },
                    },
                }
            },
        }
    )
