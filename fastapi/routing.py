import asyncio
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import (
    get_body_field,
    get_dependant,
    get_parameterless_sub_dependant,
    solve_dependencies,
)
from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig, BaseModel, Schema
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.fields import Field
from pydantic.utils import lenient_issubclass
from starlette import routing
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import compile_path, get_name, request_response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


def serialize_response(*, field: Field = None, response: Response) -> Any:
    encoded = jsonable_encoder(response)
    if field:
        errors = []
        value, errors_ = field.validate(encoded, {}, loc=("response",))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        if errors:
            raise ValidationError(errors)
        return jsonable_encoder(value)
    else:
        return encoded


def get_app(
    dependant: Dependant,
    body_field: Field = None,
    status_code: int = 200,
    response_class: Type[Response] = JSONResponse,
    response_field: Field = None,
) -> Callable:
    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = asyncio.iscoroutinefunction(dependant.call)
    is_body_form = body_field and isinstance(body_field.schema, params.Form)

    async def app(request: Request) -> Response:
        try:
            body = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        body = await request.json()
        except Exception as e:
            logging.error(f"Error getting request body: {e}")
            raise HTTPException(
                status_code=400, detail="There was an error parsing the body"
            ) from e
        values, errors, background_tasks = await solve_dependencies(
            request=request, dependant=dependant, body=body
        )
        if errors:
            errors_out = ValidationError(errors)
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
            )
        else:
            assert dependant.call is not None, "dependant.call must be a function"
            if is_coroutine:
                raw_response = await dependant.call(**values)
            else:
                raw_response = await run_in_threadpool(dependant.call, **values)
            if isinstance(raw_response, Response):
                if raw_response.background is None:
                    raw_response.background = background_tasks
                return raw_response
            response_data = serialize_response(
                field=response_field, response=raw_response
            )
            return response_class(
                content=response_data,
                status_code=status_code,
                background=background_tasks,
            )

    return app


class APIRoute(routing.Route):
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        name: str = None,
        methods: List[str] = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
    ) -> None:
        assert path.startswith("/"), "Routed paths must always start with '/'"
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.response_model = response_model
        if self.response_model:
            assert lenient_issubclass(
                response_class, JSONResponse
            ), "To declare a type the response must be a JSON response"
            response_name = "Response_" + self.name
            self.response_field: Optional[Field] = Field(
                name=response_name,
                type_=self.response_model,
                class_validators={},
                default=None,
                required=False,
                model_config=BaseConfig,
                schema=Schema(None),
            )
        else:
            self.response_field = None
        self.status_code = status_code
        self.tags = tags or []
        self.dependencies = dependencies or []
        self.summary = summary
        self.description = description or inspect.cleandoc(self.endpoint.__doc__ or "")
        self.response_description = response_description
        self.responses = responses or {}
        response_fields = {}
        for additional_status_code, response in self.responses.items():
            assert isinstance(response, dict), "An additional response must be a dict"
            model = response.get("model")
            if model:
                assert lenient_issubclass(
                    model, BaseModel
                ), "A response model must be a Pydantic model"
                response_name = f"Response_{additional_status_code}_{self.name}"
                response_field = Field(
                    name=response_name,
                    type_=model,
                    class_validators=None,
                    default=None,
                    required=False,
                    model_config=BaseConfig,
                    schema=Schema(None),
                )
                response_fields[additional_status_code] = response_field
        if response_fields:
            self.response_fields: Dict[Union[int, str], Field] = response_fields
        else:
            self.response_fields = {}
        self.deprecated = deprecated
        if methods is None:
            methods = ["GET"]
        self.methods = methods
        self.operation_id = operation_id
        self.include_in_schema = include_in_schema
        self.response_class = response_class

        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        assert inspect.isfunction(endpoint) or inspect.ismethod(
            endpoint
        ), f"An endpoint must be a function or method"
        self.dependant = get_dependant(path=path, call=self.endpoint)
        for depends in self.dependencies[::-1]:
            self.dependant.dependencies.insert(
                0, get_parameterless_sub_dependant(depends=depends, path=path)
            )
        self.body_field = get_body_field(dependant=self.dependant, name=self.name)
        self.app = request_response(
            get_app(
                dependant=self.dependant,
                body_field=self.body_field,
                status_code=self.status_code,
                response_class=self.response_class,
                response_field=self.response_field,
            )
        )


class APIRouter(routing.Router):
    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        methods: List[str] = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> None:
        route = APIRoute(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )
        self.routes.append(route)

    def api_route(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        methods: List[str] = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_api_route(
                path,
                func,
                response_model=response_model,
                status_code=status_code,
                tags=tags or [],
                dependencies=dependencies or [],
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses or {},
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                include_in_schema=include_in_schema,
                response_class=response_class,
                name=name,
            )
            return func

        return decorator

    def include_router(
        self,
        router: "APIRouter",
        *,
        prefix: str = "",
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
    ) -> None:
        if prefix:
            assert prefix.startswith("/"), "A path prefix must start with '/'"
            assert not prefix.endswith(
                "/"
            ), "A path prefix must not end with '/', as the routes will start with '/'"
        if responses is None:
            responses = {}
        for route in router.routes:
            if isinstance(route, APIRoute):
                combined_responses = {**responses, **route.responses}
                self.add_api_route(
                    prefix + route.path,
                    route.endpoint,
                    response_model=route.response_model,
                    status_code=route.status_code,
                    tags=(route.tags or []) + (tags or []),
                    dependencies=(dependencies or []) + (route.dependencies or []),
                    summary=route.summary,
                    description=route.description,
                    response_description=route.response_description,
                    responses=combined_responses,
                    deprecated=route.deprecated,
                    methods=route.methods,
                    operation_id=route.operation_id,
                    include_in_schema=route.include_in_schema,
                    response_class=route.response_class,
                    name=route.name,
                )
            elif isinstance(route, routing.Route):
                self.add_route(
                    prefix + route.path,
                    route.endpoint,
                    methods=route.methods,
                    include_in_schema=route.include_in_schema,
                    name=route.name,
                )
            elif isinstance(route, routing.WebSocketRoute):
                self.add_websocket_route(
                    prefix + route.path, route.endpoint, name=route.name
                )

    def get(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["GET"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def put(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["PUT"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def post(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["POST"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def delete(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["DELETE"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def options(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["OPTIONS"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def head(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["HEAD"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def patch(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["PATCH"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )

    def trace(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: List[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        response_class: Type[Response] = JSONResponse,
        name: str = None,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies or [],
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["TRACE"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            response_class=response_class,
            name=name,
        )
