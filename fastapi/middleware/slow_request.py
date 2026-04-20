import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

logger = logging.getLogger("fastapi")


class SlowRequestMiddleware(BaseHTTPMiddleware):
    """
    Middleware to monitor slow requests and log warnings when they exceed the threshold.
    """

    def __init__(self, app: ASGIApp, threshold: float = 0.5) -> None:
        """
        Initialize the SlowRequestMiddleware.

        Args:
            app: The ASGI application.
            threshold: The threshold in seconds for considering a request as slow.
                Defaults to 0.5 seconds (500ms).
        """
        super().__init__(app)
        self.threshold = threshold

    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Dispatch the request, measuring the time taken.

        Args:
            request: The incoming request.
            call_next: The next middleware or endpoint handler.

        Returns:
            The response from the next middleware or endpoint handler.
        """
        start_time = time.perf_counter()
        try:
            response = await call_next(request)
            return response
        finally:
            duration = time.perf_counter() - start_time
            if duration > self.threshold:
                method = request.method
                url = str(request.url)
                logger.warning(
                    f"Slow request: {method} {url} took {duration:.2f}s (threshold: {self.threshold:.2f}s)"
                )
