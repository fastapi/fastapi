from typing import Annotated

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@pytest.fixture(name="client")
def get_client():
    from pydantic import (
        BaseModel,
        ConfigDict,
        PlainSerializer,
        TypeAdapter,
        WithJsonSchema,
    )

    class FakeNumpyArray:
        def __init__(self):
            self.data = [1.0, 2.0, 3.0]

    FakeNumpyArrayPydantic = Annotated[
        FakeNumpyArray,
        WithJsonSchema(TypeAdapter(list[float]).json_schema()),
        PlainSerializer(lambda v: v.data),
    ]

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        custom_field: FakeNumpyArrayPydantic

    app = FastAPI()

    @app.get("/")
    def test() -> MyModel:
        return MyModel(custom_field=FakeNumpyArray())

    client = TestClient(app)
    return client


def test_get(client: TestClient):
    response = client.get("/")
    assert response.json() == {"custom_field": [1.0, 2.0, 3.0]}


def test_typeadapter():
    # This test is only to confirm that Pydantic alone is working as expected
    from pydantic import (
        BaseModel,
        ConfigDict,
        PlainSerializer,
        TypeAdapter,
        WithJsonSchema,
    )

    class FakeNumpyArray:
        def __init__(self):
            self.data = [1.0, 2.0, 3.0]

    FakeNumpyArrayPydantic = Annotated[
        FakeNumpyArray,
        WithJsonSchema(TypeAdapter(list[float]).json_schema()),
        PlainSerializer(lambda v: v.data),
    ]

    class MyModel(BaseModel):
        model_config = ConfigDict(arbitrary_types_allowed=True)
        custom_field: FakeNumpyArrayPydantic

    ta = TypeAdapter(MyModel)
    assert ta.dump_python(MyModel(custom_field=FakeNumpyArray())) == {
        "custom_field": [1.0, 2.0, 3.0]
    }
    assert ta.json_schema() == snapshot(
        {
            "properties": {
                "custom_field": {
                    "items": {"type": "number"},
                    "title": "Custom Field",
                    "type": "array",
                }
            },
            "required": ["custom_field"],
            "title": "MyModel",
            "type": "object",
        }
    )


def test_openapi_schema(client: TestClient):
    response = client.get("openapi.json")
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "summary": "Test",
                        "operationId": "test__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/MyModel"
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
            },
            "components": {
                "schemas": {
                    "MyModel": {
                        "properties": {
                            "custom_field": {
                                "items": {"type": "number"},
                                "type": "array",
                                "title": "Custom Field",
                            }
                        },
                        "type": "object",
                        "required": ["custom_field"],
                        "title": "MyModel",
                    }
                }
            },
        }
    )
