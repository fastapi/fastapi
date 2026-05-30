from dataclasses import dataclass
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
    """

    media_type = "text/event-stream"


def _check_single_line(v: str | None, field_name: str) -> str | None:
    if v is not None and ("\r" in v or "\n" in v):
        raise ValueError(f"SSE '{field_name}' must be a single line")
    return v


def _check_event_single_line(v: str | None) -> str | None:
    return _check_single_line(v, "event")


def _check_id_valid(v: str | None) -> str | None:
    if v is not None and "\0" in v:
        raise ValueError("SSE 'id' must not contain null characters")
    return _check_single_line(v, "id")


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
        AfterValidator(_check_event_single_line),
        Doc(
            """
            Optional event type name.

            Maps to `addEventListener(event, ...)` on the browser. When omitted,
            the browser dispatches on the generic `message` event. Must be a
            single line.
            """
        ),
    ] = None
    id: Annotated[
        str | None,
        AfterValidator(_check_id_valid),
        Doc(
            """
            Optional event ID.

            The browser sends this value back as the `Last-Event-ID` header on
            automatic reconnection. **Must be a single line** and must not contain
            null (`\\0`) characters.
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


@dataclass(frozen=True)
class ParsedSSEEvent:
    """A Server-Sent Event parsed from the wire format.

    Returned by `parse_sse_events()`. This is the *receiver-side* counterpart
    to [`ServerSentEvent`](#serversentevent) (used to *send* events): `data`
    here is the raw string from the wire (multi-line `data:` lines joined
    with `\\n`), not JSON-decoded. Decoding is up to the caller, since the
    payload may be JSON, plain text, or any other format depending on the
    server.

    Each instance reflects only fields explicitly set in its own event block
    on the wire — `id` and `retry` are not sticky across events here, unlike
    a browser `EventSource` client. Stickiness is left to the caller when
    needed.
    """

    data: Annotated[
        str,
        Doc(
            """
            The event payload — multi-line `data:` lines joined with `\\n`,
            with a single trailing `\\n` stripped per the SSE spec.
            """
        ),
    ]
    event: Annotated[
        str,
        Doc(
            """
            The event type. Defaults to `"message"` when no `event:` field
            is present, matching what an `EventSource` browser client would
            dispatch.
            """
        ),
    ] = "message"
    id: Annotated[
        str | None,
        Doc(
            """
            The event ID from the `id:` field, or `None` if not set on this
            event block. (Not carried over from the previous event.)
            """
        ),
    ] = None
    retry: Annotated[
        int | None,
        Doc(
            """
            The reconnection time in milliseconds from the `retry:` field,
            or `None` if not set on this event block.
            """
        ),
    ] = None


def parse_sse_events(
    raw: Annotated[
        bytes | str,
        Doc(
            """
            SSE wire-format text or bytes. Typically the full body of a
            `text/event-stream` response.
            """
        ),
    ],
) -> list[ParsedSSEEvent]:
    """Parse an SSE event stream into a list of `ParsedSSEEvent` objects.

    Implements the [WHATWG SSE parsing algorithm](https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation)
    for a complete stream. This is the receiver-side counterpart to
    `format_sse_event()`.

    Useful for **tests**, **clients**, or any code that consumes the response
    of an `EventSourceResponse` *path operation*.

    Parsing rules followed (per spec):

    * Lines may be separated by `\\n`, `\\r`, or `\\r\\n`.
    * A leading UTF-8 BOM is stripped.
    * Comment lines (those starting with `:`) are skipped.
    * Multi-line `data:` fields are joined with `\\n`, with a single trailing
      `\\n` stripped.
    * Events with an empty data buffer are not emitted.
    * Unknown field names are ignored.
    * `id` values containing NULL bytes are ignored.
    * `retry` values that aren't decimal integers are ignored.

    Note: this returns events as they appear on the wire. `id` and `retry`
    are **not sticky** across events in the returned list — each
    `ParsedSSEEvent` reflects only the fields seen in its own block.
    """
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")

    # Strip a single leading BOM if present (per spec).
    if raw.startswith("﻿"):
        raw = raw[1:]
    # Normalize line endings: \r\n or \r → \n.
    text = raw.replace("\r\n", "\n").replace("\r", "\n")

    events: list[ParsedSSEEvent] = []
    data_buf: list[str] = []
    event_type: str | None = None
    last_id: str | None = None
    retry: int | None = None

    def _dispatch() -> None:
        nonlocal event_type, last_id, retry
        # Per spec: if the data buffer is empty, do not dispatch the event.
        if not data_buf:
            event_type = None
            return
        data_str = "\n".join(data_buf)
        events.append(
            ParsedSSEEvent(
                data=data_str,
                event=event_type if event_type else "message",
                id=last_id,
                retry=retry,
            )
        )
        data_buf.clear()
        event_type = None
        last_id = None
        retry = None

    for line in text.split("\n"):
        if line == "":
            _dispatch()
            continue
        if line.startswith(":"):
            # Comment line, ignored per spec.
            continue
        if ":" in line:
            field, _, value = line.partition(":")
            # An optional single leading space after the colon is stripped.
            if value.startswith(" "):
                value = value[1:]
        else:
            # A line with no colon is treated as a field with empty value.
            field = line
            value = ""

        if field == "data":
            data_buf.append(value)
        elif field == "event":
            event_type = value
        elif field == "id":
            # Per spec: ignore IDs containing NULL bytes.
            if "\0" not in value:
                last_id = value
        elif field == "retry":
            # Per spec: must be a base-10 integer.
            if value.isdigit():
                retry = int(value)
        # Other fields are ignored per spec.

    return events


# Keep-alive comment, per the SSE spec recommendation
KEEPALIVE_COMMENT = b": ping\n\n"

# Seconds between keep-alive pings when a generator is idle.
# Private but importable so tests can monkeypatch it.
_PING_INTERVAL: float = 15.0
