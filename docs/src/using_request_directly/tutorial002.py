import gzip
from typing import Callable, List

from fastapi import Body, FastAPI
from fastapi.routing import APIRoute
from starlette.requests import Request
from starlette.responses import Response


class GzipRequest(Request):
    async def body(self) -> bytes:
        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.getlist("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body


class GzipRoute(APIRoute):
    def get_app(self) -> Callable:
        original_app = super().get_app()

        async def custom_app(request: Request) -> Response:
            request = GzipRequest(request.scope, request.receive)
            return await original_app(request)

        return custom_app


app = FastAPI()
app.router.route_class = GzipRoute


@app.post("/sum")
async def sum_numbers(numbers: List[int] = Body(...)):
    return {"sum": sum(numbers)}
