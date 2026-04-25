from __future__ import annotations

from collections.abc import AsyncIterator
from typing import Annotated, Any

from annotated_doc import Doc
from pydantic import AfterValidator, BaseModel, Field, model_validator
from starlette.background import BackgroundTask
from starlette.responses import StreamingResponse
from starlette.types import Receive, Scope, Send

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

# Sentinel object to represent an unset retry value.
_UNSET = object()

# Seconds between keep-alive pings when a generator is idle.
# Private but importable so tests can monkeypatch it.
_PING_INTERVAL: float = 15.0

# Keep-alive comment, per the SSE spec recommendation
KEEPALIVE_COMMENT = b": ping\n\n"


class EventSourceResponse(StreamingResponse):
    """Streaming response implementing the Server-Sent Events (SSE) protocol.

    Use as ``response_class=EventSourceResponse`` on a *path operation* that uses ``yield``
    to enable SSE responses.

    Works with **any HTTP method** (``GET``, ``POST``, etc.), which makes it compatible
    with protocols like MCP that stream SSE over ``POST``.

    When used directly (not via the routing-layer generator shortcut), pass an async
    iterator of :class:`ServerSentEvent` objects or raw bytes::

        @app.get("/feed")
        async def feed():
            return EventSourceResponse(_event_stream())

        async def _event_stream() -> AsyncIterator[ServerSentEvent]:
            yield ServerSentEvent(data="hello", event="greeting")

    Parameters
    ----------
    content:
        An async or sync iterator yielding :class:`ServerSentEvent` objects or raw
        bytes.  When yielding ``ServerSentEvent`` objects they are automatically
        encoded into SSE wire format.
    retry:
        Default reconnection time in **milliseconds** sent to the client after every
        event that does not override it.  Tells the browser how long to wait before
        reconnecting if the connection is lost.
    ping_interval:
        Seconds between keep-alive comment pings when the generator is idle.
        Set to ``0`` to disable.  Default is 15 seconds.
    """

    media_type = "text/event-stream"

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        background: BackgroundTask | None = None,
        retry: int | None | object = _UNSET,
        ping_interval: float = _PING_INTERVAL,
    ) -> None:
        # Wrap the content iterator to auto-encode ServerSentEvent objects.
        self._retry: int | None = (
            retry if retry is not _UNSET and retry is not None else None
        )
        self._ping_interval: float = ping_interval

        encoded_content = self._encode_content(content) if content is not None else ()

        merged_headers: dict[str, str] = {
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
        if headers:
            merged_headers.update(headers)

        super().__init__(
            content=encoded_content,
            status_code=status_code,
            headers=merged_headers,
            media_type=self.media_type,
            background=background,
        )

    # ------------------------------------------------------------------
    # Encoding helpers
    # ------------------------------------------------------------------

    async def _encode_content(
        self,
        content: Any,
    ) -> AsyncIterator[bytes]:
        """Iterate *content* and yield SSE-encoded bytes.

        Each item is expected to be a :class:`ServerSentEvent` (encoded
        automatically) or already-raw bytes (passed through).
        """

        if hasattr(content, "__aiter__"):
            async for item in content:
                yield self._encode_one(item)
        else:
            for item in content:
                yield self._encode_one(item)

    def _encode_one(self, item: Any) -> bytes:
        """Encode a single item into SSE wire format bytes."""
        from fastapi.sse import ServerSentEvent, format_sse_event

        if isinstance(item, ServerSentEvent):
            return self._encode_sse(item)
        elif isinstance(item, bytes):
            return item
        elif isinstance(item, str):
            return item.encode("utf-8")
        else:
            # Fallback: treat as a dict-like object — JSON-encode as data.
            data_str = self._serialize_data(item)
            return format_sse_event(
                data_str=data_str,
                retry=self._retry,
            )

    def _encode_sse(self, event: ServerSentEvent) -> bytes:
        """Encode a :class:`ServerSentEvent` into SSE wire-format bytes."""
        from fastapi.sse import format_sse_event

        if event.raw_data is not None:
            data_str: str | None = event.raw_data
        elif event.data is not None:
            if hasattr(event.data, "model_dump_json"):
                data_str = event.data.model_dump_json()
            else:
                data_str = self._serialize_data(event.data)
        else:
            data_str = None

        # Use the event's own retry if set, otherwise fall back to the
        # response-level default.
        retry: int | None = event.retry if event.retry is not None else self._retry

        return format_sse_event(
            data_str=data_str,
            event=event.event,
            id=event.id,
            retry=retry,
            comment=event.comment,
        )

    @staticmethod
    def _serialize_data(data: Any) -> str:
        """Serialize an arbitrary data payload to a JSON string."""
        import json

        from fastapi.encoders import jsonable_encoder

        data = jsonable_encoder(data)
        return json.dumps(data)

    # ------------------------------------------------------------------
    # Disconnect detection
    # ------------------------------------------------------------------

    async def disconnect(self) -> bool:
        """Wait for the client to disconnect and return ``True``.

        Use this inside an endpoint to wait until the client closes the
        connection, allowing clean shutdown of background tasks::

            @app.get("/stream")
            async def stream():
                response = EventSourceResponse(_events())
                await response.disconnect()  # blocks until client leaves
                await cleanup()
                return response
        """
        await self.listen_for_disconnect(self._receive)
        return True

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """ASGI entry-point.  Stores *receive* so :meth:`disconnect` works."""
        self._receive = receive
        await super().__call__(scope, receive, send)

    # ------------------------------------------------------------------
    # Static convenience methods (automatic event formatting)
    # ------------------------------------------------------------------

    @staticmethod
    def encode(
        data: Any | None = None,
        *,
        event: str | None = None,
        id: str | None = None,
        retry: int | None = None,
        comment: str | None = None,
    ) -> bytes:
        """Encode an event into SSE wire-format bytes.

        This is a convenience wrapper around :func:`format_sse_event` that
        automatically JSON-serializes the ``data`` argument.

        Parameters
        ----------
        data:
            Any JSON-serializable value.  Strings are quoted on the wire.
        event:
            Optional event type name.
        id:
            Optional event ID.
        retry:
            Optional reconnection time in milliseconds.
        comment:
            Optional comment text (ignored by browsers).
        """
        from fastapi.sse import format_sse_event

        if data is not None:
            if hasattr(data, "model_dump_json"):
                data_str = data.model_dump_json()
            else:
                data_str = EventSourceResponse._serialize_data(data)
        else:
            data_str = None

        return format_sse_event(
            data_str=data_str,
            event=event,
            id=id,
            retry=retry,
            comment=comment,
        )

    @staticmethod
    def encode_raw(
        raw_data: str,
        *,
        event: str | None = None,
        id: str | None = None,
        retry: int | None = None,
        comment: str | None = None,
    ) -> bytes:
        """Encode raw (non-JSON) data into SSE wire-format bytes.

        The ``raw_data`` string is placed into the ``data:`` field as-is
        without JSON encoding.
        """
        from fastapi.sse import format_sse_event

        return format_sse_event(
            data_str=raw_data,
            event=event,
            id=id,
            retry=retry,
            comment=comment,
        )

    @staticmethod
    def encode_comment(text: str) -> bytes:
        """Encode an SSE comment.

        Comments start with ``:`` on the wire and are ignored by
        ``EventSource`` clients.  Useful for keep-alive pings.
        """
        from fastapi.sse import format_sse_event

        return format_sse_event(comment=text)


def _check_id_no_null(v: str | None) -> str | None:
    if v is not None and "\0" in v:
        raise ValueError("SSE 'id' must not contain null characters")
    return v


class ServerSentEvent(BaseModel):
    """Represents a single Server-Sent Event.

    When `yield`ed from a *path operation function* that uses
    `response_class=EventSourceResponse`, each `ServerSentEvent` is encoded
    into the [SSE wire format](https://html.spec.whatwg.org/multipage/server-sent-events.html#parsing-an-event-stream)
    (`text/event-stream`).

    If you yield a plain object (dict, Pydantic model, etc.) instead, it is
    automatically JSON-encoded and sent as the `data:` field.

    All `data` values **including plain strings** are JSON-serialized.

    For example, `data="hello"` produces `data: "hello"` on the wire (with
    quotes).
    """

    data: Annotated[
        Any,
        Doc(
            """
            The event payload.

            Can be any JSON-serializable value: a Pydantic model, dict, list,
            string, number, etc. It is **always** serialized to JSON: strings
            are quoted (`"hello"` becomes `data: "hello"` on the wire).

            Mutually exclusive with `raw_data`.
            """
        ),
    ] = None
    raw_data: Annotated[
        str | None,
        Doc(
            """
            Raw string to send as the `data:` field **without** JSON encoding.

            Use this when you need to send pre-formatted text, HTML fragments,
            CSV lines, or any non-JSON payload. The string is placed directly
            into the `data:` field as-is.

            Mutually exclusive with `data`.
            """
        ),
    ] = None
    event: Annotated[
        str | None,
        Doc(
            """
            Optional event type name.

            Maps to `addEventListener(event, ...)` on the browser. When omitted,
            the browser dispatches on the generic `message` event.
            """
        ),
    ] = None
    id: Annotated[
        str | None,
        AfterValidator(_check_id_no_null),
        Doc(
            """
            Optional event ID.

            The browser sends this value back as the `Last-Event-ID` header on
            automatic reconnection. **Must not contain null (`\\0`) characters.**
            """
        ),
    ] = None
    retry: Annotated[
        int | None,
        Field(ge=0),
        Doc(
            """
            Optional reconnection time in **milliseconds**.

            Tells the browser how long to wait before reconnecting after the
            connection is lost. Must be a non-negative integer.
            """
        ),
    ] = None
    comment: Annotated[
        str | None,
        Doc(
            """
            Optional comment line(s).

            Comment lines start with `:` in the SSE wire format and are ignored by
            `EventSource` clients. Useful for keep-alive pings to prevent
            proxy/load-balancer timeouts.
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
            Pre-serialized data string to use as the `data:` field.
            """
        ),
    ] = None,
    event: Annotated[
        str | None,
        Doc(
            """
            Optional event type name (`event:` field).
            """
        ),
    ] = None,
    id: Annotated[
        str | None,
        Doc(
            """
            Optional event ID (`id:` field).
            """
        ),
    ] = None,
    retry: Annotated[
        int | None,
        Doc(
            """
            Optional reconnection time in milliseconds (`retry:` field).
            """
        ),
    ] = None,
    comment: Annotated[
        str | None,
        Doc(
            """
            Optional comment line(s) (`:` prefix).
            """
        ),
    ] = None,
) -> bytes:
    """Build SSE wire-format bytes from **pre-serialized** data.

    The result always ends with `\n\n` (the event terminator).
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
