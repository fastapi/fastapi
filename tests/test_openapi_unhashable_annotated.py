from typing import Annotated

from pydantic.fields import FieldInfo

from fastapi._compat.v2 import ModelField, get_definitions


class UnhashableMetadata:
    """Simulates third-party field metadata (e.g. from SQLModel extensions)
    that does not implement ``__hash__``."""

    __hash__ = None  # type: ignore[assignment]


def test_get_definitions_with_unhashable_annotation() -> None:
    """``get_definitions()`` should not crash when a field annotation is an
    ``Annotated`` type containing unhashable metadata.

    Regression: the function used a set comprehension over
    ``field_info.annotation`` values.  ``Annotated`` types that include
    metadata with ``__hash__ = None`` (e.g. certain SQLModel / Pydantic
    extension field-info objects) are themselves unhashable, causing
    ``TypeError: unhashable type`` when building the set.
    """
    field = ModelField(
        field_info=FieldInfo(annotation=Annotated[int, UnhashableMetadata()]),
        name="test_field",
        mode="validation",
    )
    # Should not raise TypeError
    get_definitions(
        fields=[field],
        model_name_map={},
        separate_input_output_schemas=True,
    )
