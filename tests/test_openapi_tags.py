from fastapi.testclient import TestClient

from docs_src.metadata.tutorial004 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/bar": {
            "get": {
                "operationId": "get_bar_bar_get",
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful Response",
                    }
                },
                "summary": "Get Bar",
                "tags": ["bar"],
            }
        },
        "/foo": {
            "get": {
                "operationId": "get_foo_foo_get",
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful Response",
                    }
                },
                "summary": "Get Foo",
                "tags": ["foo"],
            }
        },
    },
    "tags": [
        {"description": "This is the description for tag FOO", "name": "foo"},
        {
            "description": "This is the description for tag BAR",
            "externalDocs": {
                "description": "External documentation",
                "url": "https://fastapi.tiangolo.com/",
            },
            "name": "bar",
        },
    ],
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_get_api_route1():
    response = client.get("/foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": "foo"}


def test_get_api_route2():
    response = client.get("/bar")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": "bar"}
