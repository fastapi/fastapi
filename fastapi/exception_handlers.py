from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.datastructures import MutableHeaders
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    headers = getattr(exc, "headers", None)
    if headers is not None:
        headers = MutableHeaders(headers)
        # we need to make sure that "content-length" and "content-type" are not taken from the exception,
        # otherwise we'll have a mismatch between the headers sent and the message
        del headers["content-length"]
        del headers["content-type"]

    if exc.status_code in {204, 304}:
        content = None
        response_cls = Response
    else:
        content = {"detail": exc.detail}
        response_cls = JSONResponse

    return response_cls(content, status_code=exc.status_code, headers=headers)


async def request_validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": jsonable_encoder(exc.errors())},
    )
