"""
Internal utility functions for FastAPI.

Provides helper functions used across the framework for path parameter
extraction, model field creation, operation ID generation, and other
internal operations.
"""

import re
import warnings
from typing import (
    TYPE_CHECKING,
    Any,
)

from fastapi._compat import (
    ModelField,
    annotation_is_pydantic_v1,
)
from fastapi.datastructures import DefaultPlaceholder, DefaultType
from fastapi.exceptions import FastAPIDeprecationWarning, PydanticV1NotSupportedError
from pydantic.fields import FieldInfo

if TYPE_CHECKING:  # pragma: nocover
    from .routing import APIRoute


def is_body_allowed_for_status_code(status_code: int | str | None) -> bool:
    if status_code is None:
        return True
    current_status_code = (
        status_code if isinstance(status_code, int) else int(status_code)
    )
    return not (current_status_code < 200 or current_status_code in {204, 205, 304})


def get_path_param_names(path: str) -> set[str]:
    return set(re.findall("{(.*?)}", path))


_invalid_args_message = (
    "Invalid args for path field! Hint: "
    "check that the `path function` has the right signature"
)


def create_model_field(
    *,
    name: str,
    type_: type[Any],
    param_field: FieldInfo,
) -> ModelField:
    if annotation_is_pydantic_v1(type_):
        raise PydanticV1NotSupportedError(
            f"Pydantic v1 models are no longer supported in FastAPI. Please update the model: {type_}"
        )
    try:
        return ModelField(
            name=name,
            field_info=param_field,
        )
    except RuntimeError:
        raise FastAPIError(_invalid_args_message) from None


def generate_operation_id_for_path(
    *, name: str, path: str, method: str
) -> str:  # pragma: nocover
    warnings.warn(
        "generate_operation_id_for_path is deprecated, use generate_unique_id instead",
        FastAPIDeprecationWarning,
        stacklevel=2,
    )
    operation_id = name + path.replace("/", "_").replace("{", "_").replace("}", "_")
    if method.lower() != "get":
        operation_id += f"_{method.lower()}"
    return operation_id


def generate_unique_id(route: "APIRoute") -> str:
    operation_id = f"{route.name}{route.path_format}"
    if len(route.methods) > 1:
        operation_id += f"__{','.join(sorted(route.methods))}"
    return operation_id


def deep_dict_update(main_dict: dict[Any, Any], update_dict: dict[Any, Any]) -> None:
    for key, value in update_dict.items():
        if (
            key in main_dict
            and isinstance(main_dict[key], dict)
            and isinstance(value, dict)
        ):
            deep_dict_update(main_dict[key], value)
        else:
            main_dict[key] = value


def get_value_or_default(
    first_item: Any,
    default_value: Any,
) -> DefaultPlaceholder | DefaultType:
    """
    Get the value or return the default value wrapped in a DefaultPlaceholder.

    This is used to check if a value was provided or if the default should be used.
    """
    if first_item is not None and not isinstance(first_item, DefaultPlaceholder):
        return first_item
    return (
        first_item
        if isinstance(first_item, DefaultPlaceholder)
        else DefaultPlaceholder(default_value)
    )
