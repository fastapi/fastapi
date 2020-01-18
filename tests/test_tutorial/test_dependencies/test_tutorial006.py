from starlette.testclient import TestClient

from dependencies.tutorial006 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/": {
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
                "summary": "Read Items",
                "operationId": "read_items_items__get",
                "parameters": [
                    {
                        "required": True,
                        "schema": {"title": "X-Token", "type": "string"},
                        "name": "x-token",
                        "in": "header",
                    },
                    {
                        "required": True,
                        "schema": {"title": "X-Key", "type": "string"},
                        "name": "x-key",
                        "in": "header",
                    },
                ],
            }
        }
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
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_get_no_headers():
    response = client.get("/items/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["header", "x-token"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["header", "x-key"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }


def test_get_invalid_one_header():
    response = client.get("/items/", headers={"X-Token": "invalid"})
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Token header invalid"}


def test_get_invalid_second_header():
    response = client.get(
        "/items/", headers={"X-Token": "fake-super-secret-token", "X-Key": "invalid"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "X-Key header invalid"}


def test_get_valid_headers():
    response = client.get(
        "/items/",
        headers={
            "X-Token": "fake-super-secret-token",
            "X-Key": "fake-super-secret-key",
        },
    )
    assert response.status_code == 200
    assert response.json() == [{"item": "Foo"}, {"item": "Bar"}]
