import pytest
from fastapi.testclient import TestClient

from docs_src.path_params.tutorial002 import app


@pytest.fixture(name="client")
def get_client():
    return TestClient(app)


@pytest.mark.parametrize("parameter_value", [-10, 0, 10])
def test_with_integer_parameters(client, parameter_value):
    parameter: int = parameter_value
    response = client.get(f"/items/{parameter}")
    assert response.status_code == 200
    assert response.json() == {"item_id": parameter}


@pytest.mark.parametrize("parameter_value", [-10.00, 0.00, 10.00])
def test_with_integers_converted_to_floats(client, parameter_value):
    parameter: float = parameter_value
    response = client.get(f"/items/{parameter}")
    assert response.status_code == 200
    assert response.json() == {"item_id": int(parameter)}


@pytest.mark.parametrize("parameter_value", [-3.14, 3.14])
def test_with_float_parameters(client, parameter_value):
    parameter: float = parameter_value
    response = client.get(f"/items/{parameter}")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "item_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": f"{parameter}",
            }
        ]
    }


@pytest.mark.parametrize("parameter_value", ["foo", "foo bar", "foo bar baz"])
def test_with_string_parameters(client, parameter_value):
    parameter: str = parameter_value
    response = client.get(f"/items/{parameter}")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "item_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": f"{parameter}",
            }
        ]
    }


@pytest.mark.parametrize(
    "parameter_value", [[1, 2, 3], [-1.1, 0.0, 1.2], ["alpha", "beta", "gamma"]]
)
def test_with_list_parameters(client, parameter_value):
    parameter: list = parameter_value
    response = client.get(f"/items/{parameter}")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "int_parsing",
                "loc": ["path", "item_id"],
                "msg": "Input should be a valid integer, unable to parse string as an integer",
                "input": f"{parameter}",
            }
        ]
    }


def test_openapi_schema(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/{item_id}": {
                "get": {
                    "summary": "Read Item",
                    "operationId": "read_item_items__item_id__get",
                    "parameters": [
                        {
                            "name": "item_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "integer", "title": "Item Id"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        },
                        "422": {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError"
                                    }
                                }
                            },
                        },
                    },
                }
            }
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                            "type": "array",
                            "title": "Detail",
                        }
                    },
                    "type": "object",
                    "title": "HTTPValidationError",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                            "type": "array",
                            "title": "Location",
                        },
                        "msg": {"type": "string", "title": "Message"},
                        "type": {"type": "string", "title": "Error Type"},
                    },
                    "type": "object",
                    "required": ["loc", "msg", "type"],
                    "title": "ValidationError",
                },
            }
        },
    }
