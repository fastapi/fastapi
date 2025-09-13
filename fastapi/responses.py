from typing import Any, Optional

from starlette.responses import FileResponse as StarletteFileResponse
from starlette.responses import HTMLResponse as StarletteHTMLResponse
from starlette.responses import JSONResponse as StarletteJSONResponse
from starlette.responses import PlainTextResponse as StarlettePlainTextResponse
from starlette.responses import RedirectResponse as StarletteRedirectResponse
from starlette.responses import Response as StarletteResponse
from starlette.responses import StreamingResponse as StarletteStreamingResponse


class Response(StarletteResponse):
    default_status_code: int = 200

    def __init__(
        self,
        content: Any = None,
        *,
        status_code: Optional[int] = None,
        **kwargs: Any,
    ) -> None:
        if status_code is None:
            status_code = self.default_status_code
        super().__init__(content=content, status_code=status_code, **kwargs)


class PlainTextResponse(StarlettePlainTextResponse):
    default_status_code = 200


class JSONResponse(StarletteJSONResponse):
    default_status_code = 200


class HTMLResponse(StarletteHTMLResponse):
    default_status_code = 200


class FileResponse(StarletteFileResponse):
    default_status_code = 200


class StreamingResponse(StarletteStreamingResponse):
    default_status_code = 200


class RedirectResponse(StarletteRedirectResponse):
    default_status_code = 307


try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore


try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class UJSONResponse(JSONResponse):
    """
    JSON response using the high-performance ujson library to serialize data to JSON.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    default_status_code = getattr(JSONResponse, "default_status_code", 200)

    def render(self, content: Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


class ORJSONResponse(JSONResponse):
    """
    JSON response using the high-performance orjson library to serialize data to JSON.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    default_status_code = getattr(JSONResponse, "default_status_code", 200)

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
        )
