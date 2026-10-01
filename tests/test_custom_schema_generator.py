from typing import Any, ClassVar, Literal

import pytest
from fastapi import FastAPI
from fastapi._compat import PYDANTIC_VERSION_MINOR_TUPLE
from fastapi.openapi.utils import GenerateJsonSchema, get_openapi
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field
from pydantic_core import core_schema
from typing_extensions import NotRequired, TypedDict


class RequiredResponseSchema(GenerateJsonSchema):
    def field_is_required(
        self,
        field: core_schema.ModelField
        | core_schema.DataclassField
        | core_schema.TypedDictField,
        total: bool,
    ) -> bool:
        if self.mode == "serialization" and field["type"] != "typed-dict-field":
            return field.get("serialization_exclude_if") is None
        return super().field_is_required(field, total)


class Child(BaseModel):
    note: str | None = None


class Item(BaseModel):
    name: str
    note: str | None = None
    children: list[Child] = Field(default_factory=list)
    secret: str = Field(default="internal", exclude=True)


class Partial(TypedDict):
    value: NotRequired[str]


def create_app(**kwargs: Any) -> FastAPI:
    app = FastAPI(**kwargs)

    @app.post("/items", responses={409: {"model": Item}})
    def create_item(item: Item) -> Item:
        return item

    @app.get("/partial", response_model=Partial)
    def get_partial() -> Partial:
        return {}

    return app


def test_custom_generator_separates_requests_and_responses() -> None:
    app = create_app(schema_generator=RequiredResponseSchema)
    schema = app.openapi()
    models = schema["components"]["schemas"]
    assert models["Item-Input"]["required"] == ["name"]
    assert models["Item-Output"]["required"] == ["name", "note", "children"]
    assert models["Child-Output"]["required"] == ["note"]
    assert "required" not in models["Child-Input"]
    assert "secret" not in models["Item-Output"]["properties"]
    assert models["Item-Output"]["properties"]["note"]["anyOf"] == [
        {"type": "string"},
        {"type": "null"},
    ]
    responses = schema["paths"]["/items"]["post"]["responses"]
    assert responses["409"]["content"]["application/json"]["schema"] == {
        "$ref": "#/components/schemas/Item-Output"
    }
    with TestClient(app) as client:
        response = client.post("/items", json={"name": "example"})
        assert response.status_code == 200
        assert response.json() == {"name": "example", "note": None, "children": []}
        assert client.get("/openapi.json").json() == schema


def test_custom_generator_preserves_not_required_typed_dict_fields() -> None:
    app = create_app(schema_generator=RequiredResponseSchema)
    assert "required" not in app.openapi()["components"]["schemas"]["Partial"]
    with TestClient(app) as client:
        assert client.get("/partial").json() == {}


@pytest.mark.skipif(
    PYDANTIC_VERSION_MINOR_TUPLE < (2, 12),
    reason="Conditional field exclusion requires Pydantic 2.12+",
)
def test_custom_generator_preserves_conditional_field_exclusion() -> None:
    class Conditional(BaseModel):
        value: str | None = Field(default=None, exclude_if=lambda value: value is None)

    app = FastAPI(schema_generator=RequiredResponseSchema)

    @app.get("/conditional")
    def get_conditional() -> Conditional:
        return Conditional()

    assert "required" not in app.openapi()["components"]["schemas"]["Conditional"]
    with TestClient(app) as client:
        assert client.get("/conditional").json() == {}


def test_get_openapi_accepts_generator_for_existing_custom_openapi() -> None:
    app = create_app()
    schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
        schema_generator=RequiredResponseSchema,
    )
    assert schema["components"]["schemas"]["Item-Output"]["required"] == [
        "name",
        "note",
        "children",
    ]


def test_default_generator_preserves_existing_schema() -> None:
    models = create_app().openapi()["components"]["schemas"]
    assert models["Item-Input"]["required"] == ["name"]
    assert models["Item-Output"]["required"] == ["name"]
    assert "required" not in models["Child"]


@pytest.mark.parametrize("encoding", ["utf8", "base64"])
def test_custom_generator_preserves_fastapi_bytes_schema(
    encoding: Literal["utf8", "base64"],
) -> None:
    class BinaryItem(BaseModel):
        model_config = ConfigDict(ser_json_bytes=encoding)
        value: bytes

    def binary_app(generator: type[GenerateJsonSchema]) -> FastAPI:
        app = FastAPI(schema_generator=generator)

        @app.post("/binary")
        def binary(item: BinaryItem) -> BinaryItem:
            return item

        return app

    default_schema = binary_app(GenerateJsonSchema).openapi()
    custom_app = binary_app(RequiredResponseSchema)
    custom_schema = custom_app.openapi()
    for mode in ("Input", "Output"):
        name = f"BinaryItem-{mode}" if encoding == "base64" else "BinaryItem"
        assert (
            custom_schema["components"]["schemas"][name]
            == default_schema["components"]["schemas"][name]
        )
    with TestClient(custom_app) as client:
        response = client.post("/binary", json={"value": "hello"})
        assert response.status_code == 200
        assert response.json() == {
            "value": "aGVsbG8=" if encoding == "base64" else "hello"
        }


def test_disabled_schema_separation_still_uses_validation_schema() -> None:
    models = create_app(
        schema_generator=RequiredResponseSchema, separate_input_output_schemas=False
    ).openapi()["components"]["schemas"]
    assert models["Item"]["required"] == ["name"]
    assert "required" not in models["Child"]


def test_generator_instances_are_fresh_and_openapi_is_cached() -> None:
    class CountingGenerator(GenerateJsonSchema):
        instances: ClassVar[int] = 0

        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
            CountingGenerator.instances += 1

    app = create_app(schema_generator=CountingGenerator)
    other_app = create_app(schema_generator=CountingGenerator)
    first_schema = app.openapi()
    assert app.openapi() is first_schema
    other_app.openapi()
    assert CountingGenerator.instances == 2
    app.openapi_schema = None
    app.openapi()
    assert CountingGenerator.instances == 3
