from copy import deepcopy

from fastapi.testclient import TestClient

from docs_src.dataclasses.tutorial002 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items/next": {
            "get": {
                "summary": "Read Next Item",
                "operationId": "read_next_item_items_next_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                    }
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Item": {
                "title": "Item",
                "required": ["name", "price"],
                "type": "object",
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "price": {"title": "Price", "type": "number"},
                    "tags": {
                        "title": "Tags",
                        "type": "array",
                        "items": {"type": "string"},
                    },
                    "description": {"title": "Description", "type": "string"},
                    "tax": {"title": "Tax", "type": "number"},
                },
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    # TODO: remove this once Pydantic 1.9 is released
    # Ref: https://github.com/samuelcolvin/pydantic/pull/2557
    data = response.json()
    alternative_data1 = deepcopy(data)
    alternative_data2 = deepcopy(data)
    alternative_data1["components"]["schemas"]["Item"]["required"] = ["name", "price"]
    alternative_data2["components"]["schemas"]["Item"]["required"] = [
        "name",
        "price",
        "tags",
    ]
    assert alternative_data1 == openapi_schema or alternative_data2 == openapi_schema


def test_get_item():
    response = client.get("/items/next")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be be playin' and havin' fun",
        "tags": ["breater"],
        "tax": None,
    }
