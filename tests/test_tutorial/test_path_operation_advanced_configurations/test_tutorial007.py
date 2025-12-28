import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        pytest.param("tutorial007_py39"),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.path_operation_advanced_configuration.{request.param}"
    )

    client = TestClient(mod.app)
    return client


def test_post(client: TestClient):
    yaml_data = """
        name: Deadpoolio
        tags:
        - x-force
        - x-men
        - x-avengers
        """
    response = client.post("/items/", content=yaml_data)
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Deadpoolio",
        "tags": ["x-force", "x-men", "x-avengers"],
    }


def test_post_broken_yaml(client: TestClient):
    yaml_data = """
        name: Deadpoolio
        tags:
        x - x-force
        x - x-men
        x - x-avengers
        """
    response = client.post("/items/", content=yaml_data)
    assert response.status_code == 422, response.text
    assert response.json() == {"detail": "Invalid YAML"}


def test_post_invalid(client: TestClient):
    yaml_data = """
        name: Deadpoolio
        tags:
        - x-force
        - x-men
        - x-avengers
        - sneaky: object
        """
    response = client.post("/items/", content=yaml_data)
    assert response.status_code == 422, response.text
    # insert_assert(response.json())
    assert response.json() == {
        "detail": [
            {
                "type": "string_type",
                "loc": ["tags", 3],
                "msg": "Input should be a valid string",
                "input": {"sneaky": "object"},
            }
        ]
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
                    "summary": "Create Item",
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/x-yaml": {
                                "schema": {
                                    "title": "Item",
                                    "required": ["name", "tags"],
                                    "type": "object",
                                    "properties": {
                                        "name": {"title": "Name", "type": "string"},
                                        "tags": {
                                            "title": "Tags",
                                            "type": "array",
                                            "items": {"type": "string"},
                                        },
                                    },
                                }
                            }
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            }
        },
    }
