import itertools
from typing import List

import pytest
from fastapi.openapi.constants import TypeValue
from fastapi.openapi.models import Schema

# Define all possible type values
TYPE_VALUES: List[TypeValue] = [
    "array",
    "boolean",
    "integer",
    "null",
    "number",
    "object",
    "string",
]

# Generate all combinations of 2 or more types
TYPE_COMBINATIONS = [
    list(combo)
    for size in range(2, len(TYPE_VALUES) + 1)
    for combo in itertools.combinations(TYPE_VALUES, size)
]


@pytest.mark.parametrize("type_val", TYPE_VALUES)
def test_schema_type_single_type_value(type_val: TypeValue) -> None:
    """Test that Schema accepts single TypeValue for type field."""
    schema = Schema(type=type_val)
    assert schema.type == type_val


@pytest.mark.parametrize("type_list", TYPE_COMBINATIONS)
def test_schema_type_multiple_type_value(type_list: List[TypeValue]) -> None:
    """Test all possible combinations of TypeValue for Schema type field."""
    schema = Schema(type=type_list)
    assert schema.type == type_list


def test_schema_type_none_value() -> None:
    """Test that Schema accepts None for type field (Optional)."""
    schema = Schema(type=None)
    assert schema.type is None


def test_schema_default_type() -> None:
    """Test that Schema defaults to None for type field if not specified."""
    schema_default = Schema()
    assert schema_default.type is None
