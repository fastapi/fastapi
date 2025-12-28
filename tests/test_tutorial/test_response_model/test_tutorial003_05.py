import importlib

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial003_05_py39"),
        pytest.param("tutorial003_05_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.response_model.{request.param}")

    client = TestClient(mod.app)
    return client


def test_get_portal(client: TestClient):
    response = client.get("/portal")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Here's your interdimensional portal."}


def test_get_redirect(client: TestClient):
    response = client.get("/portal", params={"teleport": True}, follow_redirects=False)
    assert response.status_code == 307, response.text
    assert response.headers["location"] == "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/portal": {
                "get": {
                    "summary": "Get Portal",
                    "operationId": "get_portal_portal_get",
                    "parameters": [
                        {
                            "required": False,
                            "schema": {
                                "title": "Teleport",
                                "type": "boolean",
                                "default": False,
                            },
                            "name": "teleport",
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
            }
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
