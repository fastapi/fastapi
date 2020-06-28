from os import stat_result
from typing import Any, Union

from starlette.background import BackgroundTask
from starlette.datastructures import URL
from starlette.responses import FileResponse as StarletteFileResponse  # noqa
from starlette.responses import HTMLResponse  # noqa
from starlette.responses import JSONResponse  # noqa
from starlette.responses import PlainTextResponse  # noqa
from starlette.responses import RedirectResponse as StarletteRedirectResponse  # noqa
from starlette.responses import Response  # noqa
from starlette.responses import StreamingResponse  # noqa
from starlette.responses import UJSONResponse  # noqa

try:
    import orjson
except ImportError:  # pragma: nocover
    orjson = None  # type: ignore


class ORJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: Any) -> bytes:
        assert orjson is not None, "orjson must be installed to use ORJSONResponse"
        return orjson.dumps(content)


class RedirectResponse(StarletteRedirectResponse):
    def __init__(
        self,
        url: Union[str, URL] = None, status_code: int = 307, headers: dict = None,
        background: BackgroundTask = None, content: Union[str, URL] = None
    ) -> None:
        self.background = background
        super().__init__(url or content, status_code, headers)


class FileResponse(StarletteFileResponse):
    def __init__(
        self,
        path: str = None,
        status_code: int = 200,
        headers: dict = None,
        media_type: str = None,
        background: BackgroundTask = None,
        filename: str = None,
        stat_result: stat_result = None,
        method: str = None,
        content: str = None
    ) -> None:
        super().__init__(path or content, status_code, headers, media_type,
                         background, filename, stat_result, method)
