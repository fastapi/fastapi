import re
from typing import Dict, Sequence, Set, Type

from starlette.routing import BaseRoute

from fastapi import routing
from fastapi.openapi.constants import REF_PREFIX
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.schema import get_flat_models_from_fields, model_process_schema


def get_flat_models_from_routes(routes: Sequence[BaseRoute]):
    body_fields_from_routes = []
    responses_from_routes = []
    for route in routes:
        if route.include_in_schema and isinstance(route, routing.APIRoute):
            if route.body_field:
                assert isinstance(
                    route.body_field, Field
                ), "A request body must be a Pydantic Field"
                body_fields_from_routes.append(route.body_field)
            if route.response_field:
                responses_from_routes.append(route.response_field)
    flat_models = get_flat_models_from_fields(
        body_fields_from_routes + responses_from_routes
    )
    return flat_models


def get_model_definitions(
    *, flat_models: Set[Type[BaseModel]], model_name_map: Dict[Type[BaseModel], str]
):
    definitions: Dict[str, Dict] = {}
    for model in flat_models:
        m_schema, m_definitions = model_process_schema(
            model, model_name_map=model_name_map, ref_prefix=REF_PREFIX
        )
        definitions.update(m_definitions)
        model_name = model_name_map[model]
        definitions[model_name] = m_schema
    return definitions


def get_path_param_names(path: str):
    return {item.strip("{}") for item in re.findall("{[^}]*}", path)}
