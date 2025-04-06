from typing import Any

from starlette.responses import (  # noqa: F401
    FileResponse,                 # noqa: F401
    HTMLResponse,                 # noqa: F401
    JSONResponse,                 # noqa: F401
    PlainTextResponse,           # noqa: F401
    RedirectResponse,            # noqa: F401
    Response,                    # noqa: F401
    StreamingResponse,           # noqa: F401
)


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

    def render(self, content: Any) -> bytes:
        if ujson is None:
            raise RuntimeError("ujson must be installed to use UJSONResponse")
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


class ORJSONResponse(JSONResponse):
    """
    JSON response using the high-performance orjson library to serialize data to JSON.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    def render(self, content: Any) -> bytes:
        print("Inside the render my boi")
        if orjson is None:
            raise RuntimeError("orjson must be installed to use ORJSONResponse")
        return orjson.dumps(
            content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
        )
