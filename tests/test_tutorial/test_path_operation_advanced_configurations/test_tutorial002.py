from fastapi.testclient import TestClient

from docs_src.path_operation_advanced_configuration.tutorial002 import app

client = TestClient(app)


def test_get():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == [{"item_id": "Foo"}]


def test_openapi_schema():
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
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Read Items",
                    "operationId": "read_items",
                }
            }
        },
    }
