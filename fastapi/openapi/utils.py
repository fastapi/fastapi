import http.client
from typing import Any, Dict, List, Optional, Sequence, Tuple, Type, cast

from fastapi import routing
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_flat_dependant
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.constants import METHODS_WITH_BODY, REF_PREFIX
from fastapi.openapi.models import OpenAPI
from fastapi.params import Body, Param
from fastapi.utils import (
    generate_operation_id_for_path,
    get_flat_models_from_routes,
    get_model_definitions,
)
from pydantic.fields import Field
from pydantic.schema import field_schema, get_model_name_map
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


def get_openapi_params(dependant: Dependant) -> List[Field]:
    flat_dependant = get_flat_dependant(dependant)
    return (
        flat_dependant.path_params
        + flat_dependant.query_params
        + flat_dependant.header_params
        + flat_dependant.cookie_params
    )


def get_openapi_security_definitions(flat_dependant: Dependant) -> Tuple[Dict, List]:
    security_definitions = {}
    operation_security = []
    for security_requirement in flat_dependant.security_requirements:
        security_definition = jsonable_encoder(
            security_requirement.security_scheme.model,
            by_alias=True,
            include_none=False,
        )
        security_name = security_requirement.security_scheme.scheme_name
        security_definitions[security_name] = security_definition
        operation_security.append({security_name: security_requirement.scopes})
    return security_definitions, operation_security


def get_openapi_operation_parameters(
    all_route_params: Sequence[Field]
) -> Tuple[Dict[str, Dict], List[Dict[str, Any]]]:
    definitions: Dict[str, Dict] = {}
    parameters = []
    for param in all_route_params:
        schema = param.schema
        schema = cast(Param, schema)
        if "ValidationError" not in definitions:
            definitions["ValidationError"] = validation_error_definition
            definitions["HTTPValidationError"] = validation_error_response_definition
        parameter = {
            "name": param.alias,
            "in": schema.in_.value,
            "required": param.required,
            "schema": field_schema(param, model_name_map={})[0],
        }
        if schema.description:
            parameter["description"] = schema.description
        if schema.deprecated:
            parameter["deprecated"] = schema.deprecated
        parameters.append(parameter)
    return definitions, parameters


def get_openapi_operation_request_body(
    *, body_field: Optional[Field], model_name_map: Dict[Type, str]
) -> Optional[Dict]:
    if not body_field:
        return None
    assert isinstance(body_field, Field)
    body_schema, _, _ = field_schema(
        body_field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
    )
    body_field.schema = cast(Body, body_field.schema)
    request_media_type = body_field.schema.media_type
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
    if route.include_in_schema:
        for method in route.methods:
            operation = get_openapi_operation_metadata(route=route, method=method)
            parameters: List[Dict] = []
            flat_dependant = get_flat_dependant(route.dependant)
            security_definitions, operation_security = get_openapi_security_definitions(
                flat_dependant=flat_dependant
            )
            if operation_security:
                operation.setdefault("security", []).extend(operation_security)
            if security_definitions:
                security_schemes.update(security_definitions)
            all_route_params = get_openapi_params(route.dependant)
            validation_definitions, operation_parameters = get_openapi_operation_parameters(
                all_route_params=all_route_params
            )
            definitions.update(validation_definitions)
            parameters.extend(operation_parameters)
            if parameters:
                operation["parameters"] = parameters
            if method in METHODS_WITH_BODY:
                request_body_oai = get_openapi_operation_request_body(
                    body_field=route.body_field, model_name_map=model_name_map
                )
                if request_body_oai:
                    operation["requestBody"] = request_body_oai
                    if "ValidationError" not in definitions:
                        definitions["ValidationError"] = validation_error_definition
                        definitions[
                            "HTTPValidationError"
                        ] = validation_error_response_definition
            if route.responses:
                for (additional_status_code, response) in route.responses.items():
                    assert isinstance(
                        response, dict
                    ), "An additional response must be a dict"
                    field = route.response_fields.get(additional_status_code)
                    if field:
                        response_schema, _, _ = field_schema(
                            field, model_name_map=model_name_map, ref_prefix=REF_PREFIX
                        )
                        response.setdefault("content", {}).setdefault(
                            "application/json", {}
                        )["schema"] = response_schema
                    status_text = http.client.responses.get(int(additional_status_code))
                    response.setdefault(
                        "description", status_text or "Additional Response"
                    )
                    operation.setdefault("responses", {})[
                        str(additional_status_code)
                    ] = response
            status_code = str(route.status_code)
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
            operation.setdefault("responses", {}).setdefault(status_code, {})[
                "description"
            ] = route.response_description
            operation.setdefault("responses", {}).setdefault(
                status_code, {}
            ).setdefault("content", {}).setdefault(route.response_class.media_type, {})[
                "schema"
            ] = response_schema
            if all_route_params or route.body_field:
                operation["responses"][str(HTTP_422_UNPROCESSABLE_ENTITY)] = {
                    "description": "Validation Error",
                    "content": {
                        "application/json": {
                            "schema": {"$ref": REF_PREFIX + "HTTPValidationError"}
                        }
                    },
                }
            path[method.lower()] = operation
    return path, security_schemes, definitions


def get_openapi(
    *,
    title: str,
    version: str,
    openapi_version: str = "3.0.2",
    description: str = None,
    routes: Sequence[BaseRoute],
    openapi_prefix: str = ""
) -> Dict:
    info = {"title": title, "version": version}
    if description:
        info["description"] = description
    output = {"openapi": openapi_version, "info": info}
    components: Dict[str, Dict] = {}
    paths: Dict[str, Dict] = {}
    flat_models = get_flat_models_from_routes(routes)
    model_name_map = get_model_name_map(flat_models)
    definitions = get_model_definitions(
        flat_models=flat_models, model_name_map=model_name_map
    )
    for route in routes:
        if isinstance(route, routing.APIRoute):
            result = get_openapi_path(route=route, model_name_map=model_name_map)
            if result:
                path, security_schemes, path_definitions = result
                if path:
                    paths.setdefault(openapi_prefix + route.path_format, {}).update(
                        path
                    )
                if security_schemes:
                    components.setdefault("securitySchemes", {}).update(
                        security_schemes
                    )
                if path_definitions:
                    definitions.update(path_definitions)
    if definitions:
        components.setdefault("schemas", {}).update(definitions)
    if components:
        output["components"] = components
    output["paths"] = paths
    return jsonable_encoder(OpenAPI(**output), by_alias=True, include_none=False)
