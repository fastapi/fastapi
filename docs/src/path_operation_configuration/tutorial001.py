from typing import Set

from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED

from fastapi import FastAPI

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
