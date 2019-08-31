from typing import Any, Sequence

from pydantic import ValidationError
from pydantic.error_wrappers import ErrorList
from requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.websockets import WebSocket


class HTTPException(StarletteHTTPException):
    def __init__(
        self, status_code: int, detail: Any = None, headers: dict = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


class RequestValidationError(ValidationError):
    def __init__(self, errors: Sequence[ErrorList]) -> None:
        super().__init__(errors, Request)


class WebSocketRequestValidationError(ValidationError):
    def __init__(self, errors: Sequence[ErrorList]) -> None:
        super().__init__(errors, WebSocket)
