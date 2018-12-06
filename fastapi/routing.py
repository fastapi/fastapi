import asyncio
import inspect
from typing import Callable, List, Type

from starlette import routing
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.formparsers import UploadFile
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import get_name, request_response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import get_body_field, get_dependant, solve_dependencies
from fastapi.encoders import jsonable_encoder
from pydantic import BaseConfig, BaseModel, Schema
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.fields import Field
from pydantic.utils import lenient_issubclass


def serialize_response(*, field: Field = None, response):
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
    response_code: str = 200,
    response_wrapper: Type[Response] = JSONResponse,
    response_field: Type[Field] = None,
):
    is_coroutine = dependant.call and asyncio.iscoroutinefunction(dependant.call)

    async def app(request: Request) -> Response:
        body = None
        if body_field:
            if isinstance(body_field.schema, params.Form):
                raw_body = await request.form()
                body = {}
                for field, value in raw_body.items():
                    if isinstance(value, UploadFile):
                        body[field] = await value.read()
                    else:
                        body[field] = value
            else:
                body = await request.json()
        values, errors = await solve_dependencies(
            request=request, dependant=dependant, body=body
        )
        if errors:
            errors_out = ValidationError(errors)
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=errors_out.errors()
            )
        else:
            if is_coroutine:
                raw_response = await dependant.call(**values)
            else:
                raw_response = await run_in_threadpool(dependant.call, **values)
            if isinstance(raw_response, Response):
                return raw_response
            if isinstance(raw_response, BaseModel):
                return response_wrapper(
                    content=jsonable_encoder(raw_response), status_code=response_code
                )
            errors = []
            try:
                return response_wrapper(
                    content=serialize_response(
                        field=response_field, response=raw_response
                    ),
                    status_code=response_code,
                )
            except Exception as e:
                errors.append(e)
            try:
                response = dict(raw_response)
                return response_wrapper(
                    content=serialize_response(field=response_field, response=response),
                    status_code=response_code,
                )
            except Exception as e:
                errors.append(e)
            try:
                response = vars(raw_response)
                return response_wrapper(
                    content=serialize_response(field=response_field, response=response),
                    status_code=response_code,
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
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> None:
        # TODO define how to read and provide security params, and how to have them globally too
        # TODO implement dependencies and injection
        # TODO refactor code structure
        # TODO create testing
        # TODO testing coverage
        assert path.startswith("/"), "Routed paths must always start '/'"
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.include_in_schema = include_in_schema
        self.tags = tags or []
        self.summary = summary
        self.description = description or self.endpoint.__doc__
        self.operation_id = operation_id
        self.deprecated = deprecated
        self.body_field: Field = None
        self.response_description = response_description
        self.response_code = response_code
        self.response_wrapper = response_wrapper
        self.response_field = None
        if response_type:
            assert lenient_issubclass(
                response_wrapper, JSONResponse
            ), "To declare a type the response must be a JSON response"
            self.response_type = response_type
            response_name = "Response_" + self.name
            self.response_field = Field(
                name=response_name,
                type_=self.response_type,
                class_validators=[],
                default=None,
                required=False,
                model_config=BaseConfig(),
                schema=Schema(None),
            )
        else:
            self.response_type = None
        if methods is None:
            methods = ["GET"]
        self.methods = methods
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
                response_code=self.response_code,
                response_wrapper=self.response_wrapper,
                response_field=self.response_field,
            )
        )


class APIRouter(routing.Router):
    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> None:
        route = APIRoute(
            path,
            endpoint=endpoint,
            methods=methods,
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )
        self.routes.append(route)

    def api_route(
        self,
        path: str,
        methods: List[str] = None,
        name: str = None,
        include_in_schema: bool = True,
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_api_route(
                path,
                func,
                methods=methods,
                name=name,
                include_in_schema=include_in_schema,
                tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["GET"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["PUT"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["POST"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["DELETE"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["OPTIONS"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["HEAD"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["PATCH"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
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
        tags: List[str] = None,
        summary: str = None,
        description: str = None,
        operation_id: str = None,
        deprecated: bool = None,
        response_type: Type = None,
        response_description: str = "Successful Response",
        response_code=200,
        response_wrapper=JSONResponse,
    ):
        return self.api_route(
            path=path,
            methods=["TRACE"],
            name=name,
            include_in_schema=include_in_schema,
            tags=tags or [],
            summary=summary,
            description=description,
            operation_id=operation_id,
            deprecated=deprecated,
            response_type=response_type,
            response_description=response_description,
            response_code=response_code,
            response_wrapper=response_wrapper,
        )
