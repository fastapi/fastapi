import time

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class ProcessTimeHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response: Response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response


app = FastAPI()
app.add_middleware(ProcessTimeHeaderMiddleware)


@app.get("/")
def hello():
    return {"hello": "world"}