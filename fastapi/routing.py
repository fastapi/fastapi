import asyncio
import inspect
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Type, Union

from fastapi import params
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import (
    get_body_field,
    get_dependant,
    get_parameterless_sub_dependant,
    solve_dependencies,
)
from fastapi.encoders import DictIntStrAny, SetIntStr, jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.logger import logger
from fastapi.openapi.constants import STATUS_CODES_WITH_NO_BODY
from fastapi.utils import (
    PYDANTIC_1,
    create_cloned_field,
    generate_operation_id_for_path,
    get_field_info,
    warning_response_model_skip_defaults_deprecated,
)
from pydantic import BaseConfig, BaseModel
from pydantic.error_wrappers import ErrorWrapper, ValidationError
from pydantic.utils import lenient_issubclass
from starlette import routing
from starlette.concurrency import run_in_threadpool
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import (
    compile_path,
    get_name,
    request_response,
    websocket_session,
)
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.types import ASGIApp
from starlette.websockets import WebSocket

try:
    from pydantic.fields import FieldInfo, ModelField
except ImportError:  # pragma: nocover
    # TODO: remove when removing support for Pydantic < 1.0.0
    from pydantic import Schema as FieldInfo  # type: ignore
    from pydantic.fields import Field as ModelField  # type: ignore


def serialize_response(
    *,
    field: ModelField = None,
    response: Response,
    include: Union[SetIntStr, DictIntStrAny] = None,
    exclude: Union[SetIntStr, DictIntStrAny] = set(),
    by_alias: bool = True,
    exclude_unset: bool = False,
) -> Any:
    if field:
        errors = []
        if exclude_unset and isinstance(response, BaseModel):
            if PYDANTIC_1:
                response = response.dict(exclude_unset=exclude_unset)
            else:
                response = response.dict(skip_defaults=exclude_unset)  # pragma: nocover
        value, errors_ = field.validate(response, {}, loc=("response",))
        if isinstance(errors_, ErrorWrapper):
            errors.append(errors_)
        elif isinstance(errors_, list):
            errors.extend(errors_)
        if errors:
            raise ValidationError(errors, field.type_)
        return jsonable_encoder(
            value,
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            exclude_unset=exclude_unset,
        )
    else:
        return jsonable_encoder(response)


def get_request_handler(
    dependant: Dependant,
    body_field: ModelField = None,
    status_code: int = 200,
    response_class: Type[Response] = JSONResponse,
    response_field: ModelField = None,
    response_model_include: Union[SetIntStr, DictIntStrAny] = None,
    response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    dependency_overrides_provider: Any = None,
) -> Callable:
    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = asyncio.iscoroutinefunction(dependant.call)
    is_body_form = body_field and isinstance(get_field_info(body_field), params.Form)

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
            logger.error(f"Error getting request body: {e}")
            raise HTTPException(
                status_code=400, detail="There was an error parsing the body"
            ) from e
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=body,
            dependency_overrides_provider=dependency_overrides_provider,
        )
        values, errors, background_tasks, sub_response, _ = solved_result
        if errors:
            raise RequestValidationError(errors)
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
                field=response_field,
                response=raw_response,
                include=response_model_include,
                exclude=response_model_exclude,
                by_alias=response_model_by_alias,
                exclude_unset=response_model_exclude_unset,
            )
            response = response_class(
                content=response_data,
                status_code=status_code,
                background=background_tasks,
            )
            response.headers.raw.extend(sub_response.headers.raw)
            if sub_response.status_code:
                response.status_code = sub_response.status_code
            return response

    return app


def get_websocket_app(
    dependant: Dependant, dependency_overrides_provider: Any = None
) -> Callable:
    async def app(websocket: WebSocket) -> None:
        solved_result = await solve_dependencies(
            request=websocket,
            dependant=dependant,
            dependency_overrides_provider=dependency_overrides_provider,
        )
        values, errors, _, _2, _3 = solved_result
        if errors:
            await websocket.close(code=WS_1008_POLICY_VIOLATION)
            raise WebSocketRequestValidationError(errors)
        assert dependant.call is not None, "dependant.call must be a function"
        await dependant.call(**values)

    return app


class APIWebSocketRoute(routing.WebSocketRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        name: str = None,
        dependency_overrides_provider: Any = None,
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.dependant = get_dependant(path=path, call=self.endpoint)
        self.app = websocket_session(
            get_websocket_app(
                dependant=self.dependant,
                dependency_overrides_provider=dependency_overrides_provider,
            )
        )
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)


class APIRoute(routing.Route):
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        name: str = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Optional[Type[Response]] = None,
        dependency_overrides_provider: Any = None,
        callbacks: Optional[List["APIRoute"]] = None,
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        if methods is None:
            methods = ["GET"]
        self.methods = set([method.upper() for method in methods])
        self.unique_id = generate_operation_id_for_path(
            name=self.name, path=self.path_format, method=list(methods)[0]
        )
        self.response_model = response_model
        if self.response_model:
            assert (
                status_code not in STATUS_CODES_WITH_NO_BODY
            ), f"Status code {status_code} must not have a response body"
            response_name = "Response_" + self.unique_id
            if PYDANTIC_1:
                self.response_field: Optional[ModelField] = ModelField(
                    name=response_name,
                    type_=self.response_model,
                    class_validators={},
                    default=None,
                    required=False,
                    model_config=BaseConfig,
                    field_info=FieldInfo(None),
                )
            else:
                self.response_field: Optional[ModelField] = ModelField(  # type: ignore  # pragma: nocover
                    name=response_name,
                    type_=self.response_model,
                    class_validators={},
                    default=None,
                    required=False,
                    model_config=BaseConfig,
                    schema=FieldInfo(None),
                )
            # Create a clone of the field, so that a Pydantic submodel is not returned
            # as is just because it's an instance of a subclass of a more limited class
            # e.g. UserInDB (containing hashed_password) could be a subclass of User
            # that doesn't have the hashed_password. But because it's a subclass, it
            # would pass the validation and be returned as is.
            # By being a new field, no inheritance will be passed as is. A new model
            # will be always created.
            self.secure_cloned_response_field: Optional[
                ModelField
            ] = create_cloned_field(self.response_field)
        else:
            self.response_field = None
            self.secure_cloned_response_field = None
        self.status_code = status_code
        self.tags = tags or []
        if dependencies:
            self.dependencies = list(dependencies)
        else:
            self.dependencies = []
        self.summary = summary
        self.description = description or inspect.cleandoc(self.endpoint.__doc__ or "")
        # if a "form feed" character (page break) is found in the description text,
        # truncate description text to the content preceding the first "form feed"
        self.description = self.description.split("\f")[0]
        self.response_description = response_description
        self.responses = responses or {}
        response_fields = {}
        for additional_status_code, response in self.responses.items():
            assert isinstance(response, dict), "An additional response must be a dict"
            model = response.get("model")
            if model:
                assert (
                    additional_status_code not in STATUS_CODES_WITH_NO_BODY
                ), f"Status code {additional_status_code} must not have a response body"
                assert lenient_issubclass(
                    model, BaseModel
                ), "A response model must be a Pydantic model"
                response_name = f"Response_{additional_status_code}_{self.unique_id}"
                if PYDANTIC_1:
                    response_field = ModelField(
                        name=response_name,
                        type_=model,
                        class_validators=None,
                        default=None,
                        required=False,
                        model_config=BaseConfig,
                        field_info=FieldInfo(None),
                    )
                else:
                    response_field = ModelField(  # type: ignore  # pragma: nocover
                        name=response_name,
                        type_=model,
                        class_validators=None,
                        default=None,
                        required=False,
                        model_config=BaseConfig,
                        schema=FieldInfo(None),
                    )
                response_fields[additional_status_code] = response_field
        if response_fields:
            self.response_fields: Dict[Union[int, str], ModelField] = response_fields
        else:
            self.response_fields = {}
        self.deprecated = deprecated
        self.operation_id = operation_id
        self.response_model_include = response_model_include
        self.response_model_exclude = response_model_exclude
        self.response_model_by_alias = response_model_by_alias
        self.response_model_exclude_unset = response_model_exclude_unset
        self.include_in_schema = include_in_schema
        self.response_class = response_class

        assert inspect.isfunction(endpoint) or inspect.ismethod(
            endpoint
        ), f"An endpoint must be a function or method"
        self.dependant = get_dependant(path=self.path_format, call=self.endpoint)
        for depends in self.dependencies[::-1]:
            self.dependant.dependencies.insert(
                0,
                get_parameterless_sub_dependant(depends=depends, path=self.path_format),
            )
        self.body_field = get_body_field(dependant=self.dependant, name=self.unique_id)
        self.dependency_overrides_provider = dependency_overrides_provider
        self.callbacks = callbacks
        self.app = request_response(self.get_route_handler())

    def get_route_handler(self) -> Callable:
        return get_request_handler(
            dependant=self.dependant,
            body_field=self.body_field,
            status_code=self.status_code,
            response_class=self.response_class or JSONResponse,
            response_field=self.secure_cloned_response_field,
            response_model_include=self.response_model_include,
            response_model_exclude=self.response_model_exclude,
            response_model_by_alias=self.response_model_by_alias,
            response_model_exclude_unset=self.response_model_exclude_unset,
            dependency_overrides_provider=self.dependency_overrides_provider,
        )


class APIRouter(routing.Router):
    def __init__(
        self,
        routes: List[routing.BaseRoute] = None,
        redirect_slashes: bool = True,
        default: ASGIApp = None,
        dependency_overrides_provider: Any = None,
        route_class: Type[APIRoute] = APIRoute,
        default_response_class: Type[Response] = None,
    ) -> None:
        super().__init__(
            routes=routes, redirect_slashes=redirect_slashes, default=default
        )
        self.dependency_overrides_provider = dependency_overrides_provider
        self.route_class = route_class
        self.default_response_class = default_response_class

    def add_api_route(
        self,
        path: str,
        endpoint: Callable,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        methods: Optional[Union[Set[str], List[str]]] = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        route_class_override: Optional[Type[APIRoute]] = None,
        callbacks: List[APIRoute] = None,
    ) -> None:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        route_class = route_class_override or self.route_class
        route = route_class(
            path,
            endpoint=endpoint,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=methods,
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            dependency_overrides_provider=self.dependency_overrides_provider,
            callbacks=callbacks,
        )
        self.routes.append(route)

    def api_route(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        methods: List[str] = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover

        def decorator(func: Callable) -> Callable:
            self.add_api_route(
                path,
                func,
                response_model=response_model,
                status_code=status_code,
                tags=tags or [],
                dependencies=dependencies,
                summary=summary,
                description=description,
                response_description=response_description,
                responses=responses or {},
                deprecated=deprecated,
                methods=methods,
                operation_id=operation_id,
                response_model_include=response_model_include,
                response_model_exclude=response_model_exclude,
                response_model_by_alias=response_model_by_alias,
                response_model_exclude_unset=bool(
                    response_model_exclude_unset or response_model_skip_defaults
                ),
                include_in_schema=include_in_schema,
                response_class=response_class or self.default_response_class,
                name=name,
                callbacks=callbacks,
            )
            return func

        return decorator

    def add_api_websocket_route(
        self, path: str, endpoint: Callable, name: str = None
    ) -> None:
        route = APIWebSocketRoute(path, endpoint=endpoint, name=name)
        self.routes.append(route)

    def websocket(self, path: str, name: str = None) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.add_api_websocket_route(path, func, name=name)
            return func

        return decorator

    def include_router(
        self,
        router: "APIRouter",
        *,
        prefix: str = "",
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        default_response_class: Optional[Type[Response]] = None,
    ) -> None:
        if prefix:
            assert prefix.startswith("/"), "A path prefix must start with '/'"
            assert not prefix.endswith(
                "/"
            ), "A path prefix must not end with '/', as the routes will start with '/'"
        else:
            for r in router.routes:
                path = getattr(r, "path")
                name = getattr(r, "name", "unknown")
                if path is not None and not path:
                    raise Exception(
                        f"Prefix and path cannot be both empty (path operation: {name})"
                    )
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
                    dependencies=list(dependencies or [])
                    + list(route.dependencies or []),
                    summary=route.summary,
                    description=route.description,
                    response_description=route.response_description,
                    responses=combined_responses,
                    deprecated=route.deprecated,
                    methods=route.methods,
                    operation_id=route.operation_id,
                    response_model_include=route.response_model_include,
                    response_model_exclude=route.response_model_exclude,
                    response_model_by_alias=route.response_model_by_alias,
                    response_model_exclude_unset=route.response_model_exclude_unset,
                    include_in_schema=route.include_in_schema,
                    response_class=route.response_class or default_response_class,
                    name=route.name,
                    route_class_override=type(route),
                )
            elif isinstance(route, routing.Route):
                self.add_route(
                    prefix + route.path,
                    route.endpoint,
                    methods=list(route.methods or []),
                    include_in_schema=route.include_in_schema,
                    name=route.name,
                )
            elif isinstance(route, APIWebSocketRoute):
                self.add_api_websocket_route(
                    prefix + route.path, route.endpoint, name=route.name
                )
            elif isinstance(route, routing.WebSocketRoute):
                self.add_websocket_route(
                    prefix + route.path, route.endpoint, name=route.name
                )

    def get(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["GET"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def put(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["PUT"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def post(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["POST"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def delete(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["DELETE"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def options(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["OPTIONS"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def head(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["HEAD"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def patch(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["PATCH"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )

    def trace(
        self,
        path: str,
        *,
        response_model: Type[Any] = None,
        status_code: int = 200,
        tags: List[str] = None,
        dependencies: Sequence[params.Depends] = None,
        summary: str = None,
        description: str = None,
        response_description: str = "Successful Response",
        responses: Dict[Union[int, str], Dict[str, Any]] = None,
        deprecated: bool = None,
        operation_id: str = None,
        response_model_include: Union[SetIntStr, DictIntStrAny] = None,
        response_model_exclude: Union[SetIntStr, DictIntStrAny] = set(),
        response_model_by_alias: bool = True,
        response_model_skip_defaults: bool = None,
        response_model_exclude_unset: bool = False,
        include_in_schema: bool = True,
        response_class: Type[Response] = None,
        name: str = None,
        callbacks: List[APIRoute] = None,
    ) -> Callable:
        if response_model_skip_defaults is not None:
            warning_response_model_skip_defaults_deprecated()  # pragma: nocover
        return self.api_route(
            path=path,
            response_model=response_model,
            status_code=status_code,
            tags=tags or [],
            dependencies=dependencies,
            summary=summary,
            description=description,
            response_description=response_description,
            responses=responses or {},
            deprecated=deprecated,
            methods=["TRACE"],
            operation_id=operation_id,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=bool(
                response_model_exclude_unset or response_model_skip_defaults
            ),
            include_in_schema=include_in_schema,
            response_class=response_class or self.default_response_class,
            name=name,
            callbacks=callbacks,
        )
