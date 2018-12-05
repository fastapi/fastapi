import asyncio
import inspect
import re
import typing
from copy import deepcopy

from starlette import routing
from starlette.routing import get_name, request_response
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


from pydantic.fields import Field, Required
from pydantic.schema import get_annotation_from_schema
from pydantic import BaseConfig, BaseModel, create_model, Schema
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.errors import MissingError
from pydantic.utils import lenient_issubclass
from .pydantic_utils import jsonable_encoder

from fastapi import params
from fastapi.security.base import SecurityBase


param_supported_types = (str, int, float, bool)


class Dependant:
    def __init__(
        self,
        *,
        path_params: typing.List[Field] = None,
        query_params: typing.List[Field] = None,
        header_params: typing.List[Field] = None,
        cookie_params: typing.List[Field] = None,
        body_params: typing.List[Field] = None,
        dependencies: typing.List["Dependant"] = None,
        security_schemes: typing.List[Field] = None,
        name: str = None,
        call: typing.Callable = None,
        request_param_name: str = None,
    ) -> None:
        self.path_params: typing.List[Field] = path_params or []
        self.query_params: typing.List[Field] = query_params or []
        self.header_params: typing.List[Field] = header_params or []
        self.cookie_params: typing.List[Field] = cookie_params or []
        self.body_params: typing.List[Field] = body_params or []
        self.dependencies: typing.List[Dependant] = dependencies or []
        self.security_schemes: typing.List[Field] = security_schemes or []
        self.request_param_name = request_param_name
        self.name = name
        self.call: typing.Callable = call


def request_params_to_args(
    required_params: typing.List[Field], received_params: typing.Dict[str, typing.Any]
) -> typing.Tuple[typing.Dict[str, typing.Any], typing.List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        value = received_params.get(field.alias)
        if value is None:
            if field.required:
                errors.append(
                    ErrorWrapper(MissingError(), loc=field.alias, config=BaseConfig)
                )
            else:
                values[field.name] = deepcopy(field.default)
            continue
        v_, errors_ = field.validate(
            value, values, loc=(field.schema.in_.value, field.alias)
        )
        if isinstance(errors_, ErrorWrapper):
            errors_: ErrorWrapper
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors


def request_body_to_args(
    required_params: typing.List[Field], received_body: typing.Dict[str, typing.Any]
) -> typing.Tuple[typing.Dict[str, typing.Any], typing.List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        sub_key = getattr(field.schema, "sub_key", None)
        if len(required_params) == 1 and not sub_key:
            received_body = {field.alias: received_body}
        for field in required_params:
            value = received_body.get(field.alias)
            if value is None:
                if field.required:
                    errors.append(
                        ErrorWrapper(
                            MissingError(), loc=("body", field.alias), config=BaseConfig
                        )
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue

            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors_: ErrorWrapper
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors


def add_param_to_fields(
    *,
    param: inspect.Parameter,
    dependant: Dependant,
    default_schema=params.Param,
    force_type: params.ParamTypes = None,
):
    default_value = Required
    if not param.default == param.empty:
        default_value = param.default
    if isinstance(default_value, params.Param):
        schema = default_value
        default_value = schema.default
        if schema.in_ is None:
            schema.in_ = default_schema.in_
        if force_type:
            schema.in_ = force_type
    else:
        schema = default_schema(default_value)
    required = default_value == Required
    annotation = typing.Any
    if not param.annotation == param.empty:
        annotation = param.annotation
    annotation = get_annotation_from_schema(annotation, schema)
    Config = BaseConfig
    field = Field(
        name=param.name,
        type_=annotation,
        default=None if required else default_value,
        alias=schema.alias or param.name,
        required=required,
        model_config=Config,
        class_validators=[],
        schema=schema,
    )
    if schema.in_ == params.ParamTypes.path:
        dependant.path_params.append(field)
    elif schema.in_ == params.ParamTypes.query:
        dependant.query_params.append(field)
    elif schema.in_ == params.ParamTypes.header:
        dependant.header_params.append(field)
    else:
        assert (
            schema.in_ == params.ParamTypes.cookie
        ), f"non-body parameters must be in path, query, header or cookie: {param.name}"
        dependant.cookie_params.append(field)


def add_param_to_body_fields(*, param: inspect.Parameter, dependant: Dependant):
    default_value = Required
    if not param.default == param.empty:
        default_value = param.default
    if isinstance(default_value, Schema):
        schema = default_value
        default_value = schema.default
    else:
        schema = Schema(default_value)
    required = default_value == Required
    annotation = get_annotation_from_schema(param.annotation, schema)
    field = Field(
        name=param.name,
        type_=annotation,
        default=None if required else default_value,
        alias=schema.alias or param.name,
        required=required,
        model_config=BaseConfig,
        class_validators=[],
        schema=schema,
    )
    dependant.body_params.append(field)


def get_sub_dependant(
    *, param: inspect.Parameter, path: str
):
    depends: params.Depends = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    assert callable(dependency)
    sub_dependant = get_dependant(path=path, call=dependency, name=param.name)
    if isinstance(dependency, SecurityBase):
        sub_dependant.security_schemes.append(dependency)
    return sub_dependant


def get_flat_dependant(dependant: Dependant):
    flat_dependant = Dependant(
        path_params=dependant.path_params.copy(),
        query_params=dependant.query_params.copy(),
        header_params=dependant.header_params.copy(),
        cookie_params=dependant.cookie_params.copy(),
        body_params=dependant.body_params.copy(),
        security_schemes=dependant.security_schemes.copy(),
    )
    for sub_dependant in dependant.dependencies:
        if sub_dependant is dependant:
            raise ValueError("recursion", dependant.dependencies)
        flat_sub = get_flat_dependant(sub_dependant)
        flat_dependant.path_params.extend(flat_sub.path_params)
        flat_dependant.query_params.extend(flat_sub.query_params)
        flat_dependant.header_params.extend(flat_sub.header_params)
        flat_dependant.cookie_params.extend(flat_sub.cookie_params)
        flat_dependant.body_params.extend(flat_sub.body_params)
        flat_dependant.security_schemes.extend(flat_sub.security_schemes)
    return flat_dependant


def get_path_param_names(path: str):
    return {item.strip("{}") for item in re.findall("{[^}]*}", path)}


def get_dependant(*, path: str, call: typing.Callable, name: str = None):
    path_param_names = get_path_param_names(path)
    endpoint_signature = inspect.signature(call)
    signature_params = endpoint_signature.parameters
    dependant = Dependant(call=call, name=name)
    for param_name in signature_params:
        param = signature_params[param_name]
        if isinstance(param.default, params.Depends):
            sub_dependant = get_sub_dependant(param=param, path=path)
            dependant.dependencies.append(sub_dependant)
    for param_name in signature_params:
        param = signature_params[param_name]
        if (
            (param.default == param.empty) or isinstance(param.default, params.Path)
        ) and (param_name in path_param_names):
            assert lenient_issubclass(
                param.annotation, param_supported_types
            ), f"Path params must be of type str, int, float or boot: {param}"
            param = signature_params[param_name]
            add_param_to_fields(
                param=param,
                dependant=dependant,
                default_schema=params.Path,
                force_type=params.ParamTypes.path,
            )
        elif (param.default == param.empty or param.default is None) and (
            param.annotation == param.empty
            or lenient_issubclass(param.annotation, param_supported_types)
        ):
            add_param_to_fields(
                param=param, dependant=dependant, default_schema=params.Query
            )
        elif isinstance(param.default, params.Param):
            if param.annotation != param.empty:
                assert lenient_issubclass(
                    param.annotation, param_supported_types
                ), f"Parameters for Path, Query, Header and Cookies must be of type str, int, float or bool: {param}"
            add_param_to_fields(
                param=param, dependant=dependant, default_schema=params.Query
            )
        elif lenient_issubclass(param.annotation, Request):
            dependant.request_param_name = param_name
        elif not isinstance(param.default, params.Depends):
            add_param_to_body_fields(param=param, dependant=dependant)
    return dependant


def is_coroutine_callable(call: typing.Callable):
    if inspect.isfunction(call):
        return asyncio.iscoroutinefunction(call)
    elif inspect.isclass(call):
        return False
    else:
        call = getattr(call, "__call__", None)
        if not call:
            return False
        else:
            return asyncio.iscoroutinefunction(call)


async def solve_dependencies(*, request: Request, dependant: Dependant):
    values = {}
    errors = []
    for sub_dependant in dependant.dependencies:
        sub_values, sub_errors = await solve_dependencies(
            request=request, dependant=sub_dependant
        )
        if sub_errors:
            return {}, errors
        if is_coroutine_callable(sub_dependant.call):
            solved = await sub_dependant.call(**sub_values)
        else:
            solved = await run_in_threadpool(sub_dependant.call, **sub_values)
        values[sub_dependant.name] = solved
    path_values, path_errors = request_params_to_args(
        dependant.path_params, request.path_params
    )
    query_values, query_errors = request_params_to_args(
        dependant.query_params, request.query_params
    )
    header_values, header_errors = request_params_to_args(
        dependant.header_params, request.headers
    )
    cookie_values, cookie_errors = request_params_to_args(
        dependant.cookie_params, request.cookies
    )
    values.update(path_values)
    values.update(query_values)
    values.update(header_values)
    values.update(cookie_values)
    errors = path_errors + query_errors + header_errors + cookie_errors
    if dependant.body_params:
        body = await request.json()
        body_values, body_errors = request_body_to_args(dependant.body_params, body)
        values.update(body_values)
        errors.extend(body_errors)
    if dependant.request_param_name:
        values[dependant.request_param_name] = request
    return values, errors


def get_app(dependant: Dependant):
    is_coroutine = asyncio.iscoroutinefunction(dependant.call)

    async def app(request: Request) -> Response:
        values, errors = await solve_dependencies(request=request, dependant=dependant)
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
            else:
                return JSONResponse(content=jsonable_encoder(raw_response))
    return app


def get_openapi_params(dependant: Dependant):
    flat_dependant = get_flat_dependant(dependant)
    return (
        flat_dependant.path_params
        + flat_dependant.query_params
        + flat_dependant.header_params
        + flat_dependant.cookie_params
    )


class APIRoute(routing.Route):
    def __init__(
        self,
        path: str,
        endpoint: typing.Callable,
        *,
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
        self.tags = tags
        self.summary = summary
        self.description = description
        self.operation_id = operation_id
        self.deprecated = deprecated
        self.request_body: typing.Union[BaseModel, Field, None] = None
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
        # flat_dependant = get_flat_dependant(self.dependant)
        # path_param_names = get_path_param_names(path)
        # for path_param in path_param_names:
        #     assert path_param in {
        #         f.alias for f in flat_dependant.path_params
        #     }, f"Path parameter must be defined as a function parameter or be defined by a dependency: {path_param}"

        if self.dependant.body_params:
            first_param = self.dependant.body_params[0]
            sub_key = getattr(first_param.schema, "sub_key", None)
            if len(self.dependant.body_params) == 1 and not sub_key:
                self.request_body = first_param
            else:
                model_name = "Body_" + self.name
                BodyModel = create_model(model_name)
                for f in self.dependant.body_params:
                    BodyModel.__fields__[f.name] = f
                required = any(True for f in self.dependant.body_params if f.required)
                field = Field(
                    name="body",
                    type_=BodyModel,
                    default=None,
                    required=required,
                    model_config=BaseConfig,
                    class_validators=[],
                    alias="body",
                    schema=Schema(None),
                )
                self.request_body = field

        self.app = request_response(get_app(dependant=self.dependant))


class APIRouter(routing.Router):
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
        route = APIRoute(
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
        self.routes.append(route)

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
            self.add_api_route(
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
        return self.api_route(
            path=path,
            methods=["GET"],
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
        return self.api_route(
            path=path,
            methods=["PUT"],
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
        return self.api_route(
            path=path,
            methods=["POST"],
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
        return self.api_route(
            path=path,
            methods=["DELETE"],
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
        return self.api_route(
            path=path,
            methods=["OPTIONS"],
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
        return self.api_route(
            path=path,
            methods=["HEAD"],
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
        return self.api_route(
            path=path,
            methods=["PATCH"],
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
        return self.api_route(
            path=path,
            methods=["TRACE"],
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
