import typing
import inspect

from starlette.applications import Starlette
from starlette.middleware.lifespan import LifespanMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.exceptions import ExceptionMiddleware
from starlette.responses import JSONResponse, HTMLResponse, PlainTextResponse
from starlette.requests import Request
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from pydantic import BaseModel, BaseConfig, Schema
from pydantic.utils import lenient_issubclass
from pydantic.fields import Field
from pydantic.schema import (
    field_schema,
    get_flat_models_from_models,
    get_flat_models_from_fields,
    get_model_name_map,
    schema,
    model_process_schema,
)

from .routing import APIRouter, APIRoute, get_openapi_params, get_flat_dependant
from .pydantic_utils import jsonable_encoder


def docs(openapi_url):
    return HTMLResponse(
        """
    <! doctype html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="//unpkg.com/swagger-ui-dist@3/swagger-ui.css">
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
            
    const ui = SwaggerUIBundle({
        url: '""" + openapi_url + """',
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


class FastAPI(Starlette):
    def __init__(
        self,
        debug: bool = False,
        template_directory: str = None,
        title: str = "Fast API",
        description: str = "",
        version: str = "0.1.0",
        openapi_url: str = "/openapi.json",
        docs_url: str = "/docs",
        **extra: typing.Dict[str, typing.Any],
    ) -> None:
        self._debug = debug
        self.router = APIRouter()
        self.exception_middleware = ExceptionMiddleware(self.router, debug=debug)
        self.error_middleware = ServerErrorMiddleware(
            self.exception_middleware, debug=debug
        )
        self.lifespan_middleware = LifespanMiddleware(self.error_middleware)
        self.schema_generator = None  # type: typing.Optional[BaseSchemaGenerator]
        self.template_env = self.load_template_env(template_directory)

        self.title = title
        self.description = description
        self.version = version
        self.openapi_url = openapi_url
        self.docs_url = docs_url
        self.extra = extra

        self.openapi_version = "3.0.2"

        if self.openapi_url:
            assert self.title, "A title must be provided for OpenAPI, e.g.: 'My API'"
            assert self.version, "A version must be provided for OpenAPI, e.g.: '2.1.0'"

        if self.docs_url:
            assert self.openapi_url, "The openapi_url is required for the docs"

        self.add_route(
            self.openapi_url,
            lambda req: JSONResponse(self.openapi()),
            include_in_schema=False,
        )
        self.add_route(self.docs_url, lambda r: docs(self.openapi_url), include_in_schema=False)

    def add_api_route(
        self,
        path: str,
        endpoint: typing.Callable,
        methods: typing.List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> None:
        self.router.add_api_route(
            path,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def api_route(
        self,
        path: str,
        methods: typing.List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> typing.Callable:
        def decorator(func: typing.Callable) -> typing.Callable:
            self.router.add_api_route(
                path,
                func,
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
                tags=tags,
                summary=summary,
                description=description,
                operation_id=operation_id,
                deprecated=deprecated,
                response_type=response_type,
                response_description=response_description,
                response_code=response_code,
                response_wrapper=response_wrapper,
            )
            return func

        return decorator

    def get(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.get(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def put(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.put(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def post(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.post(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def delete(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.delete(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def options(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.options(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def head(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.head(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def patch(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.patch(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def trace(
        self,
        path: str,
        name: str = None,
        include_in_schema: bool = True,
        tags: typing.List[str] = [],
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: typing.Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.router.trace(
            path=path,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags,
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )

    def openapi(self):
        info = {"title": self.title, "version": self.version}
        if self.description:
            info["description"] = self.description
        output = {"openapi": self.openapi_version, "info": info}
        components = {}
        paths = {}
        methods_with_body = set(("POST", "PUT"))
        body_fields_from_routes = []
        responses_from_routes = []
        ref_prefix = "#/components/schemas/"
        for route in self.routes:
            route: APIRoute
            if route.include_in_schema and isinstance(route, APIRoute):
                if route.request_body:
                    assert isinstance(
                        route.request_body, Field
                    ), "A request body must be a Pydantic BaseModel or Field"
                    body_fields_from_routes.append(route.request_body)
                if route.response_field:
                    responses_from_routes.append(route.response_field)
        flat_models = get_flat_models_from_fields(
            body_fields_from_routes + responses_from_routes
        )
        model_name_map = get_model_name_map(flat_models)
        definitions = {}
        for model in flat_models:
            m_schema, m_definitions = model_process_schema(
                model, model_name_map=model_name_map, ref_prefix=ref_prefix
            )
            definitions.update(m_definitions)
            model_name = model_name_map[model]
            definitions[model_name] = m_schema
        validation_error_definition = {
            "title": "ValidationError",
            "type": "object",
            "properties": {
                "loc": {
                    "title": "Location",
                    "type": "array",
                    "items": {"type": "string"},
                },
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
                    "items": {"$ref": ref_prefix + "ValidationError"},
                }
            },
        }
        for route in self.routes:
            route: APIRoute
            if route.include_in_schema and isinstance(route, APIRoute):
                path = paths.get(route.path, {})
                for method in route.methods:
                    operation = {}
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
                    for security_scheme in flat_dependant.security_schemes:
                        security_definition = jsonable_encoder(security_scheme, exclude=("scheme_name",), by_alias=True, include_none=False)
                        security_name = getattr(security_scheme, "scheme_name", None) or security_scheme.__class__.__name__
                        security_definitions[security_name] = security_definition
                    if security_definitions:
                        components.setdefault("securitySchemes", {}).update(security_definitions)
                        operation["security"] = [{name: []} for name in security_definitions]
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
                    if method in methods_with_body:
                        request_body = getattr(route, "request_body", None)
                        if request_body:
                            assert isinstance(request_body, Field)
                            body_schema, _ = field_schema(
                                request_body,
                                model_name_map=model_name_map,
                                ref_prefix=ref_prefix,
                            )
                            required = request_body.required
                            request_body_oai = {}
                            if required:
                                request_body_oai["required"] = required
                            request_body_oai["content"] = {
                                "application/json": {"schema": body_schema}
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
                                ref_prefix=ref_prefix,
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
                    if all_route_params or getattr(route, "request_body", None):
                        operation["responses"][str(HTTP_422_UNPROCESSABLE_ENTITY)] = {
                            "description": "Validation Error",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": ref_prefix + "HTTPValidationError"
                                    }
                                }
                            },
                        }
                    path[method.lower()] = operation
                paths[route.path] = path
        if definitions:
            components.setdefault("schemas", {}).update(definitions)
        if components:
            output["components"] = components
        output["paths"] = paths
        return output
