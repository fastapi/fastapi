from typing import Any, Type

from starlette.responses import FileResponse  # noqa
from starlette.responses import HTMLResponse  # noqa
from starlette.responses import JSONResponse  # noqa
from starlette.responses import PlainTextResponse  # noqa
from starlette.responses import RedirectResponse  # noqa
from starlette.responses import Response  # noqa
from starlette.responses import StreamingResponse  # noqa
from starlette.responses import UJSONResponse  # noqa

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class ORJSONResponse(JSONResponse):
    media_type = "application/json"
    option: int = 0

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content, option=self.option)


def create_or_json_class(options: int = 0) -> Type[ORJSONResponse]:
    """
    Create a new ORJsonResponse class with additional options.
    """

    class _ORJSONResponse(ORJSONResponse):
        option = options

    return _ORJSONResponse
