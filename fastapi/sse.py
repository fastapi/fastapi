from collections.abc import Awaitable, Callable
from typing import Annotated, Any

from annotated_doc import Doc
from pydantic import AfterValidator, BaseModel, Field, model_validator
from starlette.requests import Request
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
    """Streaming response with `text/event-stream` media type for Server-Sent Events (SSE).

    Use as `response_class=EventSourceResponse` on a *path operation* that uses `yield`
    to enable Server Sent Events (SSE) responses.

    Works with **any HTTP method** (`GET`, `POST`, etc.), which makes it compatible
    with protocols like MCP that stream SSE over `POST`.

    The actual encoding logic lives in the FastAPI routing layer. This class
    serves mainly as a marker and sets the correct `Content-Type`.

    ## Features

    - **Automatic event formatting**: Plain objects (dicts, Pydantic models) are
      automatically JSON-encoded and wrapped in SSE format.
    - **Retry configuration**: Set default reconnection time for all events via
      `default_retry` parameter or per-event via `ServerSentEvent.retry`.
    - **Client disconnect handling**: Optional `on_disconnect` callback for cleanup.
    - **Keepalive support**: Automatic keepalive comments to prevent proxy timeouts.

    ## Example

    ```python
    from fastapi import FastAPI
    from fastapi.sse import EventSourceResponse, ServerSentEvent

    app = FastAPI()


    @app.get("/events", response_class=EventSourceResponse)
    async def stream_events():
        for i in range(3):
            yield ServerSentEvent(data={"count": i}, event="update", id=str(i))
    ```

    ## Example with retry configuration

    ```python
    @app.get(
        "/events",
        response_class=EventSourceResponse,
        response_class_kwargs={"default_retry": 3000},
    )
    async def stream_events():
        yield {"message": "Hello"}  # Automatically formatted with retry: 3000
    ```

    ## Example with disconnect callback

    ```python
    async def on_disconnect(request: Request) -> None:
        print("Client disconnected")


    @app.get(
        "/events",
        response_class=EventSourceResponse,
        response_class_kwargs={"on_disconnect": on_disconnect},
    )
    async def stream_events():
        while True:
            yield {"data": "streaming..."}
    ```
    """

    media_type = "text/event-stream"
    default_retry: int | None = None
    on_disconnect: Callable[[Request], Awaitable[None]] | None = None

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        default_retry: int | None = None,
        on_disconnect: Callable[[Request], Awaitable[None]] | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize an EventSourceResponse.

        Args:
            content: An async generator or iterable yielding SSE events.
            status_code: HTTP status code for the response.
            headers: Optional headers to include in the response.
            media_type: Media type (defaults to "text/event-stream").
            default_retry: Default reconnection time in milliseconds for all events.
                Can be overridden per-event via `ServerSentEvent.retry`.
            on_disconnect: Optional async callback invoked when the client disconnects.
                Receives the `Request` object as argument. Useful for cleanup.
            **kwargs: Additional arguments passed to StreamingResponse.
        """
        super().__init__(
            content=content,
            status_code=status_code,
            headers=headers,
            media_type=media_type or self.media_type,
            **kwargs,
        )
        # Store instance-level overrides
        if default_retry is not None:
            self.default_retry = default_retry
        if on_disconnect is not None:
            self.on_disconnect = on_disconnect


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
