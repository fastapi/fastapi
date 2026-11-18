from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException
from starlette.middleware import body_limit
from starlette.middleware.body_limit import (
    MAX_BODY_SIZE_SCOPE_KEY,
    RequestBodyLimitMiddleware,
)
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send

# Starlette has no public exception types for these two middleware signals.
# Unknown exceptions must keep their normal handling.
_response_sent = getattr(body_limit, "_RequestBodyLimitResponseSent", ())
_body_limit_errors = tuple(
    cls
    for cls in (getattr(body_limit, "_RequestBodyTooLarge", None), _response_sent)
    if cls
)


def validate_max_body_size(max_body_size: int | None) -> None:
    if max_body_size is None:
        return
    if (
        isinstance(max_body_size, bool)
        or not isinstance(max_body_size, int)
        or max_body_size < 0
    ):
        raise ValueError("max_body_size must be a non-negative integer or None")


def get_body_size_limit(*limits: int | None) -> int | None:
    for limit in limits:
        if limit is not None:
            return limit
    return None


def get_body_limit_error(exc: Exception) -> Exception | None:
    if isinstance(exc, ExceptionGroup):
        # Middleware can read the body and start the response in concurrent tasks.
        # Only unwrap a group if every error belongs to the body limiter.
        _, other = exc.split(_body_limit_errors)
        if other is not None:
            return None
        # If Starlette already sent the 413, let it finish that response.
        exc = exc.subgroup(_response_sent) or exc
        while isinstance(exc, ExceptionGroup):
            exc = exc.exceptions[0]
    return exc if isinstance(exc, _body_limit_errors) else None


def wrap_app_with_body_limit(app: ASGIApp, max_body_size: int | None) -> ASGIApp:
    if max_body_size is None:
        return app
    return RequestBodyLimitMiddleware(
        _BodyLimitExceptionMiddleware(app), max_body_size=max_body_size
    )


class _BodyLimitExceptionMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        try:
            await self.app(scope, receive, send)
        except ExceptionGroup as exc:
            if scope["type"] == "http" and (error := get_body_limit_error(exc)):
                raise error from exc
            raise


class AppBodyLimitMiddleware:
    def __init__(self, app: ASGIApp, max_body_size: int | None) -> None:
        self.app = wrap_app_with_body_limit(app, max_body_size)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if MAX_BODY_SIZE_SCOPE_KEY not in scope:
            await self.app(scope, receive, send)
            return

        # A mounted app shares the parent's byte counter. Starlette leaves
        # errors to the parent, but our ServerErrorMiddleware would send a 500
        # before they got there.
        started = False

        async def send_response(message: Message) -> None:
            nonlocal started
            if message["type"] == "http.response.start":
                started = True
            await send(message)

        try:
            await self.app(scope, receive, send_response)
        except Exception as exc:
            error = get_body_limit_error(exc)
            if started or not isinstance(error, HTTPException):
                raise
            response = await http_exception_handler(Request(scope, receive), error)
            await response(scope, receive, send)
