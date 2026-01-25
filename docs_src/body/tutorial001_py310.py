from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@asynccontextmanager
async def lifespan(app):
    yield


app = FastAPI(lifespan=lifespan)


@app.post("/items/")
async def create_item(item: Item):
    return item
