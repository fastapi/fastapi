from fastapi.testclient import TestClient

from docs_src.path_operation_advanced_configuration.tutorial007 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
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


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_post():
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


def test_post_broken_yaml():
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


def test_post_invalid():
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
    assert response.json() == {
        "detail": [
            {"loc": ["tags", 3], "msg": "str type expected", "type": "type_error.str"}
        ]
    }
