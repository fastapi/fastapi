import time
from typing import Callable

from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response


class TimedRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            before = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - before
            response.headers["X-Response-Time"] = str(duration)
            print(f"route duration: {duration}")
            print(f"route response: {response}")
            print(f"route response headers: {response.headers}")
            return response

        return custom_route_handler


app = FastAPI()
router = APIRouter(route_class=TimedRoute)


@app.get("/")
async def not_timed():
    return {"message": "Not timed"}


@router.get("/timed")
async def timed():
    return {"message": "It's the time of my life"}


app.include_router(router)
