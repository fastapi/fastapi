import re
from dataclasses import is_dataclass
from typing import Any, Dict, List, Sequence, Set, Type, cast

from fastapi import routing
from fastapi.openapi.constants import REF_PREFIX
from pydantic import BaseConfig, BaseModel, Schema, create_model
from pydantic.fields import Field
from pydantic.schema import get_flat_models_from_fields, model_process_schema
from pydantic.utils import lenient_issubclass
from starlette.routing import BaseRoute


def get_flat_models_from_routes(routes: Sequence[BaseRoute]) -> Set[Type[BaseModel]]:
    body_fields_from_routes: List[Field] = []
    responses_from_routes: List[Field] = []
    for route in routes:
        if getattr(route, "include_in_schema", None) and isinstance(
            route, routing.APIRoute
        ):
            if route.body_field:
                assert isinstance(
                    route.body_field, Field
                ), "A request body must be a Pydantic Field"
                body_fields_from_routes.append(route.body_field)
            if route.response_field:
                responses_from_routes.append(route.response_field)
            if route.response_fields:
                responses_from_routes.extend(route.response_fields.values())
    flat_models = get_flat_models_from_fields(
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


def create_cloned_field(field: Field) -> Field:
    original_type = field.type_
    if is_dataclass(original_type) and hasattr(original_type, "__pydantic_model__"):
        original_type = original_type.__pydantic_model__  # type: ignore
    use_type = original_type
    if lenient_issubclass(original_type, BaseModel):
        original_type = cast(Type[BaseModel], original_type)
        use_type = create_model(  # type: ignore
            original_type.__name__,
            __config__=original_type.__config__,
            __validators__=original_type.__validators__,
        )
        for f in original_type.__fields__.values():
            use_type.__fields__[f.name] = f
    new_field = Field(
        name=field.name,
        type_=use_type,
        class_validators={},
        default=None,
        required=False,
        model_config=BaseConfig,
        schema=Schema(None),
    )
    new_field.has_alias = field.has_alias
    new_field.alias = field.alias
    new_field.class_validators = field.class_validators
    new_field.default = field.default
    new_field.required = field.required
    new_field.model_config = field.model_config
    new_field.schema = field.schema
    new_field.allow_none = field.allow_none
    new_field.validate_always = field.validate_always
    if field.sub_fields:
        new_field.sub_fields = [
            create_cloned_field(sub_field) for sub_field in field.sub_fields
        ]
    if field.key_field:
        new_field.key_field = create_cloned_field(field.key_field)
    new_field.validators = field.validators
    new_field.whole_pre_validators = field.whole_pre_validators
    new_field.whole_post_validators = field.whole_post_validators
    new_field.parse_json = field.parse_json
    new_field.shape = field.shape
    new_field._populate_validators()
    return new_field


def generate_operation_id_for_path(*, name: str, path: str, method: str) -> str:
    operation_id = name + path
    operation_id = operation_id.replace("{", "_").replace("}", "_").replace("/", "_")
    operation_id = operation_id + "_" + method.lower()
    return operation_id
