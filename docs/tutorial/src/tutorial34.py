from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
from typing import Set

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item,
):
    results = {"item_id": item_id, "item": item}
    return results
