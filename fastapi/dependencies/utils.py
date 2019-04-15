import asyncio
import inspect
from copy import deepcopy
from datetime import date, datetime, time, timedelta
from decimal import Decimal
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
)
from uuid import UUID

from fastapi import params
from fastapi.dependencies.models import Dependant, SecurityRequirement
from fastapi.security.base import SecurityBase
from fastapi.security.oauth2 import OAuth2, SecurityScopes
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.utils import UnconstrainedConfig, get_path_param_names
from pydantic import Schema, create_model
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.fields import Field, Required, Shape
from pydantic.schema import get_annotation_from_schema
from pydantic.utils import lenient_issubclass
from starlette.background import BackgroundTasks
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import FormData, Headers, QueryParams, UploadFile
from starlette.requests import Request

param_supported_types = (
    str,
    int,
    float,
    bool,
    UUID,
    date,
    datetime,
    time,
    timedelta,
    Decimal,
)

sequence_shapes = {Shape.LIST, Shape.SET, Shape.TUPLE}
sequence_types = (list, set, tuple)
sequence_shape_to_type = {Shape.LIST: list, Shape.SET: set, Shape.TUPLE: tuple}


def get_sub_dependant(
    *, param: inspect.Parameter, path: str, security_scopes: List[str] = None
) -> Dependant:
    depends: params.Depends = param.default
    if depends.dependency:
        dependency = depends.dependency
    else:
        dependency = param.annotation
    security_requirement = None
    security_scopes = security_scopes or []
    if isinstance(depends, params.Security):
        dependency_scopes = depends.scopes
        security_scopes.extend(dependency_scopes)
    if isinstance(dependency, SecurityBase):
        use_scopes = []
        if isinstance(dependency, (OAuth2, OpenIdConnect)):
            use_scopes = security_scopes
        security_requirement = SecurityRequirement(
            security_scheme=dependency, scopes=use_scopes
        )
    sub_dependant = get_dependant(
        path=path, call=dependency, name=param.name, security_scopes=security_scopes
    )
    if security_requirement:
        sub_dependant.security_requirements.append(security_requirement)
    sub_dependant.security_scopes = security_scopes
    return sub_dependant


def get_flat_dependant(dependant: Dependant) -> Dependant:
    flat_dependant = Dependant(
        path_params=dependant.path_params.copy(),
        query_params=dependant.query_params.copy(),
        header_params=dependant.header_params.copy(),
        cookie_params=dependant.cookie_params.copy(),
        body_params=dependant.body_params.copy(),
        security_schemes=dependant.security_requirements.copy(),
    )
    for sub_dependant in dependant.dependencies:
        flat_sub = get_flat_dependant(sub_dependant)
        flat_dependant.path_params.extend(flat_sub.path_params)
        flat_dependant.query_params.extend(flat_sub.query_params)
        flat_dependant.header_params.extend(flat_sub.header_params)
        flat_dependant.cookie_params.extend(flat_sub.cookie_params)
        flat_dependant.body_params.extend(flat_sub.body_params)
        flat_dependant.security_requirements.extend(flat_sub.security_requirements)
    return flat_dependant


def get_dependant(
    *, path: str, call: Callable, name: str = None, security_scopes: List[str] = None
) -> Dependant:
    path_param_names = get_path_param_names(path)
    endpoint_signature = inspect.signature(call)
    signature_params = endpoint_signature.parameters
    dependant = Dependant(call=call, name=name)
    for param_name in signature_params:
        param = signature_params[param_name]
        if isinstance(param.default, params.Depends):
            sub_dependant = get_sub_dependant(
                param=param, path=path, security_scopes=security_scopes
            )
            dependant.dependencies.append(sub_dependant)
    for param_name in signature_params:
        param = signature_params[param_name]
        if (
            (param.default == param.empty) or isinstance(param.default, params.Path)
        ) and (param_name in path_param_names):
            assert (
                lenient_issubclass(param.annotation, param_supported_types)
                or param.annotation == param.empty
            ), f"Path params must be of one of the supported types"
            add_param_to_fields(
                param=param,
                dependant=dependant,
                default_schema=params.Path,
                force_type=params.ParamTypes.path,
            )
        elif (
            param.default == param.empty
            or param.default is None
            or isinstance(param.default, param_supported_types)
        ) and (
            param.annotation == param.empty
            or lenient_issubclass(param.annotation, param_supported_types)
        ):
            add_param_to_fields(
                param=param, dependant=dependant, default_schema=params.Query
            )
        elif isinstance(param.default, params.Param):
            if param.annotation != param.empty:
                origin = getattr(param.annotation, "__origin__", None)
                param_all_types = param_supported_types + (list, tuple, set)
                if isinstance(param.default, (params.Query, params.Header)):
                    assert lenient_issubclass(
                        param.annotation, param_all_types
                    ) or lenient_issubclass(
                        origin, param_all_types
                    ), f"Parameters for Query and Header must be of type str, int, float, bool, list, tuple or set: {param}"
                else:
                    assert lenient_issubclass(
                        param.annotation, param_supported_types
                    ), f"Parameters for Path and Cookies must be of type str, int, float, bool: {param}"
            add_param_to_fields(
                param=param, dependant=dependant, default_schema=params.Query
            )
        elif lenient_issubclass(param.annotation, Request):
            dependant.request_param_name = param_name
        elif lenient_issubclass(param.annotation, BackgroundTasks):
            dependant.background_tasks_param_name = param_name
        elif lenient_issubclass(param.annotation, SecurityScopes):
            dependant.security_scopes_param_name = param_name
        elif not isinstance(param.default, params.Depends):
            add_param_to_body_fields(param=param, dependant=dependant)
    return dependant


def add_param_to_fields(
    *,
    param: inspect.Parameter,
    dependant: Dependant,
    default_schema: Type[Schema] = params.Param,
    force_type: params.ParamTypes = None,
) -> None:
    default_value = Required
    if not param.default == param.empty:
        default_value = param.default
    if isinstance(default_value, params.Param):
        schema = default_value
        default_value = schema.default
        if getattr(schema, "in_", None) is None:
            schema.in_ = default_schema.in_
        if force_type:
            schema.in_ = force_type
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
        model_config=UnconstrainedConfig,
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


def add_param_to_body_fields(*, param: inspect.Parameter, dependant: Dependant) -> None:
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
        model_config=UnconstrainedConfig,
        class_validators=[],
        schema=schema,
    )
    dependant.body_params.append(field)


def is_coroutine_callable(call: Callable) -> bool:
    if inspect.isfunction(call):
        return asyncio.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    call = getattr(call, "__call__", None)
    return asyncio.iscoroutinefunction(call)


async def solve_dependencies(
    *,
    request: Request,
    dependant: Dependant,
    body: Dict[str, Any] = None,
    background_tasks: BackgroundTasks = None,
) -> Tuple[Dict[str, Any], List[ErrorWrapper], Optional[BackgroundTasks]]:
    values: Dict[str, Any] = {}
    errors: List[ErrorWrapper] = []
    for sub_dependant in dependant.dependencies:
        sub_values, sub_errors, background_tasks = await solve_dependencies(
            request=request,
            dependant=sub_dependant,
            body=body,
            background_tasks=background_tasks,
        )
        if sub_errors:
            errors.extend(sub_errors)
            continue
        assert sub_dependant.call is not None, "sub_dependant.call must be a function"
        if is_coroutine_callable(sub_dependant.call):
            solved = await sub_dependant.call(**sub_values)
        else:
            solved = await run_in_threadpool(sub_dependant.call, **sub_values)
        assert sub_dependant.name is not None, "Subdependants always have a name"
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
    errors += path_errors + query_errors + header_errors + cookie_errors
    if dependant.body_params:
        body_values, body_errors = await request_body_to_args(  # type: ignore # body_params checked above
            dependant.body_params, body
        )
        values.update(body_values)
        errors.extend(body_errors)
    if dependant.request_param_name:
        values[dependant.request_param_name] = request
    if dependant.background_tasks_param_name:
        if background_tasks is None:
            background_tasks = BackgroundTasks()
        values[dependant.background_tasks_param_name] = background_tasks
    if dependant.security_scopes_param_name:
        values[dependant.security_scopes_param_name] = SecurityScopes(
            scopes=dependant.security_scopes
        )
    return values, errors, background_tasks


def request_params_to_args(
    required_params: Sequence[Field],
    received_params: Union[Mapping[str, Any], QueryParams, Headers],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    for field in required_params:
        if field.shape in sequence_shapes and isinstance(
            received_params, (QueryParams, Headers)
        ):
            value = received_params.getlist(field.alias)
        else:
            value = received_params.get(field.alias)
        schema: params.Param = field.schema
        assert isinstance(schema, params.Param), "Params must be subclasses of Param"
        if value is None:
            if field.required:
                errors.append(
                    ErrorWrapper(
                        MissingError(),
                        loc=(schema.in_.value, field.alias),
                        config=UnconstrainedConfig,
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
    required_params: List[Field], received_body: Dict[str, Any]
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        embed = getattr(field.schema, "embed", None)
        if len(required_params) == 1 and not embed:
            received_body = {field.alias: received_body}
        for field in required_params:
            if field.shape in sequence_shapes and isinstance(received_body, FormData):
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
                            MissingError(),
                            loc=("body", field.alias),
                            config=UnconstrainedConfig,
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
        model_config=UnconstrainedConfig,
        class_validators=[],
        alias="body",
        schema=BodySchema(None),
    )
    return field
