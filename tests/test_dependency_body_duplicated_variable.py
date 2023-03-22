from typing import Awaitable, Callable, List
from unittest.mock import ANY

import pytest
from fastapi import Body, Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def make_field(name: str) -> Callable[..., Awaitable[str]]:
    async def inner(value: str = Body(..., alias=name)) -> str:
        return value

    return inner


@app.post("/example")
def example(
    field_0: str = Body(...),
    _field_1: str = Body(..., alias="field_1"),
    _field_2: str = Depends(make_field("field_2")),
    _field_3: str = Depends(make_field("field_3")),
) -> List[str]:
    return [field_0, _field_1, _field_2, _field_3]


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/example": {
            "post": {
                "summary": "Example",
                "operationId": "example_example_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/components/schemas/Body_example_example_post"
                            }
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "title": "Response Example Example Post",
                                    "type": "array",
                                    "items": {"type": "string"},
                                }
                            }
                        },
                    },
                    "422": ANY,
                },
            }
        }
    },
    "components": {
        "schemas": {
            "Body_example_example_post": {
                "title": "Body_example_example_post",
                "type": "object",
                "properties": {
                    "field_0": {"title": "Field 0", "type": "string"},
                    "field_1": {"title": "Field 1", "type": "string"},
                    "field_2": {"title": "Field 2", "type": "string"},
                    "field_3": {"title": "Field 3", "type": "string"},
                },
                "required": ["field_0", "field_1", "field_2", "field_3"],
            },
            "HTTPValidationError": ANY,
            "ValidationError": ANY,
        }
    },
}


client = TestClient(app)


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def _field_missing(name):
    return {
        "loc": ["body", name],
        "msg": "field required",
        "type": "value_error.missing",
    }


@pytest.mark.parametrize(
    "body_json,expected_status,expected_response",
    [
        [
            {},
            422,
            {
                "detail": [
                    _field_missing("field_2"),
                    _field_missing("field_3"),
                    _field_missing("field_0"),
                    _field_missing("field_1"),
                ],
            },
        ],
        [
            {"field_0": "a", "field_1": "b", "field_2": "c", "field_3": "d"},
            200,
            ["a", "b", "c", "d"],
        ],
    ],
)
def test_endpoint(body_json, expected_status, expected_response):
    response = client.post("/example/", json=body_json)
    assert response.status_code == expected_status, response.text
    assert response.json() == expected_response
