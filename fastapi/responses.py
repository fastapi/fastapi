from typing import Any

from starlette.responses import FileResponse  # noqa
from starlette.responses import HTMLResponse  # noqa
from starlette.responses import JSONResponse  # noqa
from starlette.responses import PlainTextResponse  # noqa
from starlette.responses import RedirectResponse  # noqa
from starlette.responses import Response  # noqa
from starlette.responses import StreamingResponse  # noqa

try:
    import ujson
except ImportError:  # pragma: nocover
    ujson = None  # type: ignore


try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class UJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content)
