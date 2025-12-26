import warnings

import pytest
from starlette.testclient import TestClient

warnings.filterwarnings(
    "ignore",
    message=r"The 'lia' package has been renamed to 'cross_web'\..*",
    category=DeprecationWarning,
)

from docs_src.graphql_.tutorial001_py39 import app  # noqa: E402


@pytest.fixture(name="client")
def get_client() -> TestClient:
    return TestClient(app)


def test_query(client: TestClient):
    response = client.post("/graphql", json={"query": "{ user { name, age } }"})
    assert response.status_code == 200
    assert response.json() == {"data": {"user": {"name": "Patrick", "age": 100}}}


def test_openapi(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/graphql": {
                "get": {
                    "operationId": "handle_http_get_graphql_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {},
                                },
                            },
                            "description": "The GraphiQL integrated development environment.",
                        },
                        "404": {
                            "description": "Not found if GraphiQL or query via GET are not enabled.",
                        },
                    },
                    "summary": "Handle Http Get",
                },
                "post": {
                    "operationId": "handle_http_post_graphql_post",
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
                    "summary": "Handle Http Post",
                },
            },
        },
    }
