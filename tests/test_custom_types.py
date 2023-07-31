import pytest
from fastapi.testclient import TestClient

from .utils import needs_pydanticv2


@pytest.fixture(name="client", params=["default", "annotated"])
def get_client(request) -> TestClient:
    from typing import Any, Callable

    from fastapi import FastAPI, Query
    from pydantic import GetJsonSchemaHandler
    from pydantic.json_schema import JsonSchemaValue
    from pydantic_core import core_schema
    from typing_extensions import Annotated

    class WrappedInt:
        x: int

        def __init__(self, x: int):
            self.x = x

    class _WrappedIntPydanticAnnotation:
        @classmethod
        def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Callable[[Any], core_schema.CoreSchema]
        ) -> core_schema.CoreSchema:
            from_int_schema = core_schema.chain_schema(
                [
                    core_schema.int_schema(),
                    core_schema.no_info_plain_validator_function(WrappedInt),
                ]
            )
            return core_schema.json_or_python_schema(
                json_schema=from_int_schema,
                python_schema=core_schema.union_schema(
                    [
                        core_schema.is_instance_schema(WrappedInt),
                        from_int_schema,
                    ]
                ),
                serialization=core_schema.plain_serializer_function_ser_schema(
                    lambda instance: instance.x
                ),
            )

        @classmethod
        def __get_pydantic_json_schema__(
            cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler
        ) -> JsonSchemaValue:
            return handler(core_schema.int_schema())

    PydanticWrappedInt = Annotated[WrappedInt, _WrappedIntPydanticAnnotation]

    app = FastAPI()

    param_style = request.param
    if param_style == "default":

        @app.get("/echo")
        def echo(x: PydanticWrappedInt = Query()) -> PydanticWrappedInt:
            return x

    elif param_style == "annotated":

        @app.get("/echo")
        def echo(x: Annotated[PydanticWrappedInt, Query()]) -> PydanticWrappedInt:
            return x

    else:
        raise ValueError(param_style)  # pragma: nocover

    client = TestClient(app)
    return client


@needs_pydanticv2
def test_custom_type(client: TestClient):
    response = client.get("/echo", params={"x": 42})
    assert response.status_code == 200
    assert response.json() == 42


@needs_pydanticv2
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/echo": {
                "get": {
                    "summary": "Echo",
                    "operationId": "echo_echo_get",
                    "parameters": [
                        {
                            "name": "x",
                            "in": "query",
                            "required": True,
                            "schema": {"type": "integer", "title": "X"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "integer",
                                        "title": "Response Echo Echo Get",
                                    }
                                }
                            },
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
