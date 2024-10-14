from typing import Literal

from fastapi import FastAPI, Query
from fastapi._compat import PYDANTIC_V2, GenerateJsonSchema
from fastapi.openapi.utils import JsonSchemaValue
from fastapi.testclient import TestClient


class MyGenerateJsonSchema(GenerateJsonSchema):
    """Custom JSON schema generator."""

    def literal_schema(self, schema) -> JsonSchemaValue:
        result = super().literal_schema(schema)
        if "const" not in result:
            return result

        # Here, we want to exclude "enum" and "type" from the result.
        return {
            key: value for key, value in result.items() if key not in ("type", "enum")
        }


app = FastAPI(schema_generator_class=MyGenerateJsonSchema)


@app.get("/foo")
def foo(
    my_const_param: Literal["cd"] = Query(),
    my_enum_param: Literal["h", "ij"] = Query(),
    my_const_param_with_default: Literal["ab"] = Query(default="ab"),
    my_enum_param_with_default: Literal["ef", "g"] = Query(default="g"),
):
    return {"message": "Hello World"}


client = TestClient(app)


def test_app():
    response = client.get("/foo?my_const_param=cd&my_enum_param=ij")
    assert response.status_code == 200, response.text


def test_openapi_schema():
    if PYDANTIC_V2:
        parameters = [
            {
                "name": "my_const_param",
                "in": "query",
                "required": True,
                "schema": {
                    "title": "My Const Param",
                    "const": "cd",
                },
            },
            {
                "name": "my_enum_param",
                "in": "query",
                "required": True,
                "schema": {
                    "title": "My Enum Param",
                    "type": "string",
                    "enum": ["h", "ij"],
                },
            },
            {
                "name": "my_const_param_with_default",
                "in": "query",
                "required": False,
                "schema": {
                    "title": "My Const Param With Default",
                    "const": "ab",
                    "default": "ab",
                },
            },
            {
                "name": "my_enum_param_with_default",
                "in": "query",
                "required": False,
                "schema": {
                    "title": "My Enum Param With Default",
                    "type": "string",
                    "enum": ["ef", "g"],
                    "default": "g",
                },
            },
        ]
    else:
        # pydantic v1 does not use a JSON schema generator, and FastAPI
        # only defines it for compatibility.
        parameters = [
            {
                "name": "my_const_param",
                "in": "query",
                "required": True,
                "schema": {
                    "title": "My Const Param",
                    "type": "string",
                    "enum": ["cd"],
                },
            },
            {
                "name": "my_enum_param",
                "in": "query",
                "required": True,
                "schema": {
                    "title": "My Enum Param",
                    "type": "string",
                    "enum": ["h", "ij"],
                },
            },
            {
                "name": "my_const_param_with_default",
                "in": "query",
                "required": False,
                "schema": {
                    "title": "My Const Param With Default",
                    "type": "string",
                    "enum": ["ab"],
                    "default": "ab",
                },
            },
            {
                "name": "my_enum_param_with_default",
                "in": "query",
                "required": False,
                "schema": {
                    "title": "My Enum Param With Default",
                    "type": "string",
                    "enum": ["ef", "g"],
                    "default": "g",
                },
            },
        ]

    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
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
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [{"type": "string"}, {"type": "integer"}]
                            },
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
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/foo": {
                "get": {
                    "summary": "Foo",
                    "operationId": "foo_foo_get",
                    "parameters": parameters,
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
    }
