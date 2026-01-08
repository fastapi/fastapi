import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial002_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.response_directly.{request.param}")

    client = TestClient(mod.app)
    return client


def test_path_operation(client: TestClient):
    expected_content = """<?xml version="1.0"?>
    <shampoo>
    <Header>
        Apply shampoo here.
    </Header>
    <Body>
        You'll have to use soap here.
    </Body>
    </shampoo>
    """

    response = client.get("/legacy/")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"] == "application/xml"
    assert response.text == expected_content


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/legacy/": {
                "get": {
                    "operationId": "get_legacy_data_legacy__get",
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
                    "summary": "Get Legacy Data",
                },
            },
        },
    }
