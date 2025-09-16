from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.websockets import WebSocket
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY, WS_1008_POLICY_VIOLATION


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
    app = request.app
    if getattr(app, "redact_error_details", False):
        # Generic message to avoid leaking validation internals
        content = {"detail": "Request validation failed"}
    else:
        content = {"detail": jsonable_encoder(exc.errors())}
    return JSONResponse(status_code=HTTP_422_UNPROCESSABLE_ENTITY, content=content)


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    app = websocket.app
    if getattr(app, "redact_error_details", False):
        reason = "WebSocket validation failed"
    else:
        reason = jsonable_encoder(exc.errors())
    await websocket.close(code=WS_1008_POLICY_VIOLATION, reason=reason)
