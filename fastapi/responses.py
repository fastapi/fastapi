import inspect
from collections.abc import AsyncIterator, Iterator
from typing import Any

from fastapi.exceptions import FastAPIDeprecationWarning
from starlette.responses import FileResponse as FileResponse  # noqa
from starlette.responses import HTMLResponse as HTMLResponse  # noqa
from starlette.responses import JSONResponse as JSONResponse  # noqa
from starlette.responses import PlainTextResponse as PlainTextResponse  # noqa
from starlette.responses import RedirectResponse as RedirectResponse  # noqa
from starlette.responses import Response as Response  # noqa
from starlette.responses import StreamingResponse as StreamingResponse  # noqa
from typing_extensions import deprecated


def _is_async(obj: Any) -> bool:
    """Check if an object is an async generator or async iterable."""
    return inspect.isasyncgen(obj) or inspect.iscoroutine(obj)


class SSEResponse(StreamingResponse):
    """Server-Sent Events (SSE) response.

    A response subclass that automatically formats events according to the SSE spec.
    Supports automatic event formatting, retry configuration, and client disconnect handling.

    Example:
    ```python
    from fastapi import FastAPI
    from fastapi.responses import SSEResponse
    import asyncio

    app = FastAPI()

    @app.get("/events")
    async def get_events():
        async def event_generator():
            for i in range(5):
                yield {"event": "message", "data": f"Message {i}"}
                await asyncio.sleep(1)

        return SSEResponse(event_generator())
    ```

    Or using the `event_serializer` parameter for simpler data:

    ```python
    @app.get("/events")
    async def get_events():
        async def simple_generator():
            for i in range(5):
                yield f"Message {i}"

        return SSEResponse(simple_generator(), event_serializer=lambda x: {"data": x})
    ```
    """

    default_media_type = "text/event-stream"

    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        background: Any = None,
        encoding: str = "utf-8",
        event_serializer: Any | None = None,
        retry: int | None = None,
    ) -> None:
        self.event_serializer = event_serializer
        self.retry = retry

        # Check if content is async
        if _is_async(content):
            # Create an SSE-formatted async iterator
            async def sse_content() -> AsyncIterator[str]:
                # First yield retry if specified
                if retry is not None:
                    yield f"retry: {retry}\n\n"

                # Then yield formatted events
                async for item in content:
                    # Serialize the event data
                    if event_serializer is not None:
                        event_dict = event_serializer(item)
                    else:
                        event_dict = item

                    # Format as SSE
                    yield format_sse(event_dict)

            super().__init__(
                content=sse_content(),
                status_code=status_code,
                headers=headers,
                media_type=media_type or self.default_media_type,
                background=background,
                encoding=encoding,
            )
        else:
            # Create an SSE-formatted sync iterator
            def sse_content() -> Iterator[str]:
                # First yield retry if specified
                if retry is not None:
                    yield f"retry: {retry}\n\n"

                # Then yield formatted events
                for item in content:
                    # Serialize the event data
                    if event_serializer is not None:
                        event_dict = event_serializer(item)
                    else:
                        event_dict = item

                    # Format as SSE
                    yield format_sse(event_dict)

            super().__init__(
                content=sse_content(),
                status_code=status_code,
                headers=headers,
                media_type=media_type or self.default_media_type,
                background=background,
                encoding=encoding,
            )


def format_sse(
    data: str | dict[str, Any] = "",
    event: str | None = None,
    id: int | str | None = None,
    retry: int | None = None,
) -> str:
    """Format data as a Server-Sent Event.

    Args:
        data: The event data. Can be a string or a dict with 'data', 'event', 'id', 'retry' keys.
        event: The event type (optional).
        id: The event ID (optional).
        retry: The retry interval in milliseconds (optional).

    Returns:
        A properly formatted SSE string.

    Example:
        >>> format_sse(data="Hello")
        'data: Hello\\n\\n'

        >>> format_sse(data={"data": "Hello", "event": "message"})
        'event: message\\ndata: Hello\\n\\n'

        >>> format_sse("Hello", event="greeting", id="1", retry=5000)
        'id: 1\\nevent: greeting\\nretry: 5000\\ndata: Hello\\n\\n'
    """
    # Handle dict input
    if isinstance(data, dict):
        event = data.get("event", event)
        id = data.get("id", id)
        retry = data.get("retry", retry)
        data = data.get("data", "")

    lines = []

    if id is not None:
        lines.append(f"id: {id}")

    if event is not None:
        lines.append(f"event: {event}")

    if retry is not None:
        lines.append(f"retry: {retry}")

    # Data can be multiline - each line should be prefixed with "data: "
    if isinstance(data, str):
        for line in data.split("\n"):
            lines.append(f"data: {line}")
    else:
        lines.append(f"data: {data}")

    # SSE events are separated by double newlines
    return "\n".join(lines) + "\n\n"


try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore


try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


@deprecated(
    "UJSONResponse is deprecated, FastAPI now serializes data directly to JSON "
    "bytes via Pydantic when a return type or response model is set, which is "
    "faster and doesn't need a custom response class. Read more in the FastAPI "
    "docs: https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model "
    "and https://fastapi.tiangolo.com/tutorial/response-model/",
    category=FastAPIDeprecationWarning,
    stacklevel=2,
)
class UJSONResponse(JSONResponse):
    """JSON response using the ujson library to serialize data to JSON.

    **Deprecated**: `UJSONResponse` is deprecated. FastAPI now serializes data
    directly to JSON bytes via Pydantic when a return type or response model is
    set, which is faster and doesn't need a custom response class.

    Read more in the
    [FastAPI docs for Custom Response](https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model)
    and the
    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).

    **Note**: `ujson` is not included with FastAPI and must be installed
    separately, e.g. `pip install ujson`.
    """

    def render(self, content: Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


@deprecated(
    "ORJSONResponse is deprecated, FastAPI now serializes data directly to JSON "
    "bytes via Pydantic when a return type or response model is set, which is "
    "faster and doesn't need a custom response class. Read more in the FastAPI "
    "docs: https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model "
    "and https://fastapi.tiangolo.com/tutorial/response-model/",
    category=FastAPIDeprecationWarning,
    stacklevel=2,
)
class ORJSONResponse(JSONResponse):
    """JSON response using the orjson library to serialize data to JSON.

    **Deprecated**: `ORJSONResponse` is deprecated. FastAPI now serializes data
    directly to JSON bytes via Pydantic when a return type or response model is
    set, which is faster and doesn't need a custom response class.

    Read more in the
    [FastAPI docs for Custom Response](https://fastapi.tiangolo.com/advanced/custom-response/#orjson-or-response-model)
    and the
    [FastAPI docs for Response Model](https://fastapi.tiangolo.com/tutorial/response-model/).

    **Note**: `orjson` is not included with FastAPI and must be installed
    separately, e.g. `pip install orjson`.
    """

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
        )
