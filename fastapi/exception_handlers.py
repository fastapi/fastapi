from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.websockets import WebSocket
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import WS_1008_POLICY_VIOLATION


async def http_exception_handler(request: Request, exc: HTTPException) -> Response:
    """
    Default exception handler for `HTTPException`.

    Returns a JSON response with the exception `detail` and the appropriate
    status code and headers. For status codes that do not allow a response body
    (1xx, 204, 205, 304), a plain `Response` without a body is returned.

    Read more about it in the
    [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
    """
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    return JSONResponse(
        {"detail": exc.detail}, status_code=exc.status_code, headers=headers
    )


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Default exception handler for `RequestValidationError`.

    Returns a 422 JSON response containing the validation error details produced
    when the request data (path parameters, query parameters, headers, or body)
    does not match the endpoint's declared schema.

    Read more about it in the
    [FastAPI docs for Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/#override-request-validation-exceptions).
    """
    return JSONResponse(
        status_code=422,
        content={"detail": jsonable_encoder(exc.errors())},
    )


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    """
    Default exception handler for `WebSocketRequestValidationError`.

    Closes the WebSocket connection with a 1008 (Policy Violation) close code
    and includes the validation error details as the close reason.
    """
    await websocket.close(
        code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
    )
