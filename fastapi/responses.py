from typing import Any

import json

from starlette.responses import FileResponse as FileResponse  # noqa
from starlette.responses import HTMLResponse as HTMLResponse  # noqa
from starlette.responses import JSONResponse as JSONResponse  # noqa
from starlette.responses import PlainTextResponse as PlainTextResponse  # noqa
from starlette.responses import RedirectResponse as RedirectResponse  # noqa
from starlette.responses import Response as Response  # noqa
from starlette.responses import StreamingResponse as StreamingResponse  # noqa

try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore


try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


try:
    import bson  # type: ignore[import-untyped]
except ImportError:  # pragma: nocover
    bson = None


try:
    import bsonjs  # type: ignore[import-untyped]
except ImportError:  # pragma: nocover
    bsonjs = None


class UJSONResponse(JSONResponse):
    """
    JSON response using the high-performance ujson library to serialize data to JSON.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    def render(self, content: Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


class ORJSONResponse(JSONResponse):
    """
    JSON response using the high-performance orjson library to serialize data to JSON.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(
            content, option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY
        )


class BSONResponse(Response):
    """
    BSON response using the current Python bson library for data serialization.

    Note: This is a temporary solution. Soon, a custom Rust wrapper will be implemented for BSON serialization/deserialization to improve performance and reliability.

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    media_type = "application/bson"

    def render(self, content: Any) -> Any:
        assert bson is not None, "bson must be installed to use BSONResponse"
        return bson.dumps(content)


class BSONJSResponse(BSONResponse):
    """
    BSON response using the C-backed python-bsonjs library to serialize BSON

    Read more about it in the
    [FastAPI docs for Custom Response - HTML, Stream, File, others](https://fastapi.tiangolo.com/advanced/custom-response/).
    """

    media_type = "application/bson"

    def render(self, content: Any) -> Any:
        assert bsonjs is not None, "bsonjs must be installed to use BSONJSResponse"
        return bsonjs.loads(json.dumps(content))
