import time
from typing import Callable

from fastapi import FastAPI
from fastapi.routing import APIRouter


class GetsGenerateHeadsRouter(APIRouter):
    def add_api_route(self, path, endpoint, *args, methods=None, **kwargs):
        if methods and "GET" in methods:
            super().add_api_route(path, endpoint, *args, methods=["HEAD"], **kwargs)
        super().add_api_route(path, endpoint, *args, methods=methods, **kwargs)


app = FastAPI(router_class=GetsGenerateHeadsRouter)


@app.get("/via-router-class")
async def via_router_class():
    return {"message": "Welcome to FastAPI!"}


included_router = GetsGenerateHeadsRouter()


@included_router.get("/via-include")
async def via_include():
    return {"message": "Welcome to FastAPI!"}


app.include_router(included_router)
