from typing import List, Optional, Union

import pytest
from fastapi.openapi.constants import TypeValue
from fastapi.openapi.models import Schema


@pytest.mark.parametrize(
    "type_value",
    [
        "array",
        ["string", "null"],
        None,
    ],
)
def test_allowed_schema_type(
    type_value: Optional[Union[TypeValue, List[TypeValue]]],
) -> None:
    """Test that Schema accepts TypeValue, List[TypeValue] and None for type field."""
    schema = Schema(type=type_value)
    assert schema.type == type_value


def test_invalid_type_value() -> None:
    """Test that Schema raises ValueError for invalid type values."""
    with pytest.raises(ValueError, match="2 validation errors for Schema"):
        Schema(type=True)  # type: ignore[arg-type]
