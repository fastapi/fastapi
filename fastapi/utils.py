import re
from typing import Any, Dict, List, Sequence, Set, Type

from fastapi import routing
from fastapi.openapi.constants import REF_PREFIX
from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.schema import get_flat_models_from_fields, model_process_schema
from starlette.routing import BaseRoute


def get_flat_models_from_routes(
    routes: Sequence[Type[BaseRoute]]
) -> Set[Type[BaseModel]]:
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
        m_schema, m_definitions = model_process_schema(
            model, model_name_map=model_name_map, ref_prefix=REF_PREFIX
        )
        definitions.update(m_definitions)
        model_name = model_name_map[model]
        definitions[model_name] = m_schema
    return definitions


def get_path_param_names(path: str) -> Set[str]:
    return {item.strip("{}") for item in re.findall("{[^}]*}", path)}
