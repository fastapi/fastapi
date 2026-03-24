import inspect
from collections.abc import Callable, Coroutine, Sequence
from enum import Enum, IntEnum
from typing import Any

from fastapi import params
from fastapi._compat import ModelField, lenient_issubclass
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.dependencies.utils import (
    _should_embed_body_fields,
    get_body_field,
    get_dependant,
    get_flat_dependant,
    get_parameterless_sub_dependant,
    get_stream_item_type,
    get_typed_return_annotation,
)
from fastapi.routing_handlers import (
    RouteHandlerConfig,
    get_request_handler,
    get_websocket_app,
)
from fastapi.routing_utils import request_response, websocket_session
from fastapi.sse import EventSourceResponse, ServerSentEvent
from fastapi.types import IncEx
from fastapi.utils import (
    create_model_field,
    generate_unique_id,
    is_body_allowed_for_status_code,
)
from starlette import routing
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import BaseRoute, Match, compile_path, get_name
from starlette.types import Scope


class APIWebSocketRoute(routing.WebSocketRoute):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        name: str | None = None,
        dependencies: Sequence[params.Depends] | None = None,
        dependency_overrides_provider: Any | None = None,
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.name = get_name(endpoint) if name is None else name
        self.dependencies = list(dependencies or [])
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        self.dependant = get_dependant(
            path=self.path_format, call=self.endpoint, scope="function"
        )
        for depends in self.dependencies[::-1]:
            self.dependant.dependencies.insert(
                0,
                get_parameterless_sub_dependant(depends=depends, path=self.path_format),
            )
        self._flat_dependant = get_flat_dependant(self.dependant)
        self._embed_body_fields = _should_embed_body_fields(
            self._flat_dependant.body_params
        )
        self.app = websocket_session(
            get_websocket_app(
                dependant=self.dependant,
                dependency_overrides_provider=dependency_overrides_provider,
                embed_body_fields=self._embed_body_fields,
            )
        )

    def matches(self, scope: Scope) -> tuple[Match, Scope]:
        match, child_scope = super().matches(scope)
        if match != Match.NONE:
            child_scope["route"] = self
        return match, child_scope


class APIRoute(routing.Route):
    def __init__(
        self,
        path: str,
        endpoint: Callable[..., Any],
        *,
        response_model: Any = Default(None),
        status_code: int | None = None,
        tags: list[str | Enum] | None = None,
        dependencies: Sequence[params.Depends] | None = None,
        summary: str | None = None,
        description: str | None = None,
        response_description: str = "Successful Response",
        responses: dict[int | str, dict[str, Any]] | None = None,
        deprecated: bool | None = None,
        name: str | None = None,
        methods: set[str] | list[str] | None = None,
        operation_id: str | None = None,
        response_model_include: IncEx | None = None,
        response_model_exclude: IncEx | None = None,
        response_model_by_alias: bool = True,
        response_model_exclude_unset: bool = False,
        response_model_exclude_defaults: bool = False,
        response_model_exclude_none: bool = False,
        include_in_schema: bool = True,
        response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
        dependency_overrides_provider: Any | None = None,
        callbacks: list[BaseRoute] | None = None,
        openapi_extra: dict[str, Any] | None = None,
        generate_unique_id_function: Callable[["APIRoute"], str]
        | DefaultPlaceholder = Default(generate_unique_id),
        strict_content_type: bool | DefaultPlaceholder = Default(True),
    ) -> None:
        self.path = path
        self.endpoint = endpoint
        self.stream_item_type: Any | None = None
        if isinstance(response_model, DefaultPlaceholder):
            return_annotation = get_typed_return_annotation(endpoint)
            if lenient_issubclass(return_annotation, Response):
                response_model = None
            else:
                stream_item = get_stream_item_type(return_annotation)
                if stream_item is not None:
                    if (
                        isinstance(response_class, DefaultPlaceholder)
                        or lenient_issubclass(response_class, EventSourceResponse)
                    ) and not lenient_issubclass(stream_item, ServerSentEvent):
                        self.stream_item_type = stream_item
                    response_model = None
                else:
                    response_model = return_annotation
        self.response_model = response_model
        self.summary = summary
        self.response_description = response_description
        self.deprecated = deprecated
        self.operation_id = operation_id
        self.response_model_include = response_model_include
        self.response_model_exclude = response_model_exclude
        self.response_model_by_alias = response_model_by_alias
        self.response_model_exclude_unset = response_model_exclude_unset
        self.response_model_exclude_defaults = response_model_exclude_defaults
        self.response_model_exclude_none = response_model_exclude_none
        self.include_in_schema = include_in_schema
        self.response_class = response_class
        self.dependency_overrides_provider = dependency_overrides_provider
        self.callbacks = callbacks
        self.openapi_extra = openapi_extra
        self.generate_unique_id_function = generate_unique_id_function
        self.strict_content_type = strict_content_type
        self.tags = tags or []
        self.responses = responses or {}
        self.name = get_name(endpoint) if name is None else name
        self.path_regex, self.path_format, self.param_convertors = compile_path(path)
        if methods is None:
            methods = ["GET"]
        self.methods: set[str] = {method.upper() for method in methods}
        if isinstance(generate_unique_id_function, DefaultPlaceholder):
            current_generate_unique_id: Callable[[APIRoute], str] = (
                generate_unique_id_function.value
            )
        else:
            current_generate_unique_id = generate_unique_id_function
        self.unique_id = self.operation_id or current_generate_unique_id(self)
        if isinstance(status_code, IntEnum):
            status_code = int(status_code)
        self.status_code = status_code
        self.response_field: ModelField | None
        if self.response_model:
            assert is_body_allowed_for_status_code(status_code), (
                f"Status code {status_code} must not have a response body"
            )
            response_name = "Response_" + self.unique_id
            self.response_field = create_model_field(
                name=response_name,
                type_=self.response_model,
                mode="serialization",
            )
        else:
            self.response_field = None
        if self.stream_item_type:
            stream_item_name = "StreamItem_" + self.unique_id
            self.stream_item_field: ModelField | None = create_model_field(
                name=stream_item_name,
                type_=self.stream_item_type,
                mode="serialization",
            )
        else:
            self.stream_item_field = None
        self.dependencies = list(dependencies or [])
        self.description = description or inspect.cleandoc(self.endpoint.__doc__ or "")
        self.description = self.description.split("\f")[0].strip()
        response_fields = {}
        for additional_status_code, response in self.responses.items():
            assert isinstance(response, dict), "An additional response must be a dict"
            model = response.get("model")
            if model:
                assert is_body_allowed_for_status_code(additional_status_code), (
                    f"Status code {additional_status_code} must not have a response body"
                )
                response_name = f"Response_{additional_status_code}_{self.unique_id}"
                response_field = create_model_field(
                    name=response_name, type_=model, mode="serialization"
                )
                response_fields[additional_status_code] = response_field
        if response_fields:
            self.response_fields: dict[int | str, ModelField] = response_fields
        else:
            self.response_fields = {}

        assert callable(endpoint), "An endpoint must be a callable"
        self.dependant = get_dependant(
            path=self.path_format, call=self.endpoint, scope="function"
        )
        for depends in self.dependencies[::-1]:
            self.dependant.dependencies.insert(
                0,
                get_parameterless_sub_dependant(depends=depends, path=self.path_format),
            )
        self._flat_dependant = get_flat_dependant(self.dependant)
        self._embed_body_fields = _should_embed_body_fields(
            self._flat_dependant.body_params
        )
        self.body_field = get_body_field(
            flat_dependant=self._flat_dependant,
            name=self.unique_id,
            embed_body_fields=self._embed_body_fields,
        )
        is_generator = (
            self.dependant.is_async_gen_callable or self.dependant.is_gen_callable
        )
        self.is_sse_stream = is_generator and lenient_issubclass(
            response_class, EventSourceResponse
        )
        self.is_json_stream = is_generator and isinstance(
            response_class, DefaultPlaceholder
        )
        self.app = request_response(self.get_route_handler())

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        return get_request_handler(
            RouteHandlerConfig(
                dependant=self.dependant,
                body_field=self.body_field,
                status_code=self.status_code,
                response_class=self.response_class,
                response_field=self.response_field,
                response_model_include=self.response_model_include,
                response_model_exclude=self.response_model_exclude,
                response_model_by_alias=self.response_model_by_alias,
                response_model_exclude_unset=self.response_model_exclude_unset,
                response_model_exclude_defaults=self.response_model_exclude_defaults,
                response_model_exclude_none=self.response_model_exclude_none,
                dependency_overrides_provider=self.dependency_overrides_provider,
                embed_body_fields=self._embed_body_fields,
                strict_content_type=self.strict_content_type,
                stream_item_field=self.stream_item_field,
                is_json_stream=self.is_json_stream,
            )
        )

    def matches(self, scope: Scope) -> tuple[Match, Scope]:
        match, child_scope = super().matches(scope)
        if match != Match.NONE:
            child_scope["route"] = self
        return match, child_scope
