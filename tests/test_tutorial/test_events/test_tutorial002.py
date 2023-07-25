from fastapi.testclient import TestClient

from docs_src.events.tutorial002 import app


def test_events():
    with TestClient(app) as client:
        response = client.get("/items/")
        assert response.status_code == 200, response.text
        assert response.json() == [{"name": "Foo"}]
    with open("log.txt") as log:
        assert "Application shutdown" in log.read()


def test_openapi_schema():
    with TestClient(app) as client:
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
                        "operationId": "read_items_items__get",
                    }
                }
            },
        }
