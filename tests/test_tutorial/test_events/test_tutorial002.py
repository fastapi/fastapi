from starlette.testclient import TestClient

from events.tutorial002 import app

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "Fast API", "version": "0.1.0"},
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
                "summary": "Read Items Get",
                "operationId": "read_items_items__get",
            }
        }
    },
}


def test_events():
    with TestClient(app) as client:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        assert response.json() == openapi_schema
        response = client.get("/items/")
        assert response.status_code == 200
        assert response.json() == [{"name": "Foo"}]
    with open("log.txt") as log:
        assert "Application shutdown" in log.read()
