from typing import Any, AsyncGenerator, Literal

from fastapi.exceptions import FastAPIDeprecationWarning
from starlette.responses import FileResponse as FileResponse  # noqa
from starlette.responses import HTMLResponse as HTMLResponse  # noqa
from starlette.responses import JSONResponse as JSONResponse  # noqa
from starlette.responses import PlainTextResponse as PlainTextResponse  # noqa
from starlette.responses import RedirectResponse as RedirectResponse  # noqa
from starlette.responses import Response as Response  # noqa
from starlette.responses import StreamingResponse as StreamingResponse  # noqa
from typing_extensions import deprecated


class SSEResponse(StreamingResponse):
    """Streaming response for Server-Sent Events (SSE).

    This response class automatically formats events according to the SSE
    specification and provides convenient methods for sending events.

    Read more about Server-Sent Events in the
    [FastAPI docs](https://fastapi.tiangolo.com/advanced/streaming-responses/#server-sent-events).

    Example:
    ```python
    from fastapi import FastAPI
    from fastapi.responses import SSEResponse

    app = FastAPI()

    @app.get("/events")
    def events():
        def event_generator():
            yield {"event": "message", "data": "Hello"}
            yield {"event": "message", "data": "World"}

        return SSEResponse(event_generator())
    ```
    """

    default_media_type: str = "text/event-stream"

    def __init__(
        self,
        content: AsyncGenerator[str, None] | AsyncGenerator[dict, None],
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
        background: Any = None,
        retry: int | None = None,
    ) -> None:
        self._retry = retry
        super().__init__(
            content=self._wrap_content(content),
            status_code=status_code,
            headers=headers,
            media_type=media_type or self.default_media_type,
            background=background,
        )

    async def _wrap_content(
        self,
        content: AsyncGenerator[str, None] | AsyncGenerator[dict, None],
    ) -> AsyncGenerator[bytes, None]:
        """Wrap the content to format SSE events."""
        async for item in content:
            if isinstance(item, dict):
                yield self._format_event(item).encode("utf-8")
            else:
                yield item.encode("utf-8")

    def _format_event(self, event_data: dict[str, Any]) -> str:
        """Format a dictionary as an SSE event."""
        lines = []

        if "event" in event_data:
            lines.append(f"event: {event_data['event']}")

        if "data" in event_data:
            data = event_data["data"]
            if isinstance(data, (list, dict)):
                import json

                data = json.dumps(data)
            for line in str(data).split("\n"):
                lines.append(f"data: {line}")

        if "id" in event_data:
            lines.append(f"id: {event_data['id']}")

        if "retry" in event_data:
            lines.append(f"retry: {event_data['retry']}")
        elif self._retry is not None:
            lines.append(f"retry: {self._retry}")

        lines.append("")
        return "\n".join(lines)


async def sse_content(
    iterator: AsyncGenerator[dict[str, Any], None],
) -> AsyncGenerator[str, None]:
    """Helper to create SSE-formatted content from a dictionary iterator.

    This is a convenience function that yields pre-formatted SSE strings,
    useful when you want full control over the event formatting.

    Example:
    ```python
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse, sse_content

    app = FastAPI()

    @app.get("/events")
    async def events():
        async def generator():
            yield {"event": "message", "data": "Hello"}
            yield {"data": "World"}

        return StreamingResponse(sse_content(generator()), media_type="text/event-stream")
    ```
    """
    async for event in iterator:
        lines = []

        if "event" in event:
            lines.append(f"event: {event['event']}")

        if "data" in event:
            data = event["data"]
            if isinstance(data, (list, dict)):
                import json

                data = json.dumps(data)
            for line in str(data).split("\n"):
                lines.append(f"data: {line}")

        if "id" in event:
            lines.append(f"id: {event['id']}")

        if "retry" in event:
            lines.append(f"retry: {event['retry']}")

        lines.append("")
        yield "\n".join(lines)


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
