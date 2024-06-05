from app.core.config import settings
from fastapi import Request
from starlette.datastructures import MutableHeaders
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class CookieToAuth2Middleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)
        self.app = app

    async def dispatch(self, request: Request, call_next) -> None:
        token = request.cookies.get(settings.COOKIE_NAME)
        if token:
            new_headers = MutableHeaders(request._headers)
            new_headers["Authorization"] = f"Bearer {token}"
            request._headers = new_headers
            request.scope.update(headers=request.headers.raw)
        response = await call_next(request)
        return response
