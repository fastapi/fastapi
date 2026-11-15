from typing import Annotated

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot
from pydantic import (
    BaseModel,
    GetPydanticSchema,
    computed_field,
    model_validator,
)


@pytest.fixture(name="client")
def get_client(request):
    separate_input_output_schemas = request.param
    app = FastAPI(separate_input_output_schemas=separate_input_output_schemas)

    class Rectangle(BaseModel):
        width: int
        length: int

        @computed_field
        @property
        def area(self) -> int:
            return self.width * self.length

    @app.get("/")
    def read_root() -> Rectangle:
        return Rectangle(width=3, length=4)

    @app.get("/responses", responses={200: {"model": Rectangle}})
    def read_responses() -> Rectangle:
        return Rectangle(width=3, length=4)

    client = TestClient(app)
    return client


@pytest.mark.parametrize("client", [True, False], indirect=True)
@pytest.mark.parametrize("path", ["/", "/responses"])
def test_get(client: TestClient, path: str):
    response = client.get(path)
    assert response.status_code == 200, response.text
    assert response.json() == {"width": 3, "length": 4, "area": 12}


@pytest.mark.parametrize("client", [True, False], indirect=True)
def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "summary": "Read Root",
                        "operationId": "read_root__get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Rectangle"
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
                "/responses": {
                    "get": {
                        "summary": "Read Responses",
                        "operationId": "read_responses_responses_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/Rectangle"
                                        }
                                    }
                                },
                            }
                        },
                    }
                },
            },
            "components": {
                "schemas": {
                    "Rectangle": {
                        "properties": {
                            "width": {"type": "integer", "title": "Width"},
                            "length": {"type": "integer", "title": "Length"},
                            "area": {
                                "type": "integer",
                                "title": "Area",
                                "readOnly": True,
                            },
                        },
                        "type": "object",
                        "required": ["width", "length", "area"],
                        "title": "Rectangle",
                    }
                }
            },
        }
    )


class ComputedItem(BaseModel):
    name: str

    @computed_field
    @property
    def label(self) -> str:
        return f"Item: {self.name}"


class ValidatedComputedItem(ComputedItem):
    @model_validator(mode="after")
    def validate_name(self) -> "ValidatedComputedItem":
        if not self.name:
            raise ValueError("Name must not be empty")
        return self


def test_nested_computed_field_schemas():
    class Envelope(BaseModel):
        children: list["Envelope"] = []
        item: ComputedItem

    app = FastAPI(separate_input_output_schemas=False)

    @app.post("/")
    def create_item(item: Envelope) -> Envelope:
        return item

    client = TestClient(app)
    response = client.post("/", json={"item": {"name": "a"}, "children": []})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "children": [],
        "item": {"name": "a", "label": "Item: a"},
    }

    schema = app.openapi()
    operation = schema["paths"]["/"]["post"]
    assert operation["requestBody"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/Envelope-Input"
    }
    assert operation["responses"]["200"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/Envelope-Output"
    }
    schemas = schema["components"]["schemas"]
    properties = schemas["Envelope-Output"]["properties"]
    assert properties["children"]["items"] == {
        "$ref": "#/components/schemas/Envelope-Output"
    }
    assert properties["item"] == {"$ref": "#/components/schemas/ComputedItem-Output"}
    assert "label" not in schemas["ComputedItem-Input"]["properties"]
    assert schemas["ComputedItem-Output"]["properties"]["label"]["readOnly"] is True


def test_computed_field_with_after_model_validator():
    app = FastAPI(separate_input_output_schemas=False)

    @app.post("/")
    def create_item(item: ValidatedComputedItem) -> list[ValidatedComputedItem]:
        return [item]

    client = TestClient(app)
    response = client.post("/", json={"name": "a"})
    assert response.status_code == 200, response.text
    assert response.json() == [{"name": "a", "label": "Item: a"}]
    response = client.post("/", json={"name": ""})
    assert response.status_code == 422, response.text

    schema = app.openapi()
    operation = schema["paths"]["/"]["post"]
    assert operation["requestBody"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/ValidatedComputedItem-Input"
    }
    response_schema = operation["responses"]["200"]["content"]["application/json"][
        "schema"
    ]
    assert response_schema["items"] == {
        "$ref": "#/components/schemas/ValidatedComputedItem-Output"
    }
    schemas = schema["components"]["schemas"]
    assert "label" not in schemas["ValidatedComputedItem-Input"]["properties"]
    assert (
        schemas["ValidatedComputedItem-Output"]["properties"]["label"]["readOnly"]
        is True
    )


def test_recursive_computed_field_schemas():
    class RecursiveItem(ComputedItem):
        children: list["RecursiveItem"] = []

    app = FastAPI(separate_input_output_schemas=False)

    @app.post("/")
    def create_item(item: RecursiveItem) -> RecursiveItem:
        return item

    client = TestClient(app)
    response = client.post("/", json={"name": "a", "children": [{"name": "b"}]})
    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": "a",
        "children": [{"name": "b", "children": [], "label": "Item: b"}],
        "label": "Item: a",
    }

    schema = app.openapi()
    operation = schema["paths"]["/"]["post"]
    assert operation["requestBody"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/RecursiveItem-Input"
    }
    output_ref = {"$ref": "#/components/schemas/RecursiveItem-Output"}
    assert (
        operation["responses"]["200"]["content"]["application/json"]["schema"]
        == output_ref
    )
    schemas = schema["components"]["schemas"]
    assert "label" not in schemas["RecursiveItem-Input"]["properties"]
    properties = schemas["RecursiveItem-Output"]["properties"]
    assert properties["children"]["items"] == output_ref
    assert properties["label"]["readOnly"] is True


def test_shared_models_do_not_rebuild_field_schemas_per_route():
    schema_builds = 0

    def count_schema_builds(source_type, handler):
        nonlocal schema_builds
        schema_builds += 1
        return handler(source_type)

    class Item(BaseModel):
        value: Annotated[int, GetPydanticSchema(count_schema_builds)]
        child: "Item | None" = None

    class Envelope(BaseModel):
        first: Item
        second: Item

    def read_item() -> Envelope:
        return Envelope(first=Item(value=1), second=Item(value=2))

    build_counts = []
    schemas = []
    for route_count in (1, 10):
        app = FastAPI(separate_input_output_schemas=False)
        for index in range(route_count):
            app.get(f"/items/{index}")(read_item)
        schema_builds = 0
        schemas.append(app.openapi()["components"]["schemas"])
        build_counts.append(schema_builds)

    assert build_counts[0] > 0
    assert build_counts[0] == build_counts[1]
    assert schemas[0] == schemas[1]
    assert set(schemas[0]) == {"Item", "Envelope"}

    response = TestClient(app).get("/items/0")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "first": {"value": 1, "child": None},
        "second": {"value": 2, "child": None},
    }
