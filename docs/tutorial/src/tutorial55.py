from typing import Set

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []


@app.post("/items/", response_model=Item, status_code=HTTP_201_CREATED)
async def create_item(*, item: Item):
    return item
