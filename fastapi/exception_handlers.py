import math
from collections.abc import Callable
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.websockets import WebSocket
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import WS_1008_POLICY_VIOLATION


def _encode_error_detail_float(value: float) -> float | str:
    # JSONResponse uses allow_nan=False; keep finite floats numeric and stringify
    # non-finite ones so validation errors can still surface the rejected input.
    if math.isfinite(value):
        return value
    return repr(value)


_VALIDATION_ERROR_ENCODERS: dict[Any, Callable[[Any], Any]] = {
    float: _encode_error_detail_float,
}


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        {"detail": exc.detail}, status_code=exc.status_code, headers=headers
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "detail": jsonable_encoder(
                exc.errors(), custom_encoder=_VALIDATION_ERROR_ENCODERS
            )
        },
    )


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    await websocket.close(
        code=WS_1008_POLICY_VIOLATION,
        reason=jsonable_encoder(
            exc.errors(), custom_encoder=_VALIDATION_ERROR_ENCODERS
        ),
    )
