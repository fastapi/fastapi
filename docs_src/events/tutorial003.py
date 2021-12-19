from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app):
    print("startup")
    yield
    print("shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def hello():
    return {"result": "hello world"}
