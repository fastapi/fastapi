import time
from collections.abc import Awaitable, Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp


class TimingMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: ASGIApp,
        header_name: str = "X-Process-Time",
    ) -> None:
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers[self.header_name] = f"{process_time:.4f}"
        return response
