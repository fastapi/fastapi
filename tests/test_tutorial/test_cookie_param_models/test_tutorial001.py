import importlib

import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

from tests.utils import needs_py39, needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial001",
        pytest.param("tutorial001_py310", marks=needs_py310),
        "tutorial001_an",
        pytest.param("tutorial001_an_py39", marks=needs_py39),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.cookie_param_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_cookie_param_model(client: TestClient):
    with client as c:
        c.cookies.set("session_id", "123")
        c.cookies.set("fatebook_tracker", "456")
        c.cookies.set("googall_tracker", "789")
        response = c.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "session_id": "123",
        "fatebook_tracker": "456",
        "googall_tracker": "789",
    }


def test_cookie_param_model_defaults(client: TestClient):
    with client as c:
        c.cookies.set("session_id", "123")
        response = c.get("/items/")
    assert response.status_code == 200
    assert response.json() == {
        "session_id": "123",
        "fatebook_tracker": None,
        "googall_tracker": None,
    }


def test_cookie_param_model_invalid(client: TestClient):
    response = client.get("/items/")
    assert response.status_code == 422
    assert response.json() == snapshot(
        IsDict(
            {
                "detail": [
                    {
                        "type": "missing",
                        "loc": ["cookie", "session_id"],
                        "msg": "Field required",
                        "input": {},
                    }
                ]
            }
        )
        | IsDict(
            # TODO: remove when deprecating Pydantic v1
            {
                "detail": [
                    {
                        "type": "value_error.missing",
                        "loc": ["cookie", "session_id"],
                        "msg": "field required",
                    }
                ]
            }
        )
    )


def test_cookie_param_model_extra(client: TestClient):
    with client as c:
        c.cookies.set("session_id", "123")
        c.cookies.set("extra", "track-me-here-too")
        response = c.get("/items/")
    assert response.status_code == 200
    assert response.json() == snapshot(
        {"session_id": "123", "fatebook_tracker": None, "googall_tracker": None}
    )


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/items/": {
                    "get": {
                        "summary": "Read Items",
                        "operationId": "read_items_items__get",
                        "parameters": [
                            {
                                "name": "session_id",
                                "in": "cookie",
                                "required": True,
                                "schema": {"type": "string", "title": "Session Id"},
                            },
                            {
                                "name": "fatebook_tracker",
                                "in": "cookie",
                                "required": False,
                                "schema": IsDict(
                                    {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Fatebook Tracker",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {
                                        "type": "string",
                                        "title": "Fatebook Tracker",
                                    }
                                ),
                            },
                            {
                                "name": "googall_tracker",
                                "in": "cookie",
                                "required": False,
                                "schema": IsDict(
                                    {
                                        "anyOf": [{"type": "string"}, {"type": "null"}],
                                        "title": "Googall Tracker",
                                    }
                                )
                                | IsDict(
                                    # TODO: remove when deprecating Pydantic v1
                                    {
                                        "type": "string",
                                        "title": "Googall Tracker",
                                    }
                                ),
                            },
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
                                "items": {
                                    "$ref": "#/components/schemas/ValidationError"
                                },
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
    )
