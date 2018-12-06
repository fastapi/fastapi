from typing import Any, Dict, Sequence, Type

from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import BaseRoute
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from fastapi import routing
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_flat_dependant
from fastapi.encoders import jsonable_encoder
from fastapi.openapi.constants import REF_PREFIX, METHODS_WITH_BODY
from fastapi.openapi.models import OpenAPI
from fastapi.params import Body
from fastapi.utils import get_flat_models_from_routes, get_model_definitions
from pydantic.fields import Field
from pydantic.schema import field_schema, get_model_name_map
from pydantic.utils import lenient_issubclass

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


def get_openapi_params(dependant: Dependant):
    flat_dependant = get_flat_dependant(dependant)
    return (
        flat_dependant.path_params
        + flat_dependant.query_params
        + flat_dependant.header_params
        + flat_dependant.cookie_params
    )

def get_openapi_path(*, route: BaseRoute, model_name_map: Dict[Type, str]):
    if not (route.include_in_schema and isinstance(route, routing.APIRoute)):
        return None
    path = {}
    security_schemes = {}
    definitions = {}
    for method in route.methods:
        operation: Dict[str, Any] = {}
        if route.tags:
            operation["tags"] = route.tags
        if route.summary:
            operation["summary"] = route.summary
        if route.description:
            operation["description"] = route.description
        if route.operation_id:
            operation["operationId"] = route.operation_id
        else:
            operation["operationId"] = route.name
        if route.deprecated:
            operation["deprecated"] = route.deprecated
        parameters = []
        flat_dependant = get_flat_dependant(route.dependant)
        security_definitions = {}
        for security_requirement in flat_dependant.security_requirements:
            security_definition = jsonable_encoder(
                security_requirement.security_scheme,
                exclude={"scheme_name"},
                by_alias=True,
                include_none=False,
            )
            security_name = (
                getattr(
                    security_requirement.security_scheme, "scheme_name", None
                )
                or security_requirement.security_scheme.__class__.__name__
            )
            security_definitions[security_name] = security_definition
            operation.setdefault("security", []).append(
                {security_name: security_requirement.scopes}
            )
        if security_definitions:
            security_schemes.update(
                security_definitions
            )
        all_route_params = get_openapi_params(route.dependant)
        for param in all_route_params:
            if "ValidationError" not in definitions:
                definitions["ValidationError"] = validation_error_definition
                definitions[
                    "HTTPValidationError"
                ] = validation_error_response_definition
            parameter = {
                "name": param.alias,
                "in": param.schema.in_.value,
                "required": param.required,
                "schema": field_schema(param, model_name_map={})[0],
            }
            if param.schema.description:
                parameter["description"] = param.schema.description
            if param.schema.deprecated:
                parameter["deprecated"] = param.schema.deprecated
            parameters.append(parameter)
        if parameters:
            operation["parameters"] = parameters
        if method in METHODS_WITH_BODY:
            body_field = route.body_field
            if body_field:
                assert isinstance(body_field, Field)
                body_schema, _ = field_schema(
                    body_field,
                    model_name_map=model_name_map,
                    ref_prefix=REF_PREFIX,
                )
                if isinstance(body_field.schema, Body):
                    request_media_type = body_field.schema.media_type
                else:
                    # Includes not declared media types (Schema)
                    request_media_type = "application/json"
                required = body_field.required
                request_body_oai = {}
                if required:
                    request_body_oai["required"] = required
                request_body_oai["content"] = {
                    request_media_type: {"schema": body_schema}
                }
                operation["requestBody"] = request_body_oai
        response_code = str(route.response_code)
        response_schema = {"type": "string"}
        if lenient_issubclass(route.response_wrapper, JSONResponse):
            response_media_type = "application/json"
            if route.response_field:
                response_schema, _ = field_schema(
                    route.response_field,
                    model_name_map=model_name_map,
                    ref_prefix=REF_PREFIX,
                )
            else:
                response_schema = {}
        elif lenient_issubclass(route.response_wrapper, HTMLResponse):
            response_media_type = "text/html"
        else:
            response_media_type = "text/plain"
        content = {response_media_type: {"schema": response_schema}}
        operation["responses"] = {
            response_code: {
                "description": route.response_description,
                "content": content,
            }
        }
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
    routes: Sequence[BaseRoute]
):
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
        result = get_openapi_path(route=route, model_name_map=model_name_map)
        if result:
            path, security_schemes, path_definitions = result
            if path:
                paths.setdefault(route.path, {}).update(path)
            if security_schemes:
                components.setdefault("securitySchemes", {}).update(security_schemes)
            if path_definitions:
                definitions.update(path_definitions)
    if definitions:
        components.setdefault("schemas", {}).update(definitions)
    if components:
        output["components"] = components
    output["paths"] = paths
    return jsonable_encoder(OpenAPI(**output), by_alias=True, include_none=False)


def get_swagger_ui_html(*, openapi_url: str, title: str):
    return HTMLResponse(
        """
    <! doctype html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css">
    <title>
    """ + title + """
    </title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
            
    const ui = SwaggerUIBundle({
        url: '"""
        + openapi_url
        + """',
        dom_id: '#swagger-ui',
        presets: [
        SwaggerUIBundle.presets.apis,
        SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
        layout: "BaseLayout"
 
    })
    </script>
    </body>
    </html>
    """,
        media_type="text/html",
    )


def get_redoc_html(*, openapi_url: str, title: str):
    return HTMLResponse(
        """
    <!DOCTYPE html>
<html>
  <head>
    <title>
    """ + title + """
    </title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">

    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
  </head>
  <body>
    <redoc spec-url='""" + openapi_url + """'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
  </body>
</html>
    """,
        media_type="text/html",
    )
