import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


@pytest.fixture(name="client", params=[True, False])
def get_client(request: pytest.FixtureRequest):
    from pydantic import computed_field

    class MyModel(BaseModel):
        id: int
        name: str
        age: int

        @computed_field
        @property
        def is_adult(self) -> bool:
            return self.age >= 18

    app = FastAPI(separate_input_output_schemas=request.param)

    @app.get("/list")
    def get_items() -> list[MyModel]:
        return [MyModel(id=1, name="Alice", age=30), MyModel(id=2, name="Bob", age=17)]

    @app.post("/item")
    def create_item(item: MyModel) -> MyModel:
        return item

    yield TestClient(app)


def test_create_item(client: TestClient):
    response = client.post(
        "/item",
        json={"id": 1, "name": "Alice", "age": 30},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"id": 1, "name": "Alice", "age": 30, "is_adult": True}


def test_get_items(client: TestClient):
    response = client.get("/list")
    assert response.status_code == 200, response.text
    assert response.json() == [
        {"id": 1, "name": "Alice", "age": 30, "is_adult": True},
        {"id": 2, "name": "Bob", "age": 17, "is_adult": False},
    ]


def test_openapi(client: TestClient):
    response = client.get("/openapi.json")
    openapi_schema = response.json()
    expected_schema = {
        "info": {
            "title": "FastAPI",
            "version": "0.1.0",
        },
        "openapi": "3.1.0",
        "paths": {
            "/item": {
                "post": {
                    "operationId": "create_item_item_post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/MyModel-Input",
                                },
                            },
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/MyModel-Output",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                        "422": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/HTTPValidationError",
                                    },
                                },
                            },
                            "description": "Validation Error",
                        },
                    },
                    "summary": "Create Item",
                },
            },
            "/list": {
                "get": {
                    "operationId": "get_items_list_get",
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "items": {
                                            "$ref": "#/components/schemas/MyModel-Output",
                                        },
                                        "title": "Response Get Items List Get",
                                        "type": "array",
                                    },
                                },
                            },
                            "description": "Successful Response",
                        },
                    },
                    "summary": "Get Items",
                },
            },
        },
        "components": {
            "schemas": {
                "HTTPValidationError": {
                    "properties": {
                        "detail": {
                            "items": {
                                "$ref": "#/components/schemas/ValidationError",
                            },
                            "title": "Detail",
                            "type": "array",
                        },
                    },
                    "title": "HTTPValidationError",
                    "type": "object",
                },
                "MyModel-Input": {
                    "properties": {
                        "age": {
                            "title": "Age",
                            "type": "integer",
                        },
                        "id": {
                            "title": "Id",
                            "type": "integer",
                        },
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                    },
                    "required": [
                        "id",
                        "name",
                        "age",
                    ],
                    "title": "MyModel",
                    "type": "object",
                },
                "MyModel-Output": {
                    "properties": {
                        "age": {
                            "title": "Age",
                            "type": "integer",
                        },
                        "id": {
                            "title": "Id",
                            "type": "integer",
                        },
                        "is_adult": {
                            "readOnly": True,
                            "title": "Is Adult",
                            "type": "boolean",
                        },
                        "name": {
                            "title": "Name",
                            "type": "string",
                        },
                    },
                    "required": [
                        "id",
                        "name",
                        "age",
                        "is_adult",
                    ],
                    "title": "MyModel",
                    "type": "object",
                },
                "ValidationError": {
                    "properties": {
                        "loc": {
                            "items": {
                                "anyOf": [
                                    {
                                        "type": "string",
                                    },
                                    {
                                        "type": "integer",
                                    },
                                ],
                            },
                            "title": "Location",
                            "type": "array",
                        },
                        "msg": {
                            "title": "Message",
                            "type": "string",
                        },
                        "type": {
                            "title": "Error Type",
                            "type": "string",
                        },
                        "ctx": {
                            "title": "Context",
                            "type": "object",
                        },
                        "input": {
                            "title": "Input",
                        },
                    },
                    "required": [
                        "loc",
                        "msg",
                        "type",
                    ],
                    "title": "ValidationError",
                    "type": "object",
                },
            },
        },
    }

    assert openapi_schema == expected_schema
