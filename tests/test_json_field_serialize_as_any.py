"""
Regression tests for:
  PydanticUserError when a generic BaseModel with a Json[T] field is
  specialized with SerializeAsAny[SomeModel].

  fastapi/_compat/v2.py: get_model_fields() must suppress config= for
  Annotated-wrapped types whose inner type is a BaseModel / dataclass,
  not only for bare BaseModel types.
"""

from typing import Generic, TypeVar

from fastapi import FastAPI
from pydantic import BaseModel, Json, SerializeAsAny

T = TypeVar("T")


class Inner(BaseModel):
    value: str


class Source(BaseModel, Generic[T]):
    payload: Json[T]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


def test_openapi_schema_generation_serialize_as_any_does_not_raise():
    """app.openapi() must not raise PydanticUserError for Source[SerializeAsAny[Inner]].

    Previously raised:
      pydantic.errors.PydanticUserError: Cannot use `config` when the type
      is a BaseModel, dataclass or TypedDict.

    Root cause: get_model_fields() in fastapi/_compat/v2.py did not unwrap
    Annotated before checking if config= should be suppressed, so
    Json[Annotated[Inner, SerializeAsAny]] slipped through and TypeAdapter
    received config= illegally.
    """
    app = FastAPI()

    @app.get("/search")
    def search() -> Source[SerializeAsAny[Inner]]:  # pragma: no cover
        ...

    schema = app.openapi()
    assert schema is not None
    # The route must appear in the generated schema.
    assert "/search" in schema["paths"]


def test_openapi_schema_generation_plain_inner_unaffected():
    """Baseline: Source[Inner] (no SerializeAsAny) must continue to work."""
    app = FastAPI()

    @app.get("/search")
    def search() -> Source[Inner]:  # pragma: no cover
        ...

    schema = app.openapi()
    assert schema is not None
    assert "/search" in schema["paths"]
