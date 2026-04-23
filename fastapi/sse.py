from collections.abc import Awaitable, Callable
from typing import Annotated, Any

from annotated_doc import Doc
from pydantic import AfterValidator, BaseModel, Field, model_validator
from starlette.responses import StreamingResponse

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
    """Streaming response with `text/event-stream` media type.

    Use as `response_class=EventSourceResponse` on a *path operation* that uses `yield`
    to enable Server Sent Events (SSE) responses.

    Works with **any HTTP method** (`GET`, `POST`, etc.), which makes it compatible
    with protocols like MCP that stream SSE over `POST`.

    The actual encoding logic lives in the FastAPI routing layer. This class
    serves mainly as a marker and sets the correct `Content-Type`.

    ## Client Disconnect Handling

    To detect when a client disconnects, pass an `on_disconnect` callback:

    ```python
    async def handle_disconnect():
        # Clean up resources, stop processing, etc.
        pass

    @app.get("/stream", response_class=EventSourceResponse)
    async def stream():
        # The on_disconnect callback will be called if the client disconnects
        yield {"message": "hello"}
    ```

    ## Default Retry Configuration

    Set a default reconnection time for all events:

    ```python
    @app.get(
        "/stream",
        response_class=EventSourceResponse(default_retry=3000)
    )
    async def stream():
        yield {"message": "hello"}  # Will include retry: 3000
    ```
    """

    media_type = "text/event-stream"

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        stream_key: str | None = None,
        default_retry: int | None = None,
        on_disconnect: Callable[[], Awaitable[None] | None] | None = None,
    ) -> None:
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type,
        )
        self.stream_key = stream_key
        self.default_retry = default_retry
        self.on_disconnect = on_disconnect
        # This will be set by the routing layer when the response is prepared
        self._disconnect_called = False

    async def call_disconnect_callback(self) -> None:
        """Call the on_disconnect callback if one was provided.

        This is called by the routing layer when a client disconnect is detected.
        """
        if self.on_disconnect is not None and not self._disconnect_called:
            self._disconnect_called = True
            result = self.on_disconnect()
            if result is not None:
                await result


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
    def _check_data_exclusive(self) -> "ServerSentEvent":
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


# Keep-alive comment, per the SSE spec recommendation
KEEPALIVE_COMMENT = b": ping\n\n"

# Seconds between keep-alive pings when a generator is idle.
# Private but importable so tests can monkeypatch it.
_PING_INTERVAL: float = 15.0


def sse_event(
    data: Any = None,
    *,
    event: str | None = None,
    id: str | None = None,
    retry: int | None = None,
    comment: str | None = None,
    raw_data: str | None = None,
) -> ServerSentEvent:
    """Create a Server-Sent Event with the given parameters.

    This is a convenience function for creating `ServerSentEvent` instances.

    ## Arguments

    - `data`: The event payload. Will be JSON-serialized. Mutually exclusive with `raw_data`.
    - `event`: Optional event type name for `addEventListener(event, ...)` on the client.
    - `id`: Optional event ID. The browser sends this back as `Last-Event-ID` on reconnect.
    - `retry`: Optional reconnection time in milliseconds.
    - `comment`: Optional comment line(s). Ignored by clients, useful for keep-alive.
    - `raw_data`: Raw string to send without JSON encoding. Mutually exclusive with `data`.

    ## Example

    ```python
    from fastapi import FastAPI
    from fastapi.sse import EventSourceResponse, sse_event

    app = FastAPI()

    @app.get("/stream", response_class=EventSourceResponse)
    async def stream():
        yield sse_event(data={"status": "started"}, event="status", id="1")
        yield sse_event(data="Processing...", comment="keep-alive")
        yield sse_event(raw_data="[DONE]", event="end")
    ```
    """
    return ServerSentEvent(
        data=data,
        event=event,
        id=id,
        retry=retry,
        comment=comment,
        raw_data=raw_data,
    )


class SSEStream:
    """Helper class for managing SSE streams with disconnect detection.

    This class provides a convenient way to create SSE streams that can detect
    client disconnects and stop processing early.

    ## Example

    ```python
    from fastapi import FastAPI
    from fastapi.sse import EventSourceResponse, SSEStream

    app = FastAPI()

    @app.get("/stream", response_class=EventSourceResponse)
    async def stream():
        async with SSEStream() as sse:
            for i in range(100):
                if sse.disconnected:
                    break
                yield {"count": i}
                await asyncio.sleep(0.1)
    ```
    """

    def __init__(self) -> None:
        self._disconnected = False

    @property
    def disconnected(self) -> bool:
        """Check if the client has disconnected."""
        return self._disconnected

    def mark_disconnected(self) -> None:
        """Mark the stream as disconnected.

        Called by the routing layer when a disconnect is detected.
        """
        self._disconnected = True

    async def __aenter__(self) -> "SSEStream":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass


def create_sse_stream(
    on_disconnect: Callable[[], Awaitable[None] | None] | None = None,
) -> tuple[SSEStream, EventSourceResponse]:
    """Create an SSE stream helper and response with disconnect handling.

    Returns a tuple of (SSEStream, EventSourceResponse) for use in path operations.

    ## Example

    ```python
    from fastapi import FastAPI
    from fastapi.sse import create_sse_stream

    app = FastAPI()

    @app.get("/stream")
    async def stream():
        sse, response = create_sse_stream(
            on_disconnect=lambda: print("Client disconnected!")
        )
        # Use sse.disconnected to check for disconnects
        # The response will be returned automatically
    ```
    """
    stream = SSEStream()
    response = EventSourceResponse(
        content=None,
        on_disconnect=on_disconnect,
    )
    # Link the stream to the response for disconnect notification
    original_callback = response.on_disconnect

    async def combined_disconnect() -> None:
        stream.mark_disconnected()
        if original_callback is not None:
            result = original_callback()
            if result is not None:
                await result

    response.on_disconnect = combined_disconnect
    return stream, response
