import http.client
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Type, Union, cast

from fastapi import routing
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_flat_dependant, get_flat_params
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.constants import (
    METHODS_WITH_BODY,
    REF_PREFIX,
    STATUS_CODES_WITH_NO_BODY,
)
from fastapi.openapi.models import OpenAPI
from fastapi.params import Body, Param
from fastapi.utils import (
    deep_dict_update,
    generate_operation_id_for_path,
    get_model_definitions,
)
from pydantic import BaseModel
from pydantic.fields import ModelField
from pydantic.schema import (
    field_schema,
    get_flat_models_from_fields,
    get_model_name_map,
)
from pydantic.utils import lenient_issubclass
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

validation_error_definition = {
    "title": "ValidationError",
    "type": "object",
    "properties": {
        "loc": {"title": "Location", "type": "array", "items": {"type": "string"}},
        "msg": {"title": "Message", "type": "string"},
        "type": {"title": "Error Type", "type": "string"},
    },
    "required": ["loc", "msg", "type"],
}

validation_error_response_definition = {
    "title": "HTTPValidationError",
    "type": "object",
    "properties": {
        "detail": {
            "title": "Detail",
            "type": "array",
            "items": {"$ref": REF_PREFIX + "ValidationError"},
        }
    },
}

status_code_ranges: Dict[str, str] = {
    "1XX": "Information",
    "2XX": "Success",
    "3XX": "Redirection",
    "4XX": "Client Error",
    "5XX": "Server Error",
    "DEFAULT": "Default Response",
}


def get_openapi_security_definitions(flat_dependant: Dependant) -> Tuple[Dict, List]:
    security_definitions = {}
    operation_security = []
    for security_requirement in flat_dependant.security_requirements:
        security_definition = jsonable_encoder(
            security_requirement.security_scheme.model,
            by_alias=True,
            exclude_none=True,
        )
        security_name = security_requirement.security_scheme.scheme_name
        security_definitions[security_name] = security_definition
        operation_security.append({security_name: security_requirement.scopes})
    return security_definitions, operation_security


def get_openapi_operation_parameters(
    *,
    all_route_params: Sequence[ModelField],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> List[Dict[str, Any]]:
    parameters = []
    for param in all_route_params:
        field_info = param.field_info
        field_info = cast(Param, field_info)
        # ignore mypy error until enum schemas are released
        parameter = {
            "name": param.alias,
            "in": field_info.in_.value,
            "required": param.required,
            "schema": field_schema(
                param, model_name_map=model_name_map, ref_prefix=REF_PREFIX  # type: ignore
            )[0],
        }
        if field_info.description:
            parameter["description"] = field_info.description
        if field_info.deprecated:
            parameter["deprecated"] = field_info.deprecated
        parameters.append(parameter)
    return parameters


def get_openapi_operation_request_body(
    *,
    body_field: Optional[ModelField],
    model_name_map: Dict[Union[Type[BaseModel], Type[Enum]], str],
) -> Optional[Dict]:
    if not body_field:
        return None
    assert isinstance(body_field, ModelField)
    # ignore mypy error until enum schemas are released
    body_schema, _, _ = field_schema(
        body_field, model_name_map=model_name_map, ref_prefix=REF_PREFIX  # type: ignore
    )
    field_info = cast(Body, body_field.field_info)
    request_media_type = field_info.media_type
    required = body_field.required
    request_body_oai: Dict[str, Any] = {}
    if required:
        request_body_oai["required"] = required
    request_body_oai["content"] = {request_media_type: {"schema": body_schema}}
    return request_body_oai


def generate_operation_id(*, route: routing.APIRoute, method: str) -> str:
    if route.operation_id:
        return route.operation_id
    path: str = route.path_format
    return generate_operation_id_for_path(name=route.name, path=path, method=method)


def generate_operation_summary(*, route: routing.APIRoute, method: str) -> str:
    if route.summary:
        return route.summary
    return route.name.replace("_", " ").title()


def get_openapi_operation_metadata(*, route: routing.APIRoute, method: str) -> Dict:
    operation: Dict[str, Any] = {}
    if route.tags:
        operation["tags"] = route.tags
    operation["summary"] = generate_operation_summary(route=route, method=method)
    if route.description:
        operation["description"] = route.description
    operation["operationId"] = generate_operation_id(route=route, method=method)
    if route.deprecated:
        operation["deprecated"] = route.deprecated
    return operation


def get_openapi_path(
    *, route: routing.APIRoute, model_name_map: Dict[Type, str]
) -> Tuple[Dict, Dict, Dict]:
    path = {}
    security_schemes: Dict[str, Any] = {}
    definitions: Dict[str, Any] = {}
    assert route.methods is not None, "Methods must be a list"
    assert route.response_class, "A response class is needed to generate OpenAPI"
    route_response_media_type: Optional[str] = route.response_class.media_type
    if route.include_in_schema:
        for method in route.methods:
            operation = get_openapi_operation_metadata(route=route, method=method)
            parameters: List[Dict] = []
            flat_dependant = get_flat_dependant(route.dependant, skip_repeats=True)
            security_definitions, operation_security = get_openapi_security_definitions(
                flat_dependant=flat_dependant
            )
            if operation_security:
                operation.setdefault("security", []).extend(operation_security)
            if security_definitions:
                security_schemes.update(security_definitions)
            all_route_params = get_flat_params(route.dependant)
            operation_parameters = get_openapi_operation_parameters(
                all_route_params=all_route_params, model_name_map=model_name_map
            )
            parameters.extend(operation_parameters)
            if parameters:
                operation["parameters"] = list(
                    {param["name"]: param for param in parameters}.values()
                )
            if method in METHODS_WITH_BODY:
                request_body_oai = get_openapi_operation_request_body(
                    body_field=route.body_field, model_name_map=model_name_map
                )
                if request_body_oai:
                    operation["requestBody"] = request_body_oai
            if route.callbacks:
                callbacks = {}
                for callback in route.callbacks:
                    cb_path, cb_security_schemes, cb_definitions, = get_openapi_path(
                        route=callback, model_name_map=model_name_map
                    )
                    callbacks[callback.name] = {callback.path: cb_path}
                operation["callbacks"] = callbacks
            status_code = str(route.status_code)
            operation.setdefault("responses", {}).setdefault(status_code, {})[
                "description"
            ] = route.response_description
            if (
                route_response_media_type
                and route.status_code not in STATUS_CODES_WITH_NO_BODY
            ):
                response_schema = {"type": "string"}
                if lenient_issubclass(route.response_class, JSONResponse):
                    if route.response_field:
                        response_schema, _, _ = field_schema(
                            route.response_field,
                            model_name_map=model_name_map,
                            ref_prefix=REF_PREFIX,
                        )
                    else:
                        response_schema = {}
                operation.setdefault("responses", {}).setdefault(
                    status_code, {}
                ).setdefault("content", {}).setdefault(route_response_media_type, {})[
                    "schema"
                ] = response_schema
            if route.responses:
                operation_responses = operation.setdefault("responses", {})
                for (
                    additional_status_code,
                    additional_response,
                ) in route.responses.items():
                    process_response = additional_response.copy()
                    process_response.pop("model", None)
                    status_code_key = str(additional_status_code).upper()
                    if status_code_key == "DEFAULT":
                        status_code_key = "default"
                    openapi_response = operation_responses.setdefault(
                        status_code_key, {}
                    )
                    assert isinstance(
                        process_response, dict
                    ), "An additional response must be a dict"
                    field = route.response_fields.get(additional_status_code)
                    additional_field_schema: Optional[Dict[str, Any]] = None
                    if field:
                        additional_field_schema, _, _ = field_schema(
                            field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
                        )
                        media_type = route_response_media_type or "application/json"
                        additional_schema = (
                            process_response.setdefault("content", {})
                            .setdefault(media_type, {})
                            .setdefault("schema", {})
                        )
                        deep_dict_update(additional_schema, additional_field_schema)
                    status_text: Optional[str] = status_code_ranges.get(
                        str(additional_status_code).upper()
                    ) or http.client.responses.get(int(additional_status_code))
                    description = (
                        process_response.get("description")
                        or openapi_response.get("description")
                        or status_text
                        or "Additional Response"
                    )
                    deep_dict_update(openapi_response, process_response)
                    openapi_response["description"] = description
            http422 = str(HTTP_422_UNPROCESSABLE_ENTITY)
            if (all_route_params or route.body_field) and not any(
                [
                    status in operation["responses"]
                    for status in [http422, "4XX", "default"]
                ]
            ):
                operation["responses"][http422] = {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": REF_PREFIX + "HTTPValidationError"}
                        }
                    },
                }
                if "ValidationError" not in definitions:
                    definitions.update(
                        {
                            "ValidationError": validation_error_definition,
                            "HTTPValidationError": validation_error_response_definition,
                        }
                    )
            path[method.lower()] = operation
    return path, security_schemes, definitions


def get_flat_models_from_routes(
    routes: Sequence[BaseRoute],
) -> Set[Union[Type[BaseModel], Type[Enum]]]:
    body_fields_from_routes: List[ModelField] = []
    responses_from_routes: List[ModelField] = []
    request_fields_from_routes: List[ModelField] = []
    callback_flat_models: Set[Union[Type[BaseModel], Type[Enum]]] = set()
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
            params = get_flat_params(route.dependant)
            request_fields_from_routes.extend(params)

    flat_models = callback_flat_models | get_flat_models_from_fields(
        body_fields_from_routes + responses_from_routes + request_fields_from_routes,
        known_models=set(),
    )
    return flat_models


def get_openapi(
    *,
    title: str,
    version: str,
    openapi_version: str = "3.0.2",
    description: Optional[str] = None,
    routes: Sequence[BaseRoute],
    tags: Optional[List[Dict[str, Any]]] = None,
    servers: Optional[List[Dict[str, Union[str, Any]]]] = None,
) -> Dict:
    info = {"title": title, "version": version}
    if description:
        info["description"] = description
    output: Dict[str, Any] = {"openapi": openapi_version, "info": info}
    if servers:
        output["servers"] = servers
    components: Dict[str, Dict] = {}
    paths: Dict[str, Dict] = {}
    flat_models = get_flat_models_from_routes(routes)
    # ignore mypy error until enum schemas are released
    model_name_map = get_model_name_map(flat_models)  # type: ignore
    # ignore mypy error until enum schemas are released
    definitions = get_model_definitions(
        flat_models=flat_models, model_name_map=model_name_map  # type: ignore
    )
    for route in routes:
        if isinstance(route, routing.APIRoute):
            result = get_openapi_path(route=route, model_name_map=model_name_map)
            if result:
                path, security_schemes, path_definitions = result
                if path:
                    paths.setdefault(route.path_format, {}).update(path)
                if security_schemes:
                    components.setdefault("securitySchemes", {}).update(
                        security_schemes
                    )
                if path_definitions:
                    definitions.update(path_definitions)
    if definitions:
        components["schemas"] = {k: definitions[k] for k in sorted(definitions)}
    if components:
        output["components"] = components
    output["paths"] = paths
    if tags:
        output["tags"] = tags
    return jsonable_encoder(OpenAPI(**output), by_alias=True, exclude_none=True)
