from contextlib import asynccontextmanager

from fastapi import FastAPI

items: dict[str, str] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    items["message"] = "Tomato"
    yield
    items.clear()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": items["message"]}
