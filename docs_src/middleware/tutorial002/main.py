from fastapi import FastAPI

from .middleware import ProcessTimeHeaderMiddleware

app = FastAPI()

app.add_middleware(ProcessTimeHeaderMiddleware, header_name="X-Process-Time")
