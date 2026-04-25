from __future__ import annotations

import json
from collections.abc import AsyncIterable, Callable, Iterable
from functools import partial
from typing import Annotated, Any

import anyio
from annotated_doc import Doc
from pydantic import AfterValidator, BaseModel, Field, model_validator
from starlette.concurrency import iterate_in_threadpool
from starlette.requests import ClientDisconnect
from starlette.responses import StreamingResponse
from starlette.types import Receive, Scope, Send

try:
    from starlette._utils import collapse_excgroups
except ImportError:
    # Fallback for older starlette versions
    import contextlib

    @contextlib.contextmanager
    def collapse_excgroups():
        yield


# Canonical SSE event schema matching the OpenAPI 3.2 spec
# (Section 4.14.4 "Special Considerations for Server-Sent Events")
_SSE_EVENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "data": {"type": "string"},
        "event": {"type": "string"},
        "id": {"type": "string"},
        "retry": {"type": "integer", "minimum": 0},
    },
}


class EventSourceResponse(StreamingResponse):
    """Streaming response with ``text/event-stream`` media type.

    Use as ``response_class=EventSourceResponse`` on a *path operation* that
    uses ``yield`` to enable Server-Sent Events (SSE) responses via the
    routing layer's automatic encoding.

    Can also be used **directly as a return value**, similar to
    ``StreamingResponse``, by passing an async iterable of pre-formatted
    SSE bytes or ``ServerSentEvent`` objects::

        @app.get("/stream")
        def stream_events():
            return EventSourceResponse(my_event_generator(), retry=3000)

    When used directly the class formats ``ServerSentEvent`` objects into
    SSE wire format, emits an optional initial ``retry:`` field, and
    inserts keep-alive comment pings on idle periods.

    **Parameters**

    * ``content`` – async iterable of ``ServerSentEvent`` objects or raw
      ``bytes``.  Required for direct-use mode; omit when used as
      ``response_class`` (the routing layer provides content).
    * ``retry`` – default reconnection time in **milliseconds**. Emitted
      as an initial ``retry:`` field.  Individual ``ServerSentEvent``
      objects can override per-event.
    * ``ping_interval`` – seconds between keep-alive ``: ping`` comments
      in direct-use mode.  Set to ``0`` to disable.  Default ``15.0``.
    * ``disconnect_callback`` – async callable invoked when the client
      disconnects.  Useful for resource cleanup.
    """

    media_type = "text/event-stream"

    def __init__(
        self,
        content: AsyncIterable[Any] | None = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        background: Any = None,
        retry: int | None = None,
        ping_interval: float = 15.0,
        disconnect_callback: (
            Callable[[], Any] | None  # sync or async callable
        ) = None,
    ) -> None:
        if retry is not None and retry < 0:
            raise ValueError("retry must be non-negative")

        # When content is provided (direct-use mode), wrap it to auto-format
        # ServerSentEvent objects, emit an initial retry field, and add
        # keepalive pings.  Also set SSE-appropriate headers.
        if content is not None:
            content = _wrap_content(content, retry=retry, ping_interval=ping_interval)
            if headers is None:
                headers = {}
            headers.setdefault("Cache-Control", "no-cache")
            # Prevent Nginx and other proxies from buffering SSE
            headers.setdefault("X-Accel-Buffering", "no")

            # Store callback and content flag for __call__
            self._disconnect_callback = disconnect_callback
            self._direct_use = True
        else:
            self._disconnect_callback = None
            self._direct_use = False

        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] == "websocket":
            send = self._wrap_websocket_denial_send(send)
            await self.stream_response(send)
            if self.background is not None:
                await self.background()
            return

        if not self._direct_use or self._disconnect_callback is None:
            # Routing-layer mode or no callback: delegate to parent
            await super().__call__(scope, receive, send)
            return

        # Direct-use mode with disconnect callback
        spec_version = tuple(
            map(int, scope.get("asgi", {}).get("spec_version", "2.0").split("."))
        )

        if spec_version >= (2, 4):
            try:
                await self.stream_response(send)
            except OSError:
                cb = self._disconnect_callback
                if cb is not None:
                    result = cb()
                    if result is not None and hasattr(result, "__await__"):
                        await result
                raise ClientDisconnect()
        else:
            with collapse_excgroups():
                async with anyio.create_task_group() as task_group:

                    async def wrap(
                        func: Callable[[], Any],
                    ) -> None:
                        await func()
                        task_group.cancel_scope.cancel()

                    task_group.start_soon(wrap, partial(self.stream_response, send))
                    await wrap(
                        partial(
                            _listen_for_disconnect,
                            receive,
                            task_group,
                            self._disconnect_callback,
                        )
                    )

        if self.background is not None:
            await self.background()


async def _listen_for_disconnect(
    receive: Receive,
    task_group: anyio.abc.TaskGroup,
    callback: Callable[[], Any] | None,
) -> None:
    """Listen for disconnect, invoke callback, then cancel the task group."""
    while True:
        message = await receive()
        if message["type"] == "http.disconnect":
            break
    if callback is not None:
        result = callback()
        if result is not None and hasattr(result, "__await__"):
            await result
    task_group.cancel_scope.cancel()


def _wrap_content(
    content: AsyncIterable[Any] | Iterable[Any],
    *,
    retry: int | None,
    ping_interval: float,
) -> AsyncIterable[bytes]:
    """Wrap content to auto-format ServerSentEvent objects and emit an
    initial ``retry:`` field if configured.

    When ``ping_interval > 0``, a keep-alive comment is inserted whenever
    the source generator is idle for longer than the interval.
    """
    if isinstance(content, AsyncIterable):
        ait: AsyncIterable[Any] = content
    else:
        ait = iterate_in_threadpool(content)

    if ping_interval <= 0:
        # No keepalive needed: simple generator
        async def _simple_generator() -> AsyncIterable[bytes]:
            if retry is not None:
                yield format_sse_event(retry=retry)
            async for event in ait:
                yield _format_one(event)
                await anyio.sleep(0)

        return _simple_generator()

    # Keepalive-enabled: use anyio memory stream to decouple
    # the producer from the timeout logic.
    send_stream, receive_stream = anyio.create_memory_object_stream[bytes](
        max_buffer_size=1
    )

    async def _format_and_send() -> None:
        async with send_stream:
            if retry is not None:
                await send_stream.send(format_sse_event(retry=retry))
            async for event in ait:
                await send_stream.send(_format_one(event))
                await anyio.sleep(0)

    async def _insert_pings() -> AsyncIterable[bytes]:
        async with receive_stream:
            try:
                while True:
                    try:
                        with anyio.fail_after(ping_interval):
                            data = await receive_stream.receive()
                        yield data
                    except TimeoutError:
                        yield KEEPALIVE_COMMENT
            except anyio.EndOfStream:
                pass

    # We need to return an async iterable that starts the producer task
    # when iterated. Use a wrapper async generator.
    async def _keepalive_generator() -> AsyncIterable[bytes]:
        async with anyio.create_task_group() as tg:
            tg.start_soon(_format_and_send)
            async for chunk in _insert_pings():
                yield chunk
                await anyio.sleep(0)
            tg.cancel_scope.cancel()

    return _keepalive_generator()


def _format_one(event: Any) -> bytes:
    """Format a single event into SSE wire-format bytes."""
    if isinstance(event, ServerSentEvent):
        if event.raw_data is not None:
            data_str: str | None = event.raw_data
        elif event.data is not None:
            if hasattr(event.data, "model_dump_json"):
                data_str = event.data.model_dump_json()
            else:
                data_str = json.dumps(jsonable_encoder(event.data))
        else:
            data_str = None
        return format_sse_event(
            data_str=data_str,
            event=event.event,
            id=event.id,
            retry=event.retry,
            comment=event.comment,
        )
    else:
        # Plain bytes or string (already formatted by user)
        if isinstance(event, bytes):
            return event
        if isinstance(event, str):
            return event.encode("utf-8")
        # Unexpected type — try to convert
        return str(event).encode("utf-8")


def jsonable_encoder(obj: Any) -> Any:
    """Minimal jsonable_encoder fallback for standalone use."""
    from fastapi.encoders import jsonable_encoder as _enc

    return _enc(obj)


def _check_id_no_null(v: str | None) -> str | None:
    if v is not None and "\0" in v:
        raise ValueError("SSE 'id' must not contain null characters")
    return v


class ServerSentEvent(BaseModel):
    """Represents a single Server-Sent Event.

    When ``yield``ed from a *path operation function* that uses
    ``response_class=EventSourceResponse``, each ``ServerSentEvent`` is
    encoded into the `SSE wire format
    <https://html.spec.whatwg.org/multipage/server-sent-events.html#parsing-an-event-stream>`_
    (``text/event-stream``).

    If you yield a plain object (dict, Pydantic model, etc.) instead, it is
    automatically JSON-encoded and sent as the ``data:`` field.

    All ``data`` values **including plain strings** are JSON-serialized.

    For example, ``data="hello"`` produces ``data: "hello"`` on the wire
    (with quotes).
    """

    data: Annotated[
        Any,
        Doc(
            """
            The event payload.

            Can be any JSON-serializable value: a Pydantic model, dict, list,
            string, number, etc. It is **always** serialized to JSON: strings
            are quoted (``"hello"`` becomes ``data: "hello"`` on the wire).

            Mutually exclusive with ``raw_data``.
            """
        ),
    ] = None
    raw_data: Annotated[
        str | None,
        Doc(
            """
            Raw string to send as the ``data:`` field **without** JSON
            encoding.

            Use this when you need to send pre-formatted text, HTML
            fragments, CSV lines, or any non-JSON payload. The string is
            placed directly into the ``data:`` field as-is.

            Mutually exclusive with ``data``.
            """
        ),
    ] = None
    event: Annotated[
        str | None,
        Doc(
            """
            Optional event type name.

            Maps to ``addEventListener(event, ...)`` on the browser. When
            omitted, the browser dispatches on the generic ``message``
            event.
            """
        ),
    ] = None
    id: Annotated[
        str | None,
        AfterValidator(_check_id_no_null),
        Doc(
            """
            Optional event ID.

            The browser sends this value back as the ``Last-Event-ID``
            header on automatic reconnection. **Must not contain null
            (``\\0``) characters.**
            """
        ),
    ] = None
    retry: Annotated[
        int | None,
        Field(ge=0),
        Doc(
            """
            Optional reconnection time in **milliseconds**.

            Tells the browser how long to wait before reconnecting after
            the connection is lost. Must be a non-negative integer.
            """
        ),
    ] = None
    comment: Annotated[
        str | None,
        Doc(
            """
            Optional comment line(s).

            Comment lines start with ``:`` in the SSE wire format and are
            ignored by ``EventSource`` clients. Useful for keep-alive
            pings to prevent proxy/load-balancer timeouts.
            """
        ),
    ] = None

    @model_validator(mode="after")
    def _check_data_exclusive(self) -> ServerSentEvent:
        if self.data is not None and self.raw_data is not None:
            raise ValueError(
                "Cannot set both 'data' and 'raw_data' on the same "
                "ServerSentEvent. Use 'data' for JSON-serialized payloads "
                "or 'raw_data' for pre-formatted strings."
            )
        return self


def format_sse_event(
    *,
    data_str: Annotated[
        str | None,
        Doc(
            """
            Pre-serialized data string to use as the ``data:`` field.
            """
        ),
    ] = None,
    event: Annotated[
        str | None,
        Doc(
            """
            Optional event type name (``event:`` field).
            """
        ),
    ] = None,
    id: Annotated[
        str | None,
        Doc(
            """
            Optional event ID (``id:`` field).
            """
        ),
    ] = None,
    retry: Annotated[
        int | None,
        Doc(
            """
            Optional reconnection time in milliseconds (``retry:`` field).
            """
        ),
    ] = None,
    comment: Annotated[
        str | None,
        Doc(
            """
            Optional comment line(s) (``:`` prefix).
            """
        ),
    ] = None,
) -> bytes:
    """Build SSE wire-format bytes from **pre-serialized** data.

    The result always ends with ``\\n\\n`` (the event terminator).
    """
    lines: list[str] = []

    if comment is not None:
        for line in comment.splitlines():
            lines.append(f": {line}")

    if event is not None:
        lines.append(f"event: {event}")

    if data_str is not None:
        for line in data_str.splitlines():
            lines.append(f"data: {line}")

    if id is not None:
        lines.append(f"id: {id}")

    if retry is not None:
        lines.append(f"retry: {retry}")

    lines.append("")
    lines.append("")
    return "\n".join(lines).encode("utf-8")


# Keep-alive comment, per the SSE spec recommendation
KEEPALIVE_COMMENT = b": ping\n\n"

# Seconds between keep-alive pings when a generator is idle.
# Private but importable so tests can monkeypatch it.
_PING_INTERVAL: float = 15.0
