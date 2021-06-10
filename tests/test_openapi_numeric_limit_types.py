from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class Number(BaseModel):
    floating_point: float = Field(minimum=0.0, maximum=3.14)
    integer: int = Field(
        minimum=-9_223_372_036_854_775_808, maximum=9_223_372_036_854_775_807
    )


@app.post("/foo")
def foo(number: Number):
    return number.floating_point, number.integer


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/foo": {
            "post": {
                "operationId": "foo_foo_post",
                "requestBody": {
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/Number"}
                        }
                    },
                    "required": True,
                },
                "responses": {
                    "200": {
                        "content": {"application/json": {"schema": {}}},
                        "description": "Successful Response",
                    },
                    "422": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/HTTPValidationError"
                                }
                            }
                        },
                        "description": "Validation Error",
                    },
                },
                "summary": "Foo",
            }
        }
    },
    "components": {
        "schemas": {
            "HTTPValidationError": {
                "properties": {
                    "detail": {
                        "items": {"$ref": "#/components/schemas/ValidationError"},
                        "title": "Detail",
                        "type": "array",
                    }
                },
                "title": "HTTPValidationError",
                "type": "object",
            },
            "Number": {
                "properties": {
                    "floating_point": {
                        "maximum": 3.14,
                        "minimum": 0.0,
                        "title": "Floating Point",
                        "type": "number",
                    },
                    "integer": {
                        "maximum": 9223372036854775807,
                        "minimum": -9223372036854775808,
                        "title": "Integer",
                        "type": "integer",
                    },
                },
                "required": ["floating_point", "integer"],
                "title": "Number",
                "type": "object",
            },
            "ValidationError": {
                "properties": {
                    "loc": {
                        "items": {"type": "string"},
                        "title": "Location",
                        "type": "array",
                    },
                    "msg": {"title": "Message", "type": "string"},
                    "type": {"title": "Error Type", "type": "string"},
                },
                "required": ["loc", "msg", "type"],
                "title": "ValidationError",
                "type": "object",
            },
        }
    },
}


def test_additional_properties_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_additional_properties_post():
    response = client.post("/foo", json={"floating_point": 1.23, "integer": 256})
    assert response.status_code == 200, response.text
    assert response.json() == [1.23, 256]
