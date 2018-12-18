from typing import Set

from pydantic import BaseModel
from pydantic.types import UrlStr

from fastapi import FastAPI

app = FastAPI()


class Image(BaseModel):
    url: UrlStr
    name: str


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []
    image: Image = None


@app.put("/items/{item_id}")
async def update_item(*, item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results
