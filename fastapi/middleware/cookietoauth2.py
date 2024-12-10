from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from starlette.types import ASGIApp


class CookieToAuth2Middleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, cookie_name: str) -> None:
        super().__init__(app)
        self.app = app
        self.cookie_name = cookie_name

    async def dispatch(self, request: Request, call_next) -> Response:
        token = request.cookies.get(self.cookie_name)
        if token:
            new_headers = MutableHeaders(request._headers)
            new_headers["Authorization"] = f"Bearer {token}"
            request._headers = new_headers
            request.scope.update(headers=request.headers.raw)
        response = await call_next(request)
        return response
