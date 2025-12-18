import asyncio

from fastapi.testclient import TestClient

from docs_src.path_params.tutorial003b_py39 import app, read_users2

client = TestClient(app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200, response.text
    assert response.json() == ["Rick", "Morty"]


def test_read_users2():  # Just for coverage
    assert asyncio.run(read_users2()) == ["Bean", "Elfo"]


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/users": {
                "get": {
                    "operationId": "read_users2_users_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Read Users2",
                },
            },
        },
    }
