from typing import Any

from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


class HTTPException(StarletteHTTPException):
    def __init__(
        self, status_code: int, detail: Any = None, headers: dict = None
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


class RequestValidationError(ValidationError):
    pass


class WebSocketRequestValidationError(ValidationError):
    pass
