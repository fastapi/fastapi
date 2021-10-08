import dataclasses
import inspect
from contextlib import contextmanager
from copy import deepcopy
from typing import (
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

import anyio
from fastapi import params
from fastapi.concurrency import (
    AsyncExitStack,
    asynccontextmanager,
    contextmanager_in_threadpool,
)
from fastapi.dependencies.models import Dependant, SecurityRequirement
from fastapi.logger import logger
from fastapi.security.base import SecurityBase
from fastapi.security.oauth2 import OAuth2, SecurityScopes
from fastapi.security.open_id_connect_url import OpenIdConnect
from fastapi.utils import create_response_field, get_path_param_names
from pydantic import BaseModel, create_model
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.fields import (
    SHAPE_LIST,
    SHAPE_SEQUENCE,
    SHAPE_SET,
    SHAPE_SINGLETON,
    SHAPE_TUPLE,
    SHAPE_TUPLE_ELLIPSIS,
    FieldInfo,
    ModelField,
    Required,
)
from pydantic.schema import get_annotation_from_field_info
from pydantic.typing import ForwardRef, evaluate_forwardref
from pydantic.utils import lenient_issubclass
from starlette.background import BackgroundTasks
from starlette.concurrency import run_in_threadpool
from starlette.datastructures import FormData, Headers, QueryParams, UploadFile
from starlette.requests import HTTPConnection, Request
from starlette.responses import Response
from starlette.websockets import WebSocket

sequence_shapes = {
    SHAPE_LIST,
    SHAPE_SET,
    SHAPE_TUPLE,
    SHAPE_SEQUENCE,
    SHAPE_TUPLE_ELLIPSIS,
}
sequence_types = (list, set, tuple)
sequence_shape_to_type = {
    SHAPE_LIST: list,
    SHAPE_SET: set,
    SHAPE_TUPLE: tuple,
    SHAPE_SEQUENCE: list,
    SHAPE_TUPLE_ELLIPSIS: list,
}


multipart_not_installed_error = (
    'Form data requires "python-multipart" to be installed. \n'
    'You can install "python-multipart" with: \n\n'
    "pip install python-multipart\n"
)
multipart_incorrect_install_error = (
    'Form data requires "python-multipart" to be installed. '
    'It seems you installed "multipart" instead. \n'
    'You can remove "multipart" with: \n\n'
    "pip uninstall multipart\n\n"
    'And then install "python-multipart" with: \n\n'
    "pip install python-multipart\n"
)


class DependencyNode(object):

    def __init__(
        self,
        call: Callable[..., Any],
        refcount: int = 0,
        backref: List[Tuple[int, str]] = None,
        arguments: Dict[str, Any] = None,
        result: Any = None,
    ):
        self.call = call
        self.refcount = refcount
        self.backref = backref or []
        self.arguments = arguments or {}
        self.result = result

    def copy(self):
        return DependencyNode(
            self.call,
            arguments={},
            refcount=self.refcount,
            backref=self.backref,
            result=None,
        )

    async def task(
        self,
        nodes: List['DependencyNode'],
        request: Request,
        task_group: anyio.abc.TaskGroup,
    ):
        call = self.call
        arguments = self.arguments
        promise = None
        if is_gen_callable(call) or is_async_gen_callable(call):
            stack = request.scope.get("fastapi_astack")
            assert isinstance(stack, AsyncExitStack)
            promise = solve_generator(call=call, stack=stack, arguments=arguments)
        elif is_coroutine_callable(call):
            promise = call(**arguments)
        else:
            promise = run_in_threadpool(call, **arguments)
        self.result = await promise

        for parent_node_idx, argument_name in self.backref:
            parent_node = nodes[parent_node_idx]
            if argument_name is not None:
                parent_node.arguments[argument_name] = self.result

            parent_node.refcount -= 1
            if parent_node.refcount == 0:
                task_group.start_soon(parent_node.task, nodes, request, task_group)


class SolvingPlan(object):

    def __init__(
        self,
        nodes,
        path_params_list,
        query_params_list,
        header_params_list,
        cookie_params_list,
        background_tasks_param_list,
        http_connection_param_list,
        request_param_list,
        websocket_param_list,
        response_param_list,
        security_scopes_param_list,
        body_params_list,
    ):
        self.nodes = nodes
        self.path_params_list = path_params_list
        self.query_params_list = query_params_list
        self.header_params_list = header_params_list
        self.cookie_params_list = cookie_params_list
        self.background_tasks_param_list = background_tasks_param_list
        self.http_connection_param_list = http_connection_param_list
        self.request_param_list = request_param_list
        self.websocket_param_list = websocket_param_list
        self.response_param_list = response_param_list
        self.security_scopes_param_list = security_scopes_param_list
        self.body_params_list = body_params_list


def check_file_field(field: ModelField) -> None:
    field_info = field.field_info
    if isinstance(field_info, params.Form):
        try:
            # __version__ is available in both multiparts, and can be mocked
            from multipart import __version__  # type: ignore

            assert __version__
            try:
                # parse_options_header is only available in the right multipart
                from multipart.multipart import parse_options_header  # type: ignore

                assert parse_options_header
            except ImportError:
                logger.error(multipart_incorrect_install_error)
                raise RuntimeError(multipart_incorrect_install_error)
        except ImportError:
            logger.error(multipart_not_installed_error)
            raise RuntimeError(multipart_not_installed_error)


def get_param_sub_dependant(
    *, param: inspect.Parameter, path: str, security_scopes: Optional[List[str]] = None
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
    dependency: Callable[..., Any],
    path: str,
    name: Optional[str] = None,
    security_scopes: Optional[List[str]] = None,
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


CacheKey = Tuple[Optional[Callable[..., Any]], Tuple[str, ...]]


def get_flat_dependant(
    dependant: Dependant,
    *,
    skip_repeats: bool = False,
    visited: Optional[List[CacheKey]] = None,
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


def get_flat_params(dependant: Dependant) -> List[ModelField]:
    flat_dependant = get_flat_dependant(dependant, skip_repeats=True)
    return (
        flat_dependant.path_params
        + flat_dependant.query_params
        + flat_dependant.header_params
        + flat_dependant.cookie_params
    )


def is_scalar_field(field: ModelField) -> bool:
    field_info = field.field_info
    if not (
        field.shape == SHAPE_SINGLETON
        and not lenient_issubclass(field.type_, BaseModel)
        and not lenient_issubclass(field.type_, sequence_types + (dict,))
        and not dataclasses.is_dataclass(field.type_)
        and not isinstance(field_info, params.Body)
    ):
        return False
    if field.sub_fields:
        if not all(is_scalar_field(f) for f in field.sub_fields):
            return False
    return True


def is_scalar_sequence_field(field: ModelField) -> bool:
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


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    signature = inspect.signature(call)
    globalns = getattr(call, "__globals__", {})
    typed_params = [
        inspect.Parameter(
            name=param.name,
            kind=param.kind,
            default=param.default,
            annotation=get_typed_annotation(param, globalns),
        )
        for param in signature.parameters.values()
    ]
    typed_signature = inspect.Signature(typed_params)
    return typed_signature


def get_typed_annotation(param: inspect.Parameter, globalns: Dict[str, Any]) -> Any:
    annotation = param.annotation
    if isinstance(annotation, str):
        annotation = ForwardRef(annotation)
        annotation = evaluate_forwardref(annotation, globalns, globalns)
    return annotation


def get_dependant(
    *,
    path: str,
    call: Callable[..., Any],
    name: Optional[str] = None,
    security_scopes: Optional[List[str]] = None,
    use_cache: bool = True,
) -> Dependant:
    path_param_names = get_path_param_names(path)
    endpoint_signature = get_typed_signature(call)
    signature_params = endpoint_signature.parameters
    dependant = Dependant(call=call, name=name, path=path, use_cache=use_cache)
    for param_name, param in signature_params.items():
        if isinstance(param.default, params.Depends):
            sub_dependant = get_param_sub_dependant(
                param=param, path=path, security_scopes=security_scopes
            )
            dependant.dependencies.append(sub_dependant)
            continue
        if add_non_field_param_to_dependency(param=param, dependant=dependant):
            continue
        param_field = get_param_field(
            param=param, default_field_info=params.Query, param_name=param_name
        )
        if param_name in path_param_names:
            assert is_scalar_field(
                field=param_field
            ), "Path params must be of one of the supported types"
            if isinstance(param.default, params.Path):
                ignore_default = False
            else:
                ignore_default = True
            param_field = get_param_field(
                param=param,
                param_name=param_name,
                default_field_info=params.Path,
                force_type=params.ParamTypes.path,
                ignore_default=ignore_default,
            )
            add_param_to_fields(field=param_field, dependant=dependant)
        elif is_scalar_field(field=param_field):
            add_param_to_fields(field=param_field, dependant=dependant)
        elif isinstance(
            param.default, (params.Query, params.Header)
        ) and is_scalar_sequence_field(param_field):
            add_param_to_fields(field=param_field, dependant=dependant)
        else:
            field_info = param_field.field_info
            assert isinstance(
                field_info, params.Body
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
    elif lenient_issubclass(param.annotation, HTTPConnection):
        dependant.http_connection_param_name = param.name
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
    param_name: str,
    default_field_info: Type[params.Param] = params.Param,
    force_type: Optional[params.ParamTypes] = None,
    ignore_default: bool = False,
) -> ModelField:
    default_value = Required
    had_schema = False
    if not param.default == param.empty and ignore_default is False:
        default_value = param.default
    if isinstance(default_value, FieldInfo):
        had_schema = True
        field_info = default_value
        default_value = field_info.default
        if (
            isinstance(field_info, params.Param)
            and getattr(field_info, "in_", None) is None
        ):
            field_info.in_ = default_field_info.in_
        if force_type:
            field_info.in_ = force_type  # type: ignore
    else:
        field_info = default_field_info(default_value)
    required = default_value == Required
    annotation: Any = Any
    if not param.annotation == param.empty:
        annotation = param.annotation
    annotation = get_annotation_from_field_info(annotation, field_info, param_name)
    if not field_info.alias and getattr(field_info, "convert_underscores", None):
        alias = param.name.replace("_", "-")
    else:
        alias = field_info.alias or param.name
    field = create_response_field(
        name=param.name,
        type_=annotation,
        default=None if required else default_value,
        alias=alias,
        required=required,
        field_info=field_info,
    )
    field.required = required
    if not had_schema and not is_scalar_field(field=field):
        field.field_info = params.Body(field_info.default)

    return field


def add_param_to_fields(*, field: ModelField, dependant: Dependant) -> None:
    field_info = cast(params.Param, field.field_info)
    if field_info.in_ == params.ParamTypes.path:
        dependant.path_params.append(field)
    elif field_info.in_ == params.ParamTypes.query:
        dependant.query_params.append(field)
    elif field_info.in_ == params.ParamTypes.header:
        dependant.header_params.append(field)
    else:
        assert (
            field_info.in_ == params.ParamTypes.cookie
        ), f"non-body parameters must be in path, query, header or cookie: {field.name}"
        dependant.cookie_params.append(field)


def is_coroutine_callable(call: Callable[..., Any]) -> bool:
    if inspect.isroutine(call):
        return inspect.iscoroutinefunction(call)
    if inspect.isclass(call):
        return False
    call = getattr(call, "__call__", None)
    return inspect.iscoroutinefunction(call)


def is_async_gen_callable(call: Callable[..., Any]) -> bool:
    if inspect.isasyncgenfunction(call):
        return True
    call = getattr(call, "__call__", None)
    return inspect.isasyncgenfunction(call)


def is_gen_callable(call: Callable[..., Any]) -> bool:
    if inspect.isgeneratorfunction(call):
        return True
    call = getattr(call, "__call__", None)
    return inspect.isgeneratorfunction(call)


async def solve_generator(
    *, call: Callable[..., Any], stack: AsyncExitStack, arguments: Dict[str, Any]
) -> Any:
    if is_gen_callable(call):
        cm = contextmanager_in_threadpool(contextmanager(call)(**arguments))
    elif is_async_gen_callable(call):
        cm = asynccontextmanager(call)(**arguments)
    return await stack.enter_async_context(cm)


def get_solving_plan(
    dependant: Dependant,
    dependency_overrides_provider: Optional[Any] = None,
):
    assert dependant.call is not None, "dependant.call must be a function"

    stack = [(None, dependant)]
    node_cache = {}
    overrides = getattr(dependency_overrides_provider, 'dependency_overrides', None) or {}

    nodes = []
    path_params_list = []
    query_params_list = []
    header_params_list = []
    cookie_params_list = []
    background_tasks_param_list = []
    http_connection_param_list = []
    request_param_list = []
    websocket_param_list = []
    response_param_list = []
    security_scopes_param_list = []
    body_params_list = []

    while stack:
        parent_node_idx, dependant = stack.pop()

        dependant.call = cast(Callable[..., Any], dependant.call)
        overrided_call = overrides.get(dependant.call)
        if overrided_call:
            security_scopes = dependant.security_scopes
            dependant = get_dependant(
                path=dependant.path,
                call=overrided_call,
                name=dependant.name,
                security_scopes=security_scopes,
            )
            dependant.security_scopes = security_scopes

        dependant.cache_key = cast(Tuple[Callable[..., Any], Tuple[str]], dependant.cache_key)

        if dependant.use_cache and dependant.cache_key in node_cache:
            node = node_cache[dependant.cache_key]
            if parent_node_idx is not None:
                node.backref.append((parent_node_idx, dependant.name))
            continue

        node = DependencyNode(call=dependant.call)
        node_idx = len(nodes)
        nodes.append(node)

        if parent_node_idx is not None:
            node.backref.append((parent_node_idx, dependant.name))

        if dependant.use_cache:
            node_cache[dependant.cache_key] = node

        # NOTE reverse dependencies only to comply legacy unit tests
        for sub_dependant in reversed(dependant.dependencies):
            node.refcount += 1
            stack.append((node_idx, sub_dependant))

        for dependant_params, list_for_params in (
            (dependant.path_params, path_params_list),
            (dependant.query_params, query_params_list),
            (dependant.header_params, header_params_list),
            (dependant.cookie_params, cookie_params_list),
        ):
            for dependant_param in dependant_params:
                list_for_params.append((node_idx, dependant_param))

        for param_name, list_for_params in (
            (
                dependant.background_tasks_param_name,
                background_tasks_param_list,
            ),
            (dependant.http_connection_param_name, http_connection_param_list),
            (dependant.request_param_name, request_param_list),
            (dependant.websocket_param_name, websocket_param_list),
            (dependant.response_param_name, response_param_list),
            (dependant.body_params, body_params_list),
        ):
            if param_name:
                list_for_params.append((node_idx, param_name))

        if dependant.security_scopes_param_name:
            security_scopes_param_list.append((
                node_idx, dependant.security_scopes_param_name, dependant.security_scopes
            ))

    plan = SolvingPlan(
        nodes,
        path_params_list,
        query_params_list,
        header_params_list,
        cookie_params_list,
        background_tasks_param_list,
        http_connection_param_list,
        request_param_list,
        websocket_param_list,
        response_param_list,
        security_scopes_param_list,
        body_params_list,
    )

    return plan


async def run_plan(
    plan: SolvingPlan,
    request: Union[Request, WebSocket],
    body: Optional[Union[Dict[str, Any], FormData]] = None,
) -> Any:
    response = Response(
        content=None,
        status_code=None,  # type: ignore
        headers=None,  # type: ignore # in Starlette
        media_type=None,  # type: ignore # in Starlette
        background=None,  # type: ignore # in Starlette
    )
    background_tasks = None
    errors = []
    nodes = [node.copy() for node in plan.nodes]

    if plan.background_tasks_param_list:
        background_tasks = BackgroundTasks()
        for node_idx, param_name in plan.background_tasks_param_list:
            nodes[node_idx].arguments[param_name] = background_tasks

    for node_idx, param_name in plan.http_connection_param_list:
        nodes[node_idx].arguments[param_name] = request

    if isinstance(request, Request):
        for node_idx, param_name in plan.request_param_list:
            nodes[node_idx].arguments[param_name] = request
    elif isinstance(request, WebSocket):
        for node_idx, param_name in plan.websocket_param_list:
            nodes[node_idx].arguments[param_name] = request

    for node_idx, param_name in plan.response_param_list:
        nodes[node_idx].arguments[param_name] = response

    for node_idx, param_name, security_scopes in plan.security_scopes_param_list:
        nodes[node_idx].arguments[param_name] = SecurityScopes(scopes=security_scopes)

    for required_params, received_params in (
        (plan.path_params_list, request.path_params),
        (plan.query_params_list, request.query_params),
        (plan.header_params_list, request.headers),
        (plan.cookie_params_list, request.cookies),
    ):
        for node_idx, field in required_params:
            node_arguments = nodes[node_idx].arguments

            if (
                is_scalar_sequence_field(field)
                and isinstance(received_params, (QueryParams, Headers))
            ):
                value = received_params.getlist(field.alias) or field.default
            else:
                value = received_params.get(field.alias)

            field_info = field.field_info
            if value is None:
                if field.required:
                    errors.append(
                        ErrorWrapper(
                            MissingError(), loc=(field_info.in_.value, field.alias)
                        )
                    )
                else:
                    node_arguments[field.name] = deepcopy(field.default)
                continue
            v_, errors_ = field.validate(
                value, node_arguments, loc=(field_info.in_.value, field.alias)
            )
            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                node_arguments[field.name] = v_

    # TODO make async task
    for node_idx, body_params in plan.body_params_list:
        (
            body_values,
            body_errors,
        ) = await request_body_to_args(  # body_params checked above
            required_params=body_params, received_body=body
        )
        nodes[node_idx].arguments.update(body_values)
        errors.extend(body_errors)

    if errors:
        return nodes[0].result, errors, background_tasks, response

    async with anyio.create_task_group() as task_group:
        for node in nodes:
            if node.refcount == 0:
                task_group.start_soon(node.task, nodes, request, task_group)

    return nodes[0].result, errors, background_tasks, response


async def request_body_to_args(
    required_params: List[ModelField],
    received_body: Optional[Union[Dict[str, Any], FormData]],
) -> Tuple[Dict[str, Any], List[ErrorWrapper]]:
    values = {}
    errors = []
    if required_params:
        field = required_params[0]
        field_info = field.field_info
        embed = getattr(field_info, "embed", None)
        field_alias_omitted = len(required_params) == 1 and not embed
        if field_alias_omitted:
            received_body = {field.alias: received_body}

        for field in required_params:
            loc: Tuple[str, ...]
            if field_alias_omitted:
                loc = ("body",)
            else:
                loc = ("body", field.alias)

            value: Optional[Any] = None
            if received_body is not None:
                if (
                    field.shape in sequence_shapes or field.type_ in sequence_types
                ) and isinstance(received_body, FormData):
                    value = received_body.getlist(field.alias)
                else:
                    try:
                        value = received_body.get(field.alias)
                    except AttributeError:
                        errors.append(get_missing_field_error(loc))
                        continue
            if (
                value is None
                or (isinstance(field_info, params.Form) and value == "")
                or (
                    isinstance(field_info, params.Form)
                    and field.shape in sequence_shapes
                    and len(value) == 0
                )
            ):
                if field.required:
                    errors.append(get_missing_field_error(loc))
                else:
                    values[field.name] = deepcopy(field.default)
                continue
            if (
                isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, UploadFile)
            ):
                value = await value.read()
            elif (
                field.shape in sequence_shapes
                and isinstance(field_info, params.File)
                and lenient_issubclass(field.type_, bytes)
                and isinstance(value, sequence_types)
            ):
                results: List[Union[bytes, str]] = []

                async def process_fn(
                    fn: Callable[[], Coroutine[Any, Any, Any]]
                ) -> None:
                    result = await fn()
                    results.append(result)

                async with anyio.create_task_group() as tg:
                    for sub_value in value:
                        tg.start_soon(process_fn, sub_value.read)
                value = sequence_shape_to_type[field.shape](results)

            v_, errors_ = field.validate(value, values, loc=loc)

            if isinstance(errors_, ErrorWrapper):
                errors.append(errors_)
            elif isinstance(errors_, list):
                errors.extend(errors_)
            else:
                values[field.name] = v_
    return values, errors


def get_missing_field_error(loc: Tuple[str, ...]) -> ErrorWrapper:
    missing_field_error = ErrorWrapper(MissingError(), loc=loc)
    return missing_field_error


def get_schema_compatible_field(*, field: ModelField) -> ModelField:
    out_field = field
    if lenient_issubclass(field.type_, UploadFile):
        use_type: type = bytes
        if field.shape in sequence_shapes:
            use_type = List[bytes]
        out_field = create_response_field(
            name=field.name,
            type_=use_type,
            class_validators=field.class_validators,
            model_config=field.model_config,
            default=field.default,
            required=field.required,
            alias=field.alias,
            field_info=field.field_info,
        )
    return out_field


def get_body_field(*, dependant: Dependant, name: str) -> Optional[ModelField]:
    flat_dependant = get_flat_dependant(dependant)
    if not flat_dependant.body_params:
        return None
    first_param = flat_dependant.body_params[0]
    field_info = first_param.field_info
    embed = getattr(field_info, "embed", None)
    body_param_names_set = {param.name for param in flat_dependant.body_params}
    if len(body_param_names_set) == 1 and not embed:
        final_field = get_schema_compatible_field(field=first_param)
        check_file_field(final_field)
        return final_field
    # If one field requires to embed, all have to be embedded
    # in case a sub-dependency is evaluated with a single unique body field
    # That is combined (embedded) with other body fields
    for param in flat_dependant.body_params:
        setattr(param.field_info, "embed", True)
    model_name = "Body_" + name
    BodyModel: Type[BaseModel] = create_model(model_name)
    for f in flat_dependant.body_params:
        BodyModel.__fields__[f.name] = get_schema_compatible_field(field=f)
    required = any(True for f in flat_dependant.body_params if f.required)

    BodyFieldInfo_kwargs: Dict[str, Any] = dict(default=None)
    if any(isinstance(f.field_info, params.File) for f in flat_dependant.body_params):
        BodyFieldInfo: Type[params.Body] = params.File
    elif any(isinstance(f.field_info, params.Form) for f in flat_dependant.body_params):
        BodyFieldInfo = params.Form
    else:
        BodyFieldInfo = params.Body

        body_param_media_types = [
            getattr(f.field_info, "media_type")
            for f in flat_dependant.body_params
            if isinstance(f.field_info, params.Body)
        ]
        if len(set(body_param_media_types)) == 1:
            BodyFieldInfo_kwargs["media_type"] = body_param_media_types[0]
    final_field = create_response_field(
        name="body",
        type_=BodyModel,
        required=required,
        alias="body",
        field_info=BodyFieldInfo(**BodyFieldInfo_kwargs),
    )
    check_file_field(final_field)
    return final_field
