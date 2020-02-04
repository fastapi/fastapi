import re
from dataclasses import is_dataclass
from typing import Any, Dict, List, Sequence, Set, Type, cast

from fastapi import routing
from fastapi.logger import logger
from fastapi.openapi.constants import REF_PREFIX
from pydantic import BaseConfig, BaseModel, create_model
from pydantic.schema import get_flat_models_from_fields, model_process_schema
from pydantic.utils import lenient_issubclass
from starlette.routing import BaseRoute

try:
    from pydantic.fields import FieldInfo, ModelField

    PYDANTIC_1 = True
except ImportError:  # pragma: nocover
    # TODO: remove when removing support for Pydantic < 1.0.0
    from pydantic.fields import Field as ModelField  # type: ignore
    from pydantic import Schema as FieldInfo  # type: ignore

    logger.warning(
        "Pydantic versions < 1.0.0 are deprecated in FastAPI and support will be "
        "removed soon."
    )
    PYDANTIC_1 = False


# TODO: remove when removing support for Pydantic < 1.0.0
def get_field_info(field: ModelField) -> FieldInfo:
    if PYDANTIC_1:
        return field.field_info  # type: ignore
    else:
        return field.schema  # type: ignore  # pragma: nocover


# TODO: remove when removing support for Pydantic < 1.0.0
def warning_response_model_skip_defaults_deprecated() -> None:
    logger.warning(  # pragma: nocover
        "response_model_skip_defaults has been deprecated in favor of "
        "response_model_exclude_unset to keep in line with Pydantic v1, support for "
        "it will be removed soon."
    )


def get_flat_models_from_routes(routes: Sequence[BaseRoute]) -> Set[Type[BaseModel]]:
    body_fields_from_routes: List[ModelField] = []
    responses_from_routes: List[ModelField] = []
    callback_flat_models: Set[Type[BaseModel]] = set()
    for route in routes:
        if getattr(route, "include_in_schema", None) and isinstance(
            route, routing.APIRoute
        ):
            if route.body_field:
                assert isinstance(
                    route.body_field, ModelField
                ), "A request body must be a Pydantic Field"
                body_fields_from_routes.append(route.body_field)
            if route.response_field:
                responses_from_routes.append(route.response_field)
            if route.response_fields:
                responses_from_routes.extend(route.response_fields.values())
            if route.callbacks:
                callback_flat_models |= get_flat_models_from_routes(route.callbacks)
    flat_models = callback_flat_models | get_flat_models_from_fields(
        body_fields_from_routes + responses_from_routes, known_models=set()
    )
    return flat_models


def get_model_definitions(
    *, flat_models: Set[Type[BaseModel]], model_name_map: Dict[Type[BaseModel], str]
) -> Dict[str, Any]:
    definitions: Dict[str, Dict] = {}
    for model in flat_models:
        m_schema, m_definitions, m_nested_models = model_process_schema(
            model, model_name_map=model_name_map, ref_prefix=REF_PREFIX
        )
        definitions.update(m_definitions)
        model_name = model_name_map[model]
        definitions[model_name] = m_schema
    return definitions


def get_path_param_names(path: str) -> Set[str]:
    return {item.strip("{}") for item in re.findall("{[^}]*}", path)}


def create_cloned_field(field: ModelField) -> ModelField:
    original_type = field.type_
    if is_dataclass(original_type) and hasattr(original_type, "__pydantic_model__"):
        original_type = original_type.__pydantic_model__  # type: ignore
    use_type = original_type
    if lenient_issubclass(original_type, BaseModel):
        original_type = cast(Type[BaseModel], original_type)
        use_type = create_model(original_type.__name__, __base__=original_type)
        for f in original_type.__fields__.values():
            use_type.__fields__[f.name] = create_cloned_field(f)
    if PYDANTIC_1:
        new_field = ModelField(
            name=field.name,
            type_=use_type,
            class_validators={},
            default=None,
            required=False,
            model_config=BaseConfig,
            field_info=FieldInfo(None),
        )
    else:  # pragma: nocover
        new_field = ModelField(  # type: ignore
            name=field.name,
            type_=use_type,
            class_validators={},
            default=None,
            required=False,
            model_config=BaseConfig,
            schema=FieldInfo(None),
        )
    new_field.has_alias = field.has_alias
    new_field.alias = field.alias
    new_field.class_validators = field.class_validators
    new_field.default = field.default
    new_field.required = field.required
    new_field.model_config = field.model_config
    if PYDANTIC_1:
        new_field.field_info = field.field_info
    else:  # pragma: nocover
        new_field.schema = field.schema  # type: ignore
    new_field.allow_none = field.allow_none
    new_field.validate_always = field.validate_always
    if field.sub_fields:
        new_field.sub_fields = [
            create_cloned_field(sub_field) for sub_field in field.sub_fields
        ]
    if field.key_field:
        new_field.key_field = create_cloned_field(field.key_field)
    new_field.validators = field.validators
    if PYDANTIC_1:
        new_field.pre_validators = field.pre_validators
        new_field.post_validators = field.post_validators
    else:  # pragma: nocover
        new_field.whole_pre_validators = field.whole_pre_validators  # type: ignore
        new_field.whole_post_validators = field.whole_post_validators  # type: ignore
    new_field.parse_json = field.parse_json
    new_field.shape = field.shape
    try:
        new_field.populate_validators()
    except AttributeError:  # pragma: nocover
        # TODO: remove when removing support for Pydantic < 1.0.0
        new_field._populate_validators()  # type: ignore
    return new_field


def generate_operation_id_for_path(*, name: str, path: str, method: str) -> str:
    operation_id = name + path
    operation_id = re.sub("[^0-9a-zA-Z_]", "_", operation_id)
    operation_id = operation_id + "_" + method.lower()
    return operation_id
