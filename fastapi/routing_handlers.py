import email.message
import json
from collections.abc import AsyncIterator, Callable, Coroutine, Iterator
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, field
from typing import Any, cast

import anyio
from anyio.abc import ObjectReceiveStream
from fastapi import params
from fastapi._compat import ModelField, Undefined, lenient_issubclass
from fastapi.datastructures import Default, DefaultPlaceholder
from fastapi.dependencies.models import Dependant
from fastapi.dependencies.utils import solve_dependencies
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import (
    EndpointContext,
    RequestValidationError,
    ResponseValidationError,
    WebSocketRequestValidationError,
)
from fastapi.routing_utils import (
    build_response_args,
    extract_endpoint_context,
    run_endpoint_function,
    serialize_response,
)
from fastapi.sse import (
    KEEPALIVE_COMMENT,
    EventSourceResponse,
    ServerSentEvent,
    format_sse_event,
)
from fastapi.types import IncEx
from fastapi.utils import is_body_allowed_for_status_code
from starlette.concurrency import iterate_in_threadpool
from starlette.datastructures import FormData
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response, StreamingResponse
from starlette.websockets import WebSocket


def _get_ping_interval() -> float:
    # Keep compatibility with tests/users that patch fastapi.routing._PING_INTERVAL.
    # If not present, fall back to the default defined in fastapi.sse.
    from fastapi import routing as routing_module
    from fastapi.sse import _PING_INTERVAL as default_ping_interval

    return float(getattr(routing_module, "_PING_INTERVAL", default_ping_interval))


@dataclass
class RouteHandlerConfig:
    dependant: Dependant
    body_field: ModelField | None = None
    status_code: int | None = None
    response_class: type[Response] | DefaultPlaceholder = field(
        default_factory=lambda: Default(JSONResponse)
    )
    response_field: ModelField | None = None
    response_model_include: IncEx | None = None
    response_model_exclude: IncEx | None = None
    response_model_by_alias: bool = True
    response_model_exclude_unset: bool = False
    response_model_exclude_defaults: bool = False
    response_model_exclude_none: bool = False
    dependency_overrides_provider: Any | None = None
    embed_body_fields: bool = False
    strict_content_type: bool | DefaultPlaceholder = field(
        default_factory=lambda: Default(True)
    )
    stream_item_field: ModelField | None = None
    is_json_stream: bool = False


def get_request_handler(
    dependant: Dependant | RouteHandlerConfig,
    body_field: ModelField | None = None,
    status_code: int | None = None,
    response_class: type[Response] | DefaultPlaceholder = Default(JSONResponse),
    response_field: ModelField | None = None,
    response_model_include: IncEx | None = None,
    response_model_exclude: IncEx | None = None,
    response_model_by_alias: bool = True,
    response_model_exclude_unset: bool = False,
    response_model_exclude_defaults: bool = False,
    response_model_exclude_none: bool = False,
    dependency_overrides_provider: Any | None = None,
    embed_body_fields: bool = False,
    strict_content_type: bool | DefaultPlaceholder = Default(True),
    stream_item_field: ModelField | None = None,
    is_json_stream: bool = False,
) -> Callable[[Request], Coroutine[Any, Any, Response]]:
    if isinstance(dependant, RouteHandlerConfig):
        config = dependant
    else:
        config = RouteHandlerConfig(
            dependant=dependant,
            body_field=body_field,
            status_code=status_code,
            response_class=response_class,
            response_field=response_field,
            response_model_include=response_model_include,
            response_model_exclude=response_model_exclude,
            response_model_by_alias=response_model_by_alias,
            response_model_exclude_unset=response_model_exclude_unset,
            response_model_exclude_defaults=response_model_exclude_defaults,
            response_model_exclude_none=response_model_exclude_none,
            dependency_overrides_provider=dependency_overrides_provider,
            embed_body_fields=embed_body_fields,
            strict_content_type=strict_content_type,
            stream_item_field=stream_item_field,
            is_json_stream=is_json_stream,
        )
    dependant = config.dependant
    body_field = config.body_field
    status_code = config.status_code
    response_class = config.response_class
    response_field = config.response_field
    response_model_include = config.response_model_include
    response_model_exclude = config.response_model_exclude
    response_model_by_alias = config.response_model_by_alias
    response_model_exclude_unset = config.response_model_exclude_unset
    response_model_exclude_defaults = config.response_model_exclude_defaults
    response_model_exclude_none = config.response_model_exclude_none
    dependency_overrides_provider = config.dependency_overrides_provider
    embed_body_fields = config.embed_body_fields
    strict_content_type = config.strict_content_type
    stream_item_field = config.stream_item_field
    is_json_stream = config.is_json_stream

    assert dependant.call is not None, "dependant.call must be a function"
    is_coroutine = dependant.is_coroutine_callable
    is_body_form = body_field and isinstance(body_field.field_info, params.Form)
    if isinstance(response_class, DefaultPlaceholder):
        actual_response_class: type[Response] = response_class.value
    else:
        actual_response_class = response_class
    is_sse_stream = lenient_issubclass(actual_response_class, EventSourceResponse)
    if isinstance(strict_content_type, DefaultPlaceholder):
        actual_strict_content_type: bool = strict_content_type.value
    else:
        actual_strict_content_type = strict_content_type

    async def app(request: Request) -> Response:
        response: Response | None = None
        file_stack = request.scope.get("fastapi_middleware_astack")
        assert isinstance(file_stack, AsyncExitStack), (
            "fastapi_middleware_astack not found in request scope"
        )

        endpoint_ctx = (
            extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )

        if dependant.path:
            mount_path = request.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"{request.method} {mount_path}{dependant.path}"

        try:
            body: Any = None
            if body_field:
                if is_body_form:
                    body = await request.form()
                    file_stack.push_async_callback(body.close)
                else:
                    body_bytes = await request.body()
                    if body_bytes:
                        json_body: Any = Undefined
                        content_type_value = request.headers.get("content-type")
                        if not content_type_value:
                            if not actual_strict_content_type:
                                json_body = await request.json()
                        else:
                            message = email.message.Message()
                            message["content-type"] = content_type_value
                            if message.get_content_maintype() == "application":
                                subtype = message.get_content_subtype()
                                if subtype == "json" or subtype.endswith("+json"):
                                    json_body = await request.json()
                        if json_body != Undefined:
                            body = json_body
                        else:
                            body = body_bytes
        except json.JSONDecodeError as e:
            validation_error = RequestValidationError(
                [
                    {
                        "type": "json_invalid",
                        "loc": ("body", e.pos),
                        "msg": "JSON decode error",
                        "input": {},
                        "ctx": {"error": e.msg},
                    }
                ],
                body=e.doc,
                endpoint_ctx=endpoint_ctx,
            )
            raise validation_error from e
        except HTTPException:
            raise
        except Exception as e:
            http_error = HTTPException(
                status_code=400, detail="There was an error parsing the body"
            )
            raise http_error from e

        async_exit_stack = request.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        solved_result = await solve_dependencies(
            request=request,
            dependant=dependant,
            body=cast(dict[str, Any] | FormData | bytes | None, body),
            dependency_overrides_provider=dependency_overrides_provider,
            async_exit_stack=async_exit_stack,
            embed_body_fields=embed_body_fields,
        )
        errors = solved_result.errors
        assert dependant.call
        if not errors:

            def _serialize_data(data: Any) -> bytes:
                if stream_item_field:
                    value, errors_ = stream_item_field.validate(
                        data, {}, loc=("response",)
                    )
                    if errors_:
                        ctx = endpoint_ctx or EndpointContext()
                        raise ResponseValidationError(
                            errors=errors_,
                            body=data,
                            endpoint_ctx=ctx,
                        )
                    return stream_item_field.serialize_json(
                        value,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                    )
                data = jsonable_encoder(data)
                return json.dumps(data).encode("utf-8")

            if is_sse_stream:
                gen = dependant.call(**solved_result.values)

                def _serialize_sse_item(item: Any) -> bytes:
                    if isinstance(item, ServerSentEvent):
                        if item.raw_data is not None:
                            data_str: str | None = item.raw_data
                        elif item.data is not None:
                            if hasattr(item.data, "model_dump_json"):
                                data_str = item.data.model_dump_json()
                            else:
                                data_str = json.dumps(jsonable_encoder(item.data))
                        else:
                            data_str = None
                        return format_sse_event(
                            data_str=data_str,
                            event=item.event,
                            id=item.id,
                            retry=item.retry,
                            comment=item.comment,
                        )
                    return format_sse_event(
                        data_str=_serialize_data(item).decode("utf-8")
                    )

                if dependant.is_async_gen_callable:
                    sse_aiter: AsyncIterator[Any] = gen.__aiter__()
                else:
                    sse_aiter = iterate_in_threadpool(gen)

                @asynccontextmanager
                async def _sse_producer_cm() -> AsyncIterator[
                    ObjectReceiveStream[bytes]
                ]:
                    send_stream, receive_stream = anyio.create_memory_object_stream[
                        bytes
                    ](max_buffer_size=1)

                    async def _producer() -> None:
                        async with send_stream:
                            async for raw_item in sse_aiter:
                                await send_stream.send(_serialize_sse_item(raw_item))

                    send_keepalive, receive_keepalive = (
                        anyio.create_memory_object_stream[bytes](max_buffer_size=1)
                    )

                    async def _keepalive_inserter() -> None:
                        async with send_keepalive, receive_stream:
                            try:
                                while True:
                                    try:
                                        with anyio.fail_after(_get_ping_interval()):
                                            data = await receive_stream.receive()
                                        await send_keepalive.send(data)
                                    except TimeoutError:
                                        await send_keepalive.send(KEEPALIVE_COMMENT)
                            except anyio.EndOfStream:
                                pass

                    async with anyio.create_task_group() as tg:
                        tg.start_soon(_producer)
                        tg.start_soon(_keepalive_inserter)
                        yield receive_keepalive
                        tg.cancel_scope.cancel()

                sse_receive_stream = await async_exit_stack.enter_async_context(
                    _sse_producer_cm()
                )
                async_exit_stack.push_async_callback(sse_receive_stream.aclose)

                async def _sse_with_checkpoints(
                    stream: ObjectReceiveStream[bytes],
                ) -> AsyncIterator[bytes]:
                    async for data in stream:
                        yield data
                        await anyio.sleep(0)

                sse_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                    _sse_with_checkpoints(sse_receive_stream)
                )

                response = StreamingResponse(
                    sse_stream_content,
                    media_type="text/event-stream",
                    background=solved_result.background_tasks,
                )
                response.headers["Cache-Control"] = "no-cache"
                response.headers["X-Accel-Buffering"] = "no"
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif is_json_stream:
                gen = dependant.call(**solved_result.values)

                def _serialize_item(item: Any) -> bytes:
                    return _serialize_data(item) + b"\n"

                if dependant.is_async_gen_callable:

                    async def _async_stream_jsonl() -> AsyncIterator[bytes]:
                        async for item in gen:
                            yield _serialize_item(item)
                            await anyio.sleep(0)

                    jsonl_stream_content: AsyncIterator[bytes] | Iterator[bytes] = (
                        _async_stream_jsonl()
                    )
                else:

                    def _sync_stream_jsonl() -> Iterator[bytes]:
                        for item in gen:  # ty: ignore[not-iterable]
                            yield _serialize_item(item)

                    jsonl_stream_content = _sync_stream_jsonl()

                response = StreamingResponse(
                    jsonl_stream_content,
                    media_type="application/jsonl",
                    background=solved_result.background_tasks,
                )
                response.headers.raw.extend(solved_result.response.headers.raw)
            elif dependant.is_async_gen_callable or dependant.is_gen_callable:
                gen = dependant.call(**solved_result.values)
                if dependant.is_async_gen_callable:

                    async def _async_stream_raw(
                        async_gen: AsyncIterator[Any],
                    ) -> AsyncIterator[Any]:
                        async for chunk in async_gen:
                            yield chunk
                            await anyio.sleep(0)

                    gen = _async_stream_raw(gen)
                response_args = build_response_args(
                    status_code=status_code, solved_result=solved_result
                )
                response = actual_response_class(content=gen, **response_args)
                response.headers.raw.extend(solved_result.response.headers.raw)
            else:
                raw_response = await run_endpoint_function(
                    dependant=dependant,
                    values=solved_result.values,
                    is_coroutine=is_coroutine,
                )
                if isinstance(raw_response, Response):
                    if raw_response.background is None:
                        raw_response.background = solved_result.background_tasks
                    response = raw_response
                else:
                    response_args = build_response_args(
                        status_code=status_code, solved_result=solved_result
                    )
                    use_dump_json = response_field is not None and isinstance(
                        response_class, DefaultPlaceholder
                    )
                    content = await serialize_response(
                        field=response_field,
                        response_content=raw_response,
                        include=response_model_include,
                        exclude=response_model_exclude,
                        by_alias=response_model_by_alias,
                        exclude_unset=response_model_exclude_unset,
                        exclude_defaults=response_model_exclude_defaults,
                        exclude_none=response_model_exclude_none,
                        is_coroutine=is_coroutine,
                        endpoint_ctx=endpoint_ctx,
                        dump_json=use_dump_json,
                    )
                    if use_dump_json:
                        response = Response(
                            content=content,
                            media_type="application/json",
                            **response_args,
                        )
                    else:
                        response = actual_response_class(content, **response_args)
                    if not is_body_allowed_for_status_code(response.status_code):
                        response.body = b""
                    response.headers.raw.extend(solved_result.response.headers.raw)
        if errors:
            raise RequestValidationError(errors, body=body, endpoint_ctx=endpoint_ctx)

        assert response
        return response

    return app


def get_websocket_app(
    dependant: Dependant,
    dependency_overrides_provider: Any | None = None,
    embed_body_fields: bool = False,
) -> Callable[[WebSocket], Coroutine[Any, Any, Any]]:
    async def app(websocket: WebSocket) -> None:
        endpoint_ctx = (
            extract_endpoint_context(dependant.call)
            if dependant.call
            else EndpointContext()
        )
        if dependant.path:
            mount_path = websocket.scope.get("root_path", "").rstrip("/")
            endpoint_ctx["path"] = f"WS {mount_path}{dependant.path}"
        async_exit_stack = websocket.scope.get("fastapi_inner_astack")
        assert isinstance(async_exit_stack, AsyncExitStack), (
            "fastapi_inner_astack not found in request scope"
        )
        solved_result = await solve_dependencies(
            request=websocket,
            dependant=dependant,
            dependency_overrides_provider=dependency_overrides_provider,
            async_exit_stack=async_exit_stack,
            embed_body_fields=embed_body_fields,
        )
        if solved_result.errors:
            raise WebSocketRequestValidationError(
                solved_result.errors,
                endpoint_ctx=endpoint_ctx,
            )
        assert dependant.call is not None, "dependant.call must be a function"
        await dependant.call(**solved_result.values)

    return app
