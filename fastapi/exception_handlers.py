from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import (
    RequestInvalidContentTypeException,
    RequestValidationError,
)
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers:
        return JSONResponse(
            {"detail": exc.detail}, status_code=exc.status_code, headers=headers
        )
    else:
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors())},
    )


async def request_invalid_content_type_exception_handler(
    request: Request, exc: RequestInvalidContentTypeException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
