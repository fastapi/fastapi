from unittest.mock import patch

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient

from ...utils import needs_py310


@pytest.fixture
def client():
    from docs_src.body.tutorial001_py310 import app

    client = TestClient(app)
    return client


@needs_py310
def test_body_float(client: TestClient):
    response = client.post("/items/", json={"name": "Foo", "price": 50.5})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 50.5,
        "description": None,
        "tax": None,
    }


@needs_py310
def test_post_with_str_float(client: TestClient):
    response = client.post("/items/", json={"name": "Foo", "price": "50.5"})
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 50.5,
        "description": None,
        "tax": None,
    }


@needs_py310
def test_post_with_str_float_description(client: TestClient):
    response = client.post(
        "/items/", json={"name": "Foo", "price": "50.5", "description": "Some Foo"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 50.5,
        "description": "Some Foo",
        "tax": None,
    }


@needs_py310
def test_post_with_str_float_description_tax(client: TestClient):
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": "50.5", "description": "Some Foo", "tax": 0.3},
    )
    assert response.status_code == 200
    assert response.json() == {
        "name": "Foo",
        "price": 50.5,
        "description": "Some Foo",
        "tax": 0.3,
    }


@needs_py310
def test_post_with_only_name(client: TestClient):
    response = client.post("/items/", json={"name": "Foo"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "price"],
                    "msg": "Field required",
                    "input": {"name": "Foo"},
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "price"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@needs_py310
def test_post_with_only_name_price(client: TestClient):
    response = client.post("/items/", json={"name": "Foo", "price": "twenty"})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "float_parsing",
                    "loc": ["body", "price"],
                    "msg": "Input should be a valid number, unable to parse string as a number",
                    "input": "twenty",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "price"],
                    "msg": "value is not a valid float",
                    "type": "type_error.float",
                }
            ]
        }
    )


@needs_py310
def test_post_with_no_data(client: TestClient):
    response = client.post("/items/", json={})
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body", "name"],
                    "msg": "Field required",
                    "input": {},
                },
                {
                    "type": "missing",
                    "loc": ["body", "price"],
                    "msg": "Field required",
                    "input": {},
                },
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", "name"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "price"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }
    )


@needs_py310
def test_post_with_none(client: TestClient):
    response = client.post("/items/", json=None)
    assert response.status_code == 422
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "missing",
                    "loc": ["body"],
                    "msg": "Field required",
                    "input": None,
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "field required",
                    "type": "value_error.missing",
                }
            ]
        }
    )


@needs_py310
def test_post_broken_body(client: TestClient):
    response = client.post(
        "/items/",
        headers={"content-type": "application/json"},
        content="{some broken json}",
    )
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "json_invalid",
                    "loc": ["body", 1],
                    "msg": "JSON decode error",
                    "input": {},
                    "ctx": {
                        "error": "Expecting property name enclosed in double quotes"
                    },
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body", 1],
                    "msg": "Expecting property name enclosed in double quotes: line 1 column 2 (char 1)",
                    "type": "value_error.jsondecode",
                    "ctx": {
                        "msg": "Expecting property name enclosed in double quotes",
                        "doc": "{some broken json}",
                        "pos": 1,
                        "lineno": 1,
                        "colno": 2,
                    },
                }
            ]
        }
    )


@needs_py310
def test_post_form_for_json(client: TestClient):
    response = client.post("/items/", data={"name": "Foo", "price": 50.5})
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": "name=Foo&price=50.5",
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "value is not a valid dict",
                    "type": "type_error.dict",
                }
            ]
        }
    )


@needs_py310
def test_explicit_content_type(client: TestClient):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 200, response.text


@needs_py310
def test_geo_json(client: TestClient):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
        headers={"Content-Type": "application/geo+json"},
    )
    assert response.status_code == 200, response.text


@needs_py310
def test_no_content_type_is_json(client: TestClient):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "Foo",
        "description": None,
        "price": 50.5,
        "tax": None,
    }


@needs_py310
def test_wrong_headers(client: TestClient):
    data = '{"name": "Foo", "price": 50.5}'
    response = client.post(
        "/items/", content=data, headers={"Content-Type": "text/plain"}
    )
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": '{"name": "Foo", "price": 50.5}',
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "value is not a valid dict",
                    "type": "type_error.dict",
                }
            ]
        }
    )

    response = client.post(
        "/items/", content=data, headers={"Content-Type": "application/geo+json-seq"}
    )
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": '{"name": "Foo", "price": 50.5}',
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "value is not a valid dict",
                    "type": "type_error.dict",
                }
            ]
        }
    )
    response = client.post(
        "/items/", content=data, headers={"Content-Type": "application/not-really-json"}
    )
    assert response.status_code == 422, response.text
    assert response.json() == IsDict(
        {
            "detail": [
                {
                    "type": "model_attributes_type",
                    "loc": ["body"],
                    "msg": "Input should be a valid dictionary or object to extract fields from",
                    "input": '{"name": "Foo", "price": 50.5}',
                }
            ]
        }
    ) | IsDict(
        # TODO: remove when deprecating Pydantic v1
        {
            "detail": [
                {
                    "loc": ["body"],
                    "msg": "value is not a valid dict",
                    "type": "type_error.dict",
                }
            ]
        }
    )


@needs_py310
def test_other_exceptions(client: TestClient):
    with patch("json.loads", side_effect=Exception):
        response = client.post("/items/", json={"test": "test2"})
        assert response.status_code == 400, response.text


@needs_py310
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/items/": {
                "post": {
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
                    "summary": "Create Item",
                    "operationId": "create_item_items__post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Item"}
                            }
                        },
                        "required": True,
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
                        "description": IsDict(
                            {
                                "title": "Description",
                                "anyOf": [{"type": "string"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Description", "type": "string"}
                        ),
                        "tax": IsDict(
                            {
                                "title": "Tax",
                                "anyOf": [{"type": "number"}, {"type": "null"}],
                            }
                        )
                        | IsDict(
                            # TODO: remove when deprecating Pydantic v1
                            {"title": "Tax", "type": "number"}
                        ),
                    },
                },
                "ValidationError": {
                    "title": "ValidationError",
                    "required": ["loc", "msg", "type"],
                    "type": "object",
                    "properties": {
                        "loc": {
                            "title": "Location",
                            "type": "array",
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
                        },
                        "msg": {"title": "Message", "type": "string"},
                        "type": {"title": "Error Type", "type": "string"},
                    },
                },
                "HTTPValidationError": {
                    "title": "HTTPValidationError",
                    "type": "object",
                    "properties": {
                        "detail": {
                            "title": "Detail",
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/ValidationError"},
                        }
                    },
                },
            }
        },
    }
