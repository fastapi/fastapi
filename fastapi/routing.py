import asyncio
import inspect
import logging
from typing import Any, Callable, List, Optional, Type

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_body_field, get_dependant, solve_dependencies
from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig, BaseModel, Schema
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.fields import Field
from pydantic.utils import lenient_issubclass
from starlette import routing
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.formparsers import UploadFile
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import get_name, request_response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


def serialize_response(*, field: Field = None, response: Response) -> Any:
    if field:
        errors = []
        value, errors_ = field.validate(response, {}, loc=("response",))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        if errors:
            raise ValidationError(errors)
        return jsonable_encoder(value)
    else:
        return jsonable_encoder(response)


def get_app(
    dependant: Dependant,
    body_field: Field = None,
    status_code: int = 200,
    content_type: Type[Response] = JSONResponse,
    response_field: Field = None,
) -> Callable:
    assert dependant.call is not None, "dependant.call must me a function"
    is_coroutine = asyncio.iscoroutinefunction(dependant.call)
    is_body_form = body_field and isinstance(body_field.schema, params.Form)

    async def app(request: Request) -> Response:
        try:
            body = None
            if body_field:
                if is_body_form:
                    raw_body = await request.form()
                    body = {}
                    for field, value in raw_body.items():
                        if isinstance(value, UploadFile):
                            body[field] = await value.read()
                        else:
                            body[field] = value
                else:
                    body = await request.json()
        except Exception:
            raise HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
        try:
            values, errors = await solve_dependencies(
                request=request, dependant=dependant, body=body
            )
        except Exception as e:
            logging.error("Error solving dependencies", e)
            raise HTTPException(status_code=400, detail="Error processing request")
        if errors:
            errors_out = ValidationError(errors)
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
            )
        else:
            assert dependant.call is not None, "dependant.call must me a function"
            if is_coroutine:
                raw_response = await dependant.call(**values)
            else:
                raw_response = await run_in_threadpool(dependant.call, **values)
            if isinstance(raw_response, Response):
                return raw_response
            if isinstance(raw_response, BaseModel):
                return content_type(
                    content=serialize_response(
                        field=response_field, response=raw_response
                    ),
                    status_code=status_code,
                )
            errors = []
            try:
                return content_type(
                    content=serialize_response(
                        field=response_field, response=raw_response
                    ),
                    status_code=status_code,
                )
            except Exception as e:
                errors.append(e)
            try:
                response = dict(raw_response)
                return content_type(
                    content=serialize_response(field=response_field, response=response),
                    status_code=status_code,
                )
            except Exception as e:
                errors.append(e)
            try:
                response = vars(raw_response)
                return content_type(
                    content=serialize_response(field=response_field, response=response),
                    status_code=status_code,
                )
            except Exception as e:
                errors.append(e)
                raise ValueError(errors)

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
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        methods: List[str] = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> None:
        assert path.startswith("/"), "Routed paths must always start with '/'"
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.response_model = response_model
        if self.response_model:
            assert lenient_issubclass(
                content_type, JSONResponse
            ), "To declare a type the response must be a JSON response"
            response_name = "Response_" + self.name
            self.response_field: Optional[Field] = Field(
                name=response_name,
                type_=self.response_model,
                class_validators=[],
                default=None,
                required=False,
                model_config=BaseConfig(),
                schema=Schema(None),
            )
        else:
            self.response_field = None
        self.status_code = status_code
        self.tags = tags or []
        self.summary = summary
        self.description = description or self.endpoint.__doc__
        self.response_description = response_description
        self.deprecated = deprecated
        if methods is None:
            methods = ["GET"]
        self.methods = methods
        self.operation_id = operation_id
        self.include_in_schema = include_in_schema
        self.content_type = content_type

        self.path_regex, self.path_format, self.param_convertors = self.compile_path(
            path
        )
        assert inspect.isfunction(endpoint) or inspect.ismethod(
            endpoint
        ), f"An endpoint must be a function or method"
        self.dependant = get_dependant(path=path, call=self.endpoint)
        self.body_field = get_body_field(dependant=self.dependant, name=self.name)
        self.app = request_response(
            get_app(
                dependant=self.dependant,
                body_field=self.body_field,
                status_code=self.status_code,
                content_type=self.content_type,
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
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        methods: List[str] = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> None:
        route = APIRoute(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=methods,
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )
        self.routes.append(route)

    def api_route(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        methods: List[str] = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_api_route(
                path,
                func,
                response_model=response_model,
                status_code=status_code,
                tags=tags or [],
                summary=summary,
                description=description,
                response_description=response_description,
                deprecated=deprecated,
                name=name,
                methods=methods,
                operation_id=operation_id,
                include_in_schema=include_in_schema,
                content_type=content_type,
            )
            return func

        return decorator

    def include_router(self, router: "APIRouter", *, prefix: str = "") -> None:
        if prefix:
            assert prefix.startswith("/"), "A path prefix must start with '/'"
            assert not prefix.endswith(
                "/"
            ), "A path prefix must not end with '/', as the routes will start with '/'"
        for route in router.routes:
            if isinstance(route, APIRoute):
                self.add_api_route(
                    prefix + route.path,
                    route.endpoint,
                    response_model=route.response_model,
                    status_code=route.status_code,
                    tags=route.tags or [],
                    summary=route.summary,
                    description=route.description,
                    response_description=route.response_description,
                    deprecated=route.deprecated,
                    name=route.name,
                    methods=route.methods,
                    operation_id=route.operation_id,
                    include_in_schema=route.include_in_schema,
                    content_type=route.content_type,
                )
            elif isinstance(route, routing.Route):
                self.add_route(
                    prefix + route.path,
                    route.endpoint,
                    methods=route.methods,
                    name=route.name,
                    include_in_schema=route.include_in_schema,
                )

    def get(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["GET"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def put(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["PUT"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def post(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["POST"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def delete(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["DELETE"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def options(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["OPTIONS"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def head(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["HEAD"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def patch(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["PATCH"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )

    def trace(
        self,
        path: str,
        *,
        response_model: Type[BaseModel] = None,
        status_code: int = 200,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        deprecated: bool = None,
        name: str = None,
        operation_id: str = None,
        include_in_schema: bool = True,
        content_type: Type[Response] = JSONResponse,
    ) -> Callable:
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            summary=summary,
            description=description,
            response_description=response_description,
            deprecated=deprecated,
            name=name,
            methods=["TRACE"],
            operation_id=operation_id,
            include_in_schema=include_in_schema,
            content_type=content_type,
        )
