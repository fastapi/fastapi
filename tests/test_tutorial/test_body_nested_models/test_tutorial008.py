import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial008_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.body_nested_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_post_body(client: TestClient):
    data = [
        {"url": "http://example.com/", "name": "Example"},
        {"url": "http://fastapi.tiangolo.com/", "name": "FastAPI"},
    ]
    response = client.post("/images/multiple", json=data)
    assert response.status_code == 200, response.text
    assert response.json() == data


def test_post_invalid_list_item(client: TestClient):
    data = [{"url": "not a valid url", "name": "Example"}]
    response = client.post("/images/multiple", json=data)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", 0, "url"],
                "input": "not a valid url",
                "msg": "Input should be a valid URL, relative URL without a base",
                "type": "url_parsing",
                "ctx": {"error": "relative URL without a base"},
            },
        ]
    }


def test_post_not_a_list(client: TestClient):
    data = {"url": "http://example.com/", "name": "Example"}
    response = client.post("/images/multiple", json=data)
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "loc": ["body"],
                "input": {
                    "name": "Example",
                    "url": "http://example.com/",
                },
                "msg": "Input should be a valid list",
                "type": "list_type",
            }
        ]
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/images/multiple/": {
                "post": {
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
                    "summary": "Create Multiple Images",
                    "operationId": "create_multiple_images_images_multiple__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Images",
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Image"},
                                }
                            }
                        },
                        "required": True,
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "Image": {
                    "properties": {
                        "url": {
                            "title": "Url",
                            "type": "string",
                            "format": "uri",
                            "maxLength": 2083,
                            "minLength": 1,
                        },
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                    },
                    "required": ["url", "name"],
                    "title": "Image",
                    "type": "object",
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
            }
        },
    }
