from contextlib import asynccontextmanager

from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app):
    yield
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


app = FastAPI(lifespan=lifespan)


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]
