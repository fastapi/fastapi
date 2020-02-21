from typing import Sequence

import fastapi
import pydantic.fields
import pytest


class NonPydanticModel:
    pass


@pytest.mark.parametrize(
    "type_", [int, Sequence[int], pydantic.BaseModel, Sequence[pydantic.BaseModel]]
)
def test_create_response_field_accepts_valid_pydantic_field_types(type_):
    field = fastapi.utils.create_response_field(name="dummy_test_field", type_=type_)
    assert isinstance(field, pydantic.fields.ModelField)


@pytest.mark.parametrize("type_", [NonPydanticModel, Sequence[NonPydanticModel]])
def test_create_response_field_raises_for_invalid_field_types(type_):
    with pytest.raises(fastapi.exceptions.FastAPIError) as ex:
        fastapi.utils.create_response_field(name="dummy_test_field", type_=type_)
