from typing import Any, Dict, Optional, Sequence, Type

from pydantic import BaseModel, ValidationError, create_model

# TODO (pv2)
# from pydantic.error_wrappers import ErrorList
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.exceptions import WebSocketException as WebSocketException  # noqa: F401


class HTTPException(StarletteHTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


RequestErrorModel: Type[BaseModel] = create_model("Request")
WebSocketErrorModel: Type[BaseModel] = create_model("WebSocket")


class FastAPIError(RuntimeError):
    """
    A generic, FastAPI-specific error.
    """


class RequestValidationError(Exception):
    # TODO (pv2)
    # def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
    def __init__(self, errors: Sequence[Any], *, body: Any = None) -> None:
        self.body = body
        self.pydantic_validation_error = ValidationError("Request", errors)

    def errors(self) -> Sequence[Any]:
        return self.pydantic_validation_error.errors()


class WebSocketRequestValidationError(Exception):
    # TODO (pv2)
    # def __init__(self, errors: Sequence[ErrorList]) -> None:
    def __init__(self, errors: Sequence[Any]) -> None:
        self.pydantic_validation_error = ValidationError("WebSocket", errors)

    def errors(self) -> Sequence[Any]:
        return self.pydantic_validation_error.errors()


class ResponseValidationError(Exception):
    # TODO (pv2)
    # def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
    def __init__(self, errors: Sequence[Any], *, body: Any = None) -> None:
        self.body = body
        self.pydantic_validation_error = ValidationError("Response", errors)

    def errors(self) -> Sequence[Any]:
        return self.pydantic_validation_error.errors()
