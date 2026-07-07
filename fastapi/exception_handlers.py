from collections.abc import Mapping

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, WebSocketRequestValidationError
from fastapi.problem_details import (
    problem_details_from_http_exception,
    problem_details_from_request_validation,
)
from fastapi.responses import ProblemDetailsResponse
from fastapi.utils import is_body_allowed_for_status_code
from fastapi.websockets import WebSocket
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import WS_1008_POLICY_VIOLATION


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
        content={"detail": jsonable_encoder(exc.errors())},
    )


async def websocket_request_validation_exception_handler(
    websocket: WebSocket, exc: WebSocketRequestValidationError
) -> None:
    await websocket.close(
        code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
    )


def _get_problem_details_config(
    request: Request,
) -> tuple[str | None, Mapping[int | type, str] | None]:
    try:
        app = request.app
    except (AttributeError, KeyError):
        return None, None
    return (
        getattr(app, "problem_type_base_uri", None),
        getattr(app, "problem_types", None),
    )


async def problem_details_http_exception_handler(
    request: Request, exc: HTTPException
) -> Response:
    headers = getattr(exc, "headers", None)
    if not is_body_allowed_for_status_code(exc.status_code):
        return Response(status_code=exc.status_code, headers=headers)
    type_base_uri, problem_types = _get_problem_details_config(request)
    problem = problem_details_from_http_exception(
        exc,
        url=str(request.url),
        type_base_uri=type_base_uri,
        problem_types=problem_types,
    )
    return ProblemDetailsResponse(
        content=problem.model_dump(exclude_none=True),
        status_code=exc.status_code,
        headers=headers,
    )


async def problem_details_request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> ProblemDetailsResponse:
    type_base_uri, problem_types = _get_problem_details_config(request)
    problem = problem_details_from_request_validation(
        exc.errors(),
        url=str(request.url),
        type_base_uri=type_base_uri,
        problem_types=problem_types,
    )
    return ProblemDetailsResponse(
        content=problem.model_dump(exclude_none=True),
        status_code=422,
    )
