from typing import Any, Dict, Optional, Sequence, Type

from pydantic import BaseModel, ValidationError, create_model
from pydantic._internal._typing_extra import all_literal_values
from pydantic_core import InitErrorDetails, PydanticCustomError
from pydantic_core.core_schema import ErrorType

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


def _prepare_errors(errors: Sequence[Any]) -> list[InitErrorDetails]:
    # return errors
    result: list[InitErrorDetails] = []
    known_errors = set(all_literal_values(ErrorType))
    for error in errors:
        assert isinstance(error, dict)
        if error['type'] in known_errors:
            result.append(error)
        else:
            new_error = error.copy()
            new_error["type"] = PydanticCustomError(error["type"], error["msg"])
            result.append(new_error)
    return result


class RequestValidationError(Exception):
    # TODO (pv2)
    # def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
    def __init__(self, errors: Sequence[Any], *, body: Any = None) -> None:
        self.body = body
        self.pydantic_validation_error = ValidationError.from_exception_data(
            "Request", _prepare_errors(errors)
        )

    def errors(self) -> Sequence[Any]:
        return self.pydantic_validation_error.errors()


class WebSocketRequestValidationError(Exception):
    # TODO (pv2)
    # def __init__(self, errors: Sequence[ErrorList]) -> None:
    def __init__(self, errors: Sequence[Any]) -> None:
        self.pydantic_validation_error = ValidationError.from_exception_data(
            "WebSocket", errors
        )

    def errors(self) -> Sequence[Any]:
        return self.pydantic_validation_error.errors()


class ResponseValidationError(Exception):
    # TODO (pv2)
    # def __init__(self, errors: Sequence[ErrorList], *, body: Any = None) -> None:
    def __init__(self, errors: Sequence[Any], *, body: Any = None) -> None:
        self.body = body
        self.pydantic_validation_error = ValidationError.from_exception_data(
            "Response", errors
        )

    def errors(self) -> Sequence[Any]:
        return self.pydantic_validation_error.errors()

    def __repr__(self):
        return repr(self.pydantic_validation_error)
