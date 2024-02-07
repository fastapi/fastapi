import pytest
from fastapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.extra_models.tutorial004_py39 import app

    client = TestClient(app)
    return client


@needs_py39
def test_get_items(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"name": "Foo", "description": "There comes my hero"},
        {"name": "Red", "description": "It's my aeroplane"},
    ]


@needs_py39
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "get": {
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "title": "Response Read Items Items  Get",
                                        "type": "array",
                                        "items": {"$ref": "#/components/schemas/Item"},
                                    }
                                }
                            },
                        }
                    },
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                }
            }
        },
        "components": {
            "schemas": {
                "Item": {
                    "title": "Item",
                    "required": ["name", "description"],
                    "type": "object",
                    "properties": {
                        "name": {"title": "Name", "type": "string"},
                        "description": {"title": "Description", "type": "string"},
                    },
                }
            }
        },
    }
