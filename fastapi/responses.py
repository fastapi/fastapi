from typing import Any

from pydantic import BaseModel
from starlette.responses import FileResponse as FileResponse  # noqa
from starlette.responses import HTMLResponse as HTMLResponse  # noqa
from starlette.responses import JSONResponse as JSONResponse  # noqa
from starlette.responses import PlainTextResponse as PlainTextResponse  # noqa
from starlette.responses import RedirectResponse as RedirectResponse  # noqa
from starlette.responses import Response as Response  # noqa
from starlette.responses import StreamingResponse as StreamingResponse  # noqa
from starlette.responses import UJSONResponse as UJSONResponse  # noqa

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content)


class ModelResponse(JSONResponse):
    """
    A Response that skips validation of Pydantic models and calls directly the json method of the pydantic model
    using it's configured encoder.
    """

    media_type = "application/json"

    def render(self, content: BaseModel) -> bytes:
        return content.json().encode("utf-8")
