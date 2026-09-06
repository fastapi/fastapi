import time

from fastapi import FastAPI, Request
from fastapi.datastructures import MutableHeaders
from fastapi.middleware.asgi import ASGIMiddleware

app = FastAPI()


class ProcessTimeMiddleware(ASGIMiddleware):
    async def on_request(self, request: Request) -> None:
        request.state.start_time = time.perf_counter()

    async def on_response(
        self, request: Request, status_code: int, headers: MutableHeaders
    ) -> None:
        process_time = time.perf_counter() - request.state.start_time
        headers["X-Process-Time"] = str(process_time)


app.add_middleware(ProcessTimeMiddleware)


@app.get("/")
async def main():
    return "Hello World"
