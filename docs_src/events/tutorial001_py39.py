from contextlib import asynccontextmanager

from fastapi import FastAPI

items = {}


@asynccontextmanager
async def lifespan(app):
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]
