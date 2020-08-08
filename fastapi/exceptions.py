from typing import Any, Dict, Optional, Sequence

from fastapi.utils import PYDANTIC_1
from pydantic import ValidationError, create_model
from pydantic.error_wrappers import ErrorList
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from starlette.websockets import WebSocket


class HTTPException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail)
        self.headers = headers


RequestErrorModel = create_model("Request")
WebSocketErrorModel = create_model("WebSocket")


class FastAPIError(RuntimeError):
    """
    A generic, FastAPI-specific error.
    """


class RequestValidationError(ValidationError):
    def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
        self.body = body
        if PYDANTIC_1:
            super().__init__(errors, RequestErrorModel)
        else:
            super().__init__(errors, Request)  # type: ignore  # pragma: nocover


class WebSocketRequestValidationError(ValidationError):
    def __init__(self, errors: Sequence[ErrorList]) -> None:
        if PYDANTIC_1:
            super().__init__(errors, WebSocketErrorModel)
        else:
            super().__init__(errors, WebSocket)  # type: ignore  # pragma: nocover
