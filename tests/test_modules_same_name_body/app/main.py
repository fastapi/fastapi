from fastapi import FastAPI

from . import a, b

app = FastAPI()

app.include_router(a.router, prefix="/a")
app.include_router(b.router, prefix="/b")
