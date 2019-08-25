import asyncio
import inspect
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    cast,
)

from fastapi import params
from fastapi.dependencies.models import Dependant, SecurityRequirement
from fastapi.security.base import SecurityBase
from fastapi.security.oauth2 import OAuth2, SecurityScopes
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.utils import get_path_param_names
from pydantic import BaseConfig, BaseModel, Schema, create_model
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.fields import Field, Required, Shape
from pydantic.schema import get_annotation_from_schema
from pydantic.utils import lenient_issubclass
from starlette.background import BackgroundTasks
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import FormData, Headers, QueryParams, UploadFile
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket

sequence_shapes = {
    Shape.LIST,
    Shape.SET,
    Shape.TUPLE,
    Shape.SEQUENCE,
    Shape.TUPLE_ELLIPS,
}
sequence_types = (list, set, tuple)
sequence_shape_to_type = {
    Shape.LIST: list,
    Shape.SET: set,
    Shape.TUPLE: tuple,
    Shape.SEQUENCE: list,
    Shape.TUPLE_ELLIPS: list,
}


def get_param_sub_dependant(
    *, param: inspect.Parameter, path: str, security_scopes: List[str] = None
) -> Dependant:
    depends: params.Depends = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    return get_sub_dependant(
        depends=depends,
        dependency=dependency,
        path=path,
        name=param.name,
        security_scopes=security_scopes,
    )


def get_parameterless_sub_dependant(*, depends: params.Depends, path: str) -> Dependant:
    assert callable(
        depends.dependency
    ), "A parameter-less dependency must have a callable dependency"
    return get_sub_dependant(depends=depends, dependency=depends.dependency, path=path)


def get_sub_dependant(
    *,
    depends: params.Depends,
    dependency: Callable,
    path: str,
    name: str = None,
    security_scopes: List[str] = None,
) -> Dependant:
    security_requirement = None
    security_scopes = security_scopes or []
    if isinstance(depends, params.Security):
        dependency_scopes = depends.scopes
        security_scopes.extend(dependency_scopes)
    if isinstance(dependency, SecurityBase):
        use_scopes: List[str] = []
        if isinstance(dependency, (OAuth2, OpenIdConnect)):
            use_scopes = security_scopes
        security_requirement = SecurityRequirement(
            security_scheme=dependency, scopes=use_scopes
        )
    sub_dependant = get_dependant(
        path=path,
        call=dependency,
        name=name,
        security_scopes=security_scopes,
        use_cache=depends.use_cache,
    )
    if security_requirement:
        sub_dependant.security_requirements.append(security_requirement)
    sub_dependant.security_scopes = security_scopes
    return sub_dependant


CacheKey = Tuple[Optional[Callable], Tuple[str, ...]]


def get_flat_dependant(
    dependant: Dependant, *, skip_repeats: bool = False, visited: List[CacheKey] = None
) -> Dependant:
    if visited is None:
        visited = []
    visited.append(dependant.cache_key)

    flat_dependant = Dependant(
        path_params=dependant.path_params.copy(),
        query_params=dependant.query_params.copy(),
        header_params=dependant.header_params.copy(),
        cookie_params=dependant.cookie_params.copy(),
        body_params=dependant.body_params.copy(),
        security_schemes=dependant.security_requirements.copy(),
        use_cache=dependant.use_cache,
        path=dependant.path,
    )
    for sub_dependant in dependant.dependencies:
        if skip_repeats and sub_dependant.cache_key in visited:
            continue
        flat_sub = get_flat_dependant(
            sub_dependant, skip_repeats=skip_repeats, visited=visited
        )
        flat_dependant.path_params.extend(flat_sub.path_params)
        flat_dependant.query_params.extend(flat_sub.query_params)
        flat_dependant.header_params.extend(flat_sub.header_params)
        flat_dependant.cookie_params.extend(flat_sub.cookie_params)
        flat_dependant.body_params.extend(flat_sub.body_params)
        flat_dependant.security_requirements.extend(flat_sub.security_requirements)
    return flat_dependant


def is_scalar_field(field: Field) -> bool:
    if not (
        field.shape == Shape.SINGLETON
        and not lenient_issubclass(field.type_, BaseModel)
        and not lenient_issubclass(field.type_, sequence_types + (dict,))
        and not isinstance(field.schema, params.Body)
    ):
        return False
    if field.sub_fields:
        if not all(is_scalar_field(f) for f in field.sub_fields):
            return False
    return True


def is_scalar_sequence_field(field: Field) -> bool:
    if (field.shape in sequence_shapes) and not lenient_issubclass(
        field.type_, BaseModel
    ):
        if field.sub_fields is not None:
            for sub_field in field.sub_fields:
                if not is_scalar_field(sub_field):
                    return False
        return True
    if lenient_issubclass(field.type_, sequence_types):
        return True
    return False


def get_dependant(
    *,
    path: str,
    call: Callable,
    name: str = None,
    security_scopes: List[str] = None,
    use_cache: bool = True,
) -> Dependant:
    path_param_names = get_path_param_names(path)
    endpoint_signature = inspect.signature(call)
    signature_params = endpoint_signature.parameters
    dependant = Dependant(call=call, name=name, path=path, use_cache=use_cache)
    for param_name, param in signature_params.items():
        if isinstance(param.default, params.Depends):
            sub_dependant = get_param_sub_dependant(
                param=param, path=path, security_scopes=security_scopes
            )
            dependant.dependencies.append(sub_dependant)
    for param_name, param in signature_params.items():
        if isinstance(param.default, params.Depends):
            continue
        if add_non_field_param_to_dependency(param=param, dependant=dependant):
            continue
        param_field = get_param_field(param=param, default_schema=params.Query)
        if param_name in path_param_names:
            assert param.default == param.empty or isinstance(
                param.default, params.Path
            ), "Path params must have no defaults or use Path(...)"
            assert is_scalar_field(
                field=param_field
            ), f"Path params must be of one of the supported types"
            param_field = get_param_field(
                param=param,
                default_schema=params.Path,
                force_type=params.ParamTypes.path,
            )
            add_param_to_fields(field=param_field, dependant=dependant)
        elif is_scalar_field(field=param_field):
            add_param_to_fields(field=param_field, dependant=dependant)
        elif isinstance(
            param.default, (params.Query, params.Header)
        ) and is_scalar_sequence_field(param_field):
            add_param_to_fields(field=param_field, dependant=dependant)
        else:
            assert isinstance(
                param_field.schema, params.Body
            ), f"Param: {param_field.name} can only be a request body, using Body(...)"
            dependant.body_params.append(param_field)
    return dependant


def add_non_field_param_to_dependency(
    *, param: inspect.Parameter, dependant: Dependant
) -> Optional[bool]:
    if lenient_issubclass(param.annotation, Request):
        dependant.request_param_name = param.name
        return True
    elif lenient_issubclass(param.annotation, WebSocket):
        dependant.websocket_param_name = param.name
        return True
    elif lenient_issubclass(param.annotation, Response):
        dependant.response_param_name = param.name
        return True
    elif lenient_issubclass(param.annotation, BackgroundTasks):
        dependant.background_tasks_param_name = param.name
        return True
    elif lenient_issubclass(param.annotation, SecurityScopes):
        dependant.security_scopes_param_name = param.name
        return True
    return None


def get_param_field(
    *,
    param: inspect.Parameter,
    default_schema: Type[params.Param] = params.Param,
    force_type: params.ParamTypes = None,
) -> Field:
    default_value = Required
    had_schema = False
    if not param.default == param.empty:
        default_value = param.default
    if isinstance(default_value, Schema):
        had_schema = True
        schema = default_value
        default_value = schema.default
        if isinstance(schema, params.Param) and getattr(schema, "in_", None) is None:
            schema.in_ = default_schema.in_
        if force_type:
            schema.in_ = force_type  # type: ignore
    else:
        schema = default_schema(default_value)
    required = default_value == Required
    annotation: Any = Any
    if not param.annotation == param.empty:
        annotation = param.annotation
    annotation = get_annotation_from_schema(annotation, schema)
    if not schema.alias and getattr(schema, "convert_underscores", None):
        alias = param.name.replace("_", "-")
    else:
        alias = schema.alias or param.name
    field = Field(
        name=param.name,
        type_=annotation,
        default=None if required else default_value,
        alias=alias,
        required=required,
        model_config=BaseConfig,
        class_validators={},
        schema=schema,
    )
    if not had_schema and not is_scalar_field(field=field):
        field.schema = params.Body(schema.default)
    return field


def add_param_to_fields(*, field: Field, dependant: Dependant) -> None:
    field.schema = cast(params.Param, field.schema)
    if field.schema.in_ == params.ParamTypes.path:
        dependant.path_params.append(field)
    elif field.schema.in_ == params.ParamTypes.query:
        dependant.query_params.append(field)
    elif field.schema.in_ == params.ParamTypes.header:
        dependant.header_params.append(field)
    else:
        assert (
            field.schema.in_ == params.ParamTypes.cookie
        ), f"non-body parameters must be in path, query, header or cookie: {field.name}"
        dependant.cookie_params.append(field)


def is_coroutine_callable(call: Callable) -> bool:
    if inspect.isfunction(call):
        return asyncio.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    call = getattr(call, "__call__", None)
    return asyncio.iscoroutinefunction(call)


async def solve_dependencies(
    *,
    request: Union[Request, WebSocket],
    dependant: Dependant,
    body: Optional[Union[Dict[str, Any], FormData]] = None,
    background_tasks: BackgroundTasks = None,
    response: Response = None,
    dependency_overrides_provider: Any = None,
    dependency_cache: Dict[Tuple[Callable, Tuple[str]], Any] = None,
) -> Tuple[
    Dict[str, Any],
    List[ErrorWrapper],
    Optional[BackgroundTasks],
    Response,
    Dict[Tuple[Callable, Tuple[str]], Any],
]:
    values: Dict[str, Any] = {}
    errors: List[ErrorWrapper] = []
    response = response or Response(  # type: ignore
        content=None, status_code=None, headers=None, media_type=None, background=None
    )
    dependency_cache = dependency_cache or {}
    sub_dependant: Dependant
    for sub_dependant in dependant.dependencies:
        sub_dependant.call = cast(Callable, sub_dependant.call)
        sub_dependant.cache_key = cast(
            Tuple[Callable, Tuple[str]], sub_dependant.cache_key
        )
        call = sub_dependant.call
        use_sub_dependant = sub_dependant
        if (
            dependency_overrides_provider
            and dependency_overrides_provider.dependency_overrides
        ):
            original_call = sub_dependant.call
            call = getattr(
                dependency_overrides_provider, "dependency_overrides", {}
            ).get(original_call, original_call)
            use_path: str = sub_dependant.path  # type: ignore
            use_sub_dependant = get_dependant(
                path=use_path,
                call=call,
                name=sub_dependant.name,
                security_scopes=sub_dependant.security_scopes,
            )

        solved_result = await solve_dependencies(
            request=request,
            dependant=use_sub_dependant,
            body=body,
            background_tasks=background_tasks,
            response=response,
            dependency_overrides_provider=dependency_overrides_provider,
            dependency_cache=dependency_cache,
        )
        sub_values, sub_errors, background_tasks, sub_response, sub_dependency_cache = (
            solved_result
        )
        sub_response = cast(Response, sub_response)
        response.headers.raw.extend(sub_response.headers.raw)
        if sub_response.status_code:
            response.status_code = sub_response.status_code
        dependency_cache.update(sub_dependency_cache)
        if sub_errors:
            errors.extend(sub_errors)
            continue
        if sub_dependant.use_cache and sub_dependant.cache_key in dependency_cache:
            solved = dependency_cache[sub_dependant.cache_key]
        elif is_coroutine_callable(call):
            solved = await call(**sub_values)
        else:
            solved = await run_in_threadpool(call, **sub_values)
        if sub_dependant.name is not None:
            values[sub_dependant.name] = solved
        if sub_dependant.cache_key not in dependency_cache:
            dependency_cache[sub_dependant.cache_key] = solved
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
    errors += path_errors + query_errors + header_errors + cookie_errors
    if dependant.body_params:
        body_values, body_errors = await request_body_to_args(  # type: ignore # body_params checked above
            required_params=dependant.body_params, received_body=body
        )
        values.update(body_values)
        errors.extend(body_errors)
    if dependant.request_param_name and isinstance(request, Request):
        values[dependant.request_param_name] = request
    elif dependant.websocket_param_name and isinstance(request, WebSocket):
        values[dependant.websocket_param_name] = request
    if dependant.background_tasks_param_name:
        if background_tasks is None:
            background_tasks = BackgroundTasks()
        values[dependant.background_tasks_param_name] = background_tasks
    if dependant.response_param_name:
        values[dependant.response_param_name] = response
    if dependant.security_scopes_param_name:
        values[dependant.security_scopes_param_name] = SecurityScopes(
            scopes=dependant.security_scopes
        )
    return values, errors, background_tasks, response, dependency_cache


def request_params_to_args(
    required_params: Sequence[Field],
    received_params: Union[Mapping[str, Any], QueryParams, Headers],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        if is_scalar_sequence_field(field) and isinstance(
            received_params, (QueryParams, Headers)
        ):
            value = received_params.getlist(field.alias) or field.default
        else:
            value = received_params.get(field.alias)
        schema = field.schema
        assert isinstance(schema, params.Param), "Params must be subclasses of Param"
        if value is None:
            if field.required:
                errors.append(
                    ErrorWrapper(
                        MissingError(),
                        loc=(schema.in_.value, field.alias),
                        config=BaseConfig,
                    )
                )
            else:
                values[field.name] = deepcopy(field.default)
            continue
        v_, errors_ = field.validate(value, values, loc=(schema.in_.value, field.alias))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        else:
            values[field.name] = v_
    return values, errors


async def request_body_to_args(
    required_params: List[Field],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        embed = getattr(field.schema, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            value: Any = None
            if received_body is not None:
                if field.shape in sequence_shapes and isinstance(
                    received_body, FormData
                ):
                    value = received_body.getlist(field.alias)
                else:
                    value = received_body.get(field.alias)
            if (
                value is None
                or (isinstance(field.schema, params.Form) and value == "")
                or (
                    isinstance(field.schema, params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    errors.append(
                        ErrorWrapper(
                            MissingError(), loc=("body", field.alias), config=BaseConfig
                        )
                    )
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
                isinstance(field.schema, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field.schema, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
                awaitables = [sub_value.read() for sub_value in value]
                contents = await asyncio.gather(*awaitables)
                value = sequence_shape_to_type[field.shape](contents)
            v_, errors_ = field.validate(value, values, loc=("body", field.alias))
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors


def get_schema_compatible_field(*, field: Field) -> Field:
    out_field = field
    if lenient_issubclass(field.type_, UploadFile):
        use_type: type = bytes
        if field.shape in sequence_shapes:
            use_type = List[bytes]
        out_field = Field(
            name=field.name,
            type_=use_type,
            class_validators=field.class_validators,
            model_config=field.model_config,
            default=field.default,
            required=field.required,
            alias=field.alias,
            schema=field.schema,
        )
    return out_field


def get_body_field(*, dependant: Dependant, name: str) -> Optional[Field]:
    flat_dependant = get_flat_dependant(dependant)
    if not flat_dependant.body_params:
        return None
    first_param = flat_dependant.body_params[0]
    embed = getattr(first_param.schema, "embed", None)
    if len(flat_dependant.body_params) == 1 and not embed:
        return get_schema_compatible_field(field=first_param)
    model_name = "Body_" + name
    BodyModel = create_model(model_name)
    for f in flat_dependant.body_params:
        BodyModel.__fields__[f.name] = get_schema_compatible_field(field=f)
    required = any(True for f in flat_dependant.body_params if f.required)
    if any(isinstance(f.schema, params.File) for f in flat_dependant.body_params):
        BodySchema: Type[params.Body] = params.File
    elif any(isinstance(f.schema, params.Form) for f in flat_dependant.body_params):
        BodySchema = params.Form
    else:
        BodySchema = params.Body

    field = Field(
        name="body",
        type_=BodyModel,
        default=None,
        required=required,
        model_config=BaseConfig,
        class_validators={},
        alias="body",
        schema=BodySchema(None),
    )
    return field
