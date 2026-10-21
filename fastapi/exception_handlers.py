from collections.abc import Sequence
from typing import Any

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.websockets import WebSocket
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import WS_1008_POLICY_VIOLATION


def _encode_validation_errors(errors: Sequence[Any]) -> list[Any]:
    # An error can carry the raw request body as its `input`, and that body is not
    # always valid UTF-8 (e.g. protobuf sent with a non-JSON content type). Leave
    # such an `input` out, so the client still gets the 422 instead of a 500.
    encoded = []
    for error in errors:
        try:
            encoded.append(jsonable_encoder(error))
        except UnicodeDecodeError:
            encoded.append(
                jsonable_encoder({k: v for k, v in error.items() if k != "input"})
            )
    return encoded


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
        content={"detail": _encode_validation_errors(exc.errors())},
    )


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    await websocket.close(
        code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
    )
