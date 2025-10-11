import time

from fastapi import Request
from fastapi.middleware.base import BaseHTTPMiddleware


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, header_name: str = "X-Process-Time"):
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers[self.header_name] = str(process_time)
        return response
