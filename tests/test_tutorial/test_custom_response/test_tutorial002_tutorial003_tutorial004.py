import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="mod_name",
    params=[
        pytest.param("tutorial002_py39"),
        pytest.param("tutorial003_py39"),
        pytest.param("tutorial004_py39"),
    ],
)
def get_mod_name(request: pytest.FixtureRequest) -> str:
    return request.param


@pytest.fixture(name="client")
def get_client(mod_name: str) -> TestClient:
    mod = importlib.import_module(f"docs_src.custom_response.{mod_name}")
    return TestClient(mod.app)


html_contents = """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


def test_get_custom_response(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.text == html_contents


def test_openapi_schema(client: TestClient, mod_name: str):
    if mod_name.startswith("tutorial003"):
        response_content = {"application/json": {"schema": {}}}
    else:
        response_content = {"text/html": {"schema": {"type": "string"}}}

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
                            "content": response_content,
                        }
                    },
                    "summary": "Read Items",
                    "operationId": "read_items_items__get",
                }
            }
        },
    }
