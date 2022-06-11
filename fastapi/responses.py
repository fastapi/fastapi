from typing import Any

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
    import simplejson
except ImportError:  # pragma: nocover
    simplejson = None  # type: ignore


class UJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        assert ujson is not None, "ujson must be installed to use UJSONResponse"
        return ujson.dumps(content, ensure_ascii=False).encode("utf-8")


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content)


class SimpleJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert (
            simplejson is not None
        ), "simplejson must be installed to use SimpleJSONResponse"
        return simplejson.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            use_decimal=True,
        ).encode("utf-8")
