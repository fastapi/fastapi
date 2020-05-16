from fastapi.testclient import TestClient

from .app.main import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/a/compute": {
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
                "summary": "Compute",
                "operationId": "compute_a_compute_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_compute_a_compute_post"
                            }
                        }
                    },
                    "required": True,
                },
            }
        },
        "/b/compute/": {
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
                "summary": "Compute",
                "operationId": "compute_b_compute__post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_compute_b_compute__post"
                            }
                        }
                    },
                    "required": True,
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Body_compute_b_compute__post": {
                "title": "Body_compute_b_compute__post",
                "required": ["a", "b"],
                "type": "object",
                "properties": {
                    "a": {"title": "A", "type": "integer"},
                    "b": {"title": "B", "type": "string"},
                },
            },
            "Body_compute_a_compute_post": {
                "title": "Body_compute_a_compute_post",
                "required": ["a", "b"],
                "type": "object",
                "properties": {
                    "a": {"title": "A", "type": "integer"},
                    "b": {"title": "B", "type": "string"},
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_post_a():
    data = {"a": 2, "b": "foo"}
    response = client.post("/a/compute", json=data)
    assert response.status_code == 200, response.text
    data = response.json()


def test_post_a_invalid():
    data = {"a": "bar", "b": "foo"}
    response = client.post("/a/compute", json=data)
    assert response.status_code == 422, response.text


def test_post_b():
    data = {"a": 2, "b": "foo"}
    response = client.post("/b/compute/", json=data)
    assert response.status_code == 200, response.text
    data = response.json()


def test_post_b_invalid():
    data = {"a": "bar", "b": "foo"}
    response = client.post("/b/compute/", json=data)
    assert response.status_code == 422, response.text
