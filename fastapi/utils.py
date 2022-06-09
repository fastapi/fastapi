import functools
import re
import warnings
from dataclasses import is_dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, Optional, Set, Type, Union, cast

import fastapi
from fastapi.datastructures import DefaultPlaceholder, DefaultType
from fastapi.openapi.constants import REF_PREFIX
from pydantic import BaseConfig, BaseModel, create_model
from pydantic.class_validators import Validator
from pydantic.fields import FieldInfo, ModelField, UndefinedType
from pydantic.schema import model_process_schema
from pydantic.utils import lenient_issubclass

if TYPE_CHECKING:  # pragma: nocover
    from .routing import APIRoute


def get_model_definitions(
    *,
    flat_models: Set[Union[Type[BaseModel], Type[Enum]]],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> Dict[str, Any]:
    definitions: Dict[str, Dict[str, Any]] = {}
    for model in flat_models:
        m_schema, m_definitions, m_nested_models = model_process_schema(
            model, model_name_map=model_name_map, ref_prefix=REF_PREFIX
        )
        definitions.update(m_definitions)
        model_name = model_name_map[model]
        definitions[model_name] = m_schema
    return definitions


def get_path_param_names(path: str) -> Set[str]:
    return set(re.findall("{(.*?)}", path))


def create_response_field(
    name: str,
    type_: Type[Any],
    class_validators: Optional[Dict[str, Validator]] = None,
    default: Optional[Any] = None,
    required: Union[bool, UndefinedType] = False,
    model_config: Type[BaseConfig] = BaseConfig,
    field_info: Optional[FieldInfo] = None,
    alias: Optional[str] = None,
) -> ModelField:
    """
    Create a new response field. Raises if type_ is invalid.
    """
    class_validators = class_validators or {}
    field_info = field_info or FieldInfo()

    response_field = functools.partial(
        ModelField,
        name=name,
        type_=type_,
        class_validators=class_validators,
        default=default,
        required=required,
        model_config=model_config,
        alias=alias,
    )

    try:
        return response_field(field_info=field_info)
    except RuntimeError:
        raise fastapi.exceptions.FastAPIError(
            f"Invalid args for response field! Hint: check that {type_} is a valid pydantic field type"
        )


def create_cloned_field(
    field: ModelField,
    *,
    cloned_types: Optional[Dict[Type[BaseModel], Type[BaseModel]]] = None,
) -> ModelField:
    # _cloned_types has already cloned types, to support recursive models
    if cloned_types is None:
        cloned_types = dict()
    original_type = field.type_
    if is_dataclass(original_type) and hasattr(original_type, "__pydantic_model__"):
        original_type = original_type.__pydantic_model__
    use_type = original_type
    if lenient_issubclass(original_type, BaseModel):
        original_type = cast(Type[BaseModel], original_type)
        use_type = cloned_types.get(original_type)
        if use_type is None:
            use_type = create_model(original_type.__name__, __base__=original_type)
            cloned_types[original_type] = use_type
            for f in original_type.__fields__.values():
                use_type.__fields__[f.name] = create_cloned_field(
                    f, cloned_types=cloned_types
                )
    new_field = create_response_field(name=field.name, type_=use_type)
    new_field.has_alias = field.has_alias
    new_field.alias = field.alias
    new_field.class_validators = field.class_validators
    new_field.default = field.default
    new_field.required = field.required
    new_field.model_config = field.model_config
    new_field.field_info = field.field_info
    new_field.allow_none = field.allow_none
    new_field.validate_always = field.validate_always
    if field.sub_fields:
        new_field.sub_fields = [
            create_cloned_field(sub_field, cloned_types=cloned_types)
            for sub_field in field.sub_fields
        ]
    if field.key_field:
        new_field.key_field = create_cloned_field(
            field.key_field, cloned_types=cloned_types
        )
    new_field.validators = field.validators
    new_field.pre_validators = field.pre_validators
    new_field.post_validators = field.post_validators
    new_field.parse_json = field.parse_json
    new_field.shape = field.shape
    new_field.populate_validators()
    return new_field


def generate_operation_id_for_path(
    *, name: str, path: str, method: str
) -> str:  # pragma: nocover
    warnings.warn(
        "fastapi.utils.generate_operation_id_for_path() was deprecated, "
        "it is not used internally, and will be removed soon",
        DeprecationWarning,
        stacklevel=2,
    )
    operation_id = name + path
    operation_id = re.sub("[^0-9a-zA-Z_]", "_", operation_id)
    operation_id = operation_id + "_" + method.lower()
    return operation_id


def generate_unique_id(route: "APIRoute") -> str:
    operation_id = route.name + route.path_format
    operation_id = re.sub("[^0-9a-zA-Z_]", "_", operation_id)
    assert route.methods
    operation_id = operation_id + "_" + list(route.methods)[0].lower()
    return operation_id


def deep_dict_update(main_dict: Dict[Any, Any], update_dict: Dict[Any, Any]) -> None:
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
