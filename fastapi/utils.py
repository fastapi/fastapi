import re
import warnings
from collections.abc import MutableMapping
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
)
from weakref import WeakKeyDictionary

import fastapi
from fastapi._compat import (
    BaseConfig,
    ModelField,
    PydanticSchemaGenerationError,
    Undefined,
    UndefinedType,
    Validator,
    annotation_is_pydantic_v1,
)
from fastapi.datastructures import DefaultPlaceholder, DefaultType
from fastapi.exceptions import FastAPIDeprecationWarning, PydanticV1NotSupportedError
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing_extensions import Literal

from ._compat import v2

if TYPE_CHECKING:  # pragma: nocover
    from .routing import APIRoute

# Cache for `create_cloned_field`
_CLONED_TYPES_CACHE: MutableMapping[type[BaseModel], type[BaseModel]] = (
    WeakKeyDictionary()
)


def is_body_allowed_for_status_code(status_code: Union[int, str, None]) -> bool:
    if status_code is None:
        return True
    # Ref: https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.1.0.md#patterned-fields-1
    if status_code in {
        "default",
        "1XX",
        "2XX",
        "3XX",
        "4XX",
        "5XX",
    }:
        return True
    current_status_code = int(status_code)
    return not (current_status_code < 200 or current_status_code in {204, 205, 304})


def get_path_param_names(path: str) -> set[str]:
    return set(re.findall("{(.*?)}", path))


_invalid_args_message = (
    "Invalid args for response field! Hint: "
    "check that {type_} is a valid Pydantic field type. "
    "If you are using a return type annotation that is not a valid Pydantic "
    "field (e.g. Union[Response, dict, None]) you can disable generating the "
    "response model from the type annotation with the path operation decorator "
    "parameter response_model=None. Read more: "
    "https://fastapi.tiangolo.com/tutorial/response-model/"
)


def create_model_field(
    name: str,
    type_: Any,
    class_validators: Optional[dict[str, Validator]] = None,
    default: Optional[Any] = Undefined,
    required: Union[bool, UndefinedType] = Undefined,
    model_config: Union[type[BaseConfig], None] = None,
    field_info: Optional[FieldInfo] = None,
    alias: Optional[str] = None,
    mode: Literal["validation", "serialization"] = "validation",
    version: Literal["1", "auto"] = "auto",
) -> ModelField:
    if annotation_is_pydantic_v1(type_):
        raise PydanticV1NotSupportedError(
            "pydantic.v1 models are no longer supported by FastAPI."
            f" Please update the response model {type_!r}."
        )
    class_validators = class_validators or {}

    field_info = field_info or FieldInfo(annotation=type_, default=default, alias=alias)
    kwargs = {"mode": mode, "name": name, "field_info": field_info}
    try:
        return v2.ModelField(**kwargs)  # type: ignore[arg-type]
    except PydanticSchemaGenerationError:
        raise fastapi.exceptions.FastAPIError(
            _invalid_args_message.format(type_=type_)
        ) from None


def create_cloned_field(
    field: ModelField,
    *,
    cloned_types: Optional[MutableMapping[type[BaseModel], type[BaseModel]]] = None,
) -> ModelField:
    return field


def generate_operation_id_for_path(
    *, name: str, path: str, method: str
) -> str:  # pragma: nocover
    warnings.warn(
        message="fastapi.utils.generate_operation_id_for_path() was deprecated, "
        "it is not used internally, and will be removed soon",
        category=FastAPIDeprecationWarning,
        stacklevel=2,
    )
    operation_id = f"{name}{path}"
    operation_id = re.sub(r"\W", "_", operation_id)
    operation_id = f"{operation_id}_{method.lower()}"
    return operation_id


def generate_unique_id(route: "APIRoute") -> str:
    operation_id = f"{route.name}{route.path_format}"
    operation_id = re.sub(r"\W", "_", operation_id)
    assert route.methods
    operation_id = f"{operation_id}_{list(route.methods)[0].lower()}"
    return operation_id


def deep_dict_update(main_dict: dict[Any, Any], update_dict: dict[Any, Any]) -> None:
    for key, value in update_dict.items():
        if (
            key in main_dict
            and isinstance(main_dict[key], dict)
            and isinstance(value, dict)
        ):
            deep_dict_update(main_dict[key], value)
        elif (
            key in main_dict
            and isinstance(main_dict[key], list)
            and isinstance(update_dict[key], list)
        ):
            main_dict[key] = main_dict[key] + update_dict[key]
        else:
            main_dict[key] = value


def get_value_or_default(
    first_item: Union[DefaultPlaceholder, DefaultType],
    *extra_items: Union[DefaultPlaceholder, DefaultType],
) -> Union[DefaultPlaceholder, DefaultType]:
    """
    Pass items or `DefaultPlaceholder`s by descending priority.

    The first one to _not_ be a `DefaultPlaceholder` will be returned.

    Otherwise, the first item (a `DefaultPlaceholder`) will be returned.
    """
    items = (first_item,) + extra_items
    for item in items:
        if not isinstance(item, DefaultPlaceholder):
            return item
    return first_item
