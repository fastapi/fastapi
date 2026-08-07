from typing import Annotated, Any, Generic, TypeVar

from fastapi import FastAPI
from fastapi._compat import field_annotation_is_custom_object_type
from fastapi.testclient import TestClient
from pydantic import BaseModel, GetCoreSchemaHandler, SecretStr
from pydantic_core import CoreSchema, core_schema

T = TypeVar("T")


def _point_schema(cls: Any) -> CoreSchema:
    return core_schema.no_info_wrap_validator_function(
        lambda value, handler: (
            value if isinstance(value, cls) else cls(**handler(value))
        ),
        core_schema.typed_dict_schema(
            {
                "x": core_schema.typed_dict_field(core_schema.int_schema()),
                "y": core_schema.typed_dict_field(core_schema.int_schema()),
            }
        ),
        serialization=core_schema.plain_serializer_function_ser_schema(
            lambda point: {"x": point.x, "y": point.y}
        ),
    )


class Point:
    """Object-shaped custom type: validates from a JSON object."""

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _point_schema(cls)


class GenericPoint(Generic[T]):
    """Same shape, but generic, to check bare vs parameterized consistency."""

    def __init__(self, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return _point_schema(cls)


class Token:
    """Scalar-shaped custom type: validates from a JSON string."""

    def __init__(self, value: str) -> None:
        self.value = value

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.no_info_after_validator_function(
            cls,
            core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda token: token.value
            ),
        )


class Opaque:
    """Custom type whose JSON schema can't be generated."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.is_instance_schema(cls)


class RecursiveModel(BaseModel):
    children: list["RecursiveModel"] = []


class WarnsDuringSchemaGeneration:
    """Object-shaped custom type whose JSON schema generation emits a
    PydanticJsonSchemaWarning (non-JSON-serializable default) but succeeds."""

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        return core_schema.typed_dict_schema(
            {
                "x": core_schema.typed_dict_field(
                    core_schema.with_default_schema(
                        core_schema.any_schema(), default=object()
                    )
                )
            }
        )


app = FastAPI()


@app.post("/points/")
def create_point(point: Point) -> Point:
    return Point(x=point.x + 1, y=point.y + 1)


@app.post("/generic-points/")
def create_generic_point(point: GenericPoint[int]) -> dict[str, int]:
    return {"x": point.x, "y": point.y}


@app.post("/bare-generic-points/")
def create_bare_generic_point(point: GenericPoint) -> dict[str, int]:
    return {"x": point.x, "y": point.y}


@app.post("/optional-points/")
def create_optional_point(point: Point | None = None) -> dict[str, Any]:
    if point is None:
        return {"point": None}
    return {"point": {"x": point.x, "y": point.y}}


@app.get("/tokens/")
def read_token(token: Token) -> dict[str, str]:
    return {"token": token.value}


@app.get("/secrets/")
def read_secret(secret: SecretStr) -> dict[str, int]:
    return {"length": len(secret.get_secret_value())}


client = TestClient(app)


def test_custom_object_type_is_a_body_param():
    response = client.post("/points/", json={"x": 1, "y": 2})
    assert response.status_code == 200, response.text
    assert response.json() == {"x": 2, "y": 3}


def test_custom_object_type_validation_error():
    response = client.post("/points/", json={"x": "not-an-int", "y": 2})
    assert response.status_code == 422, response.text


def test_bare_and_parameterized_generic_are_both_body_params():
    # A bare class and its parameterized form must classify the same way.
    for path in ("/generic-points/", "/bare-generic-points/"):
        response = client.post(path, json={"x": 1, "y": 2})
        assert response.status_code == 200, response.text
        assert response.json() == {"x": 1, "y": 2}


def test_optional_custom_object_type_is_a_body_param():
    response = client.post("/optional-points/", json={"x": 1, "y": 2})
    assert response.status_code == 200, response.text
    assert response.json() == {"point": {"x": 1, "y": 2}}

    response = client.post("/optional-points/")
    assert response.status_code == 200, response.text
    assert response.json() == {"point": None}


def test_scalar_shaped_custom_type_is_still_a_query_param():
    response = client.get("/tokens/", params={"token": "abc"})
    assert response.status_code == 200, response.text
    assert response.json() == {"token": "abc"}


def test_secret_str_is_still_a_query_param():
    response = client.get("/secrets/", params={"secret": "hunter2"})
    assert response.status_code == 200, response.text
    assert response.json() == {"length": 7}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    paths = response.json()["paths"]

    point_post = paths["/points/"]["post"]
    assert "requestBody" in point_post
    assert "parameters" not in point_post

    optional_post = paths["/optional-points/"]["post"]
    assert "requestBody" in optional_post
    assert "parameters" not in optional_post

    token_get = paths["/tokens/"]["get"]
    assert "requestBody" not in token_get
    assert [param["in"] for param in token_get["parameters"]] == ["query"]

    secret_get = paths["/secrets/"]["get"]
    assert "requestBody" not in secret_get
    assert [param["in"] for param in secret_get["parameters"]] == ["query"]


def test_field_annotation_is_custom_object_type():
    assert field_annotation_is_custom_object_type(Point)
    assert field_annotation_is_custom_object_type(GenericPoint)
    assert field_annotation_is_custom_object_type(Point | None)
    assert field_annotation_is_custom_object_type(Point | Token)
    assert field_annotation_is_custom_object_type(Annotated[Point, "meta"])
    # Self-referencing types hide their body behind a top-level $ref.
    assert field_annotation_is_custom_object_type(RecursiveModel)
    # Schema generation warnings don't affect classification (this test module
    # runs under `filterwarnings = error`, so an unsuppressed warning would
    # raise and misclassify).
    assert field_annotation_is_custom_object_type(WarnsDuringSchemaGeneration)

    assert not field_annotation_is_custom_object_type(Token)
    assert not field_annotation_is_custom_object_type(SecretStr)
    assert not field_annotation_is_custom_object_type(Token | None)
    assert not field_annotation_is_custom_object_type(int)
    assert not field_annotation_is_custom_object_type(str)
    assert not field_annotation_is_custom_object_type(None)
    # No JSON schema available: classification is left unchanged.
    assert not field_annotation_is_custom_object_type(Opaque)
