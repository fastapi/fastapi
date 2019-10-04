from typing import Callable, List

from fastapi import Body, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response


class ValidationErrorLoggingRoute(APIRoute):
    def get_app(self) -> Callable:
        original_app = super().get_app()

        async def custom_app(request: Request) -> Response:
            try:
                return await original_app(request)
            except RequestValidationError as exc:
                body = await request.body()
                detail = {"errors": exc.errors(), "body": body.decode()}
                raise HTTPException(status_code=422, detail=detail)

        return custom_app


app = FastAPI()
app.router.route_class = ValidationErrorLoggingRoute


@app.post("/")
async def sum_numbers(numbers: List[int] = Body(...)):
    return sum(numbers)
