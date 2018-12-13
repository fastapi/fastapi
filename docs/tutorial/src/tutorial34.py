from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Schema

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = Schema(None, title="The description of the item", max_length=300)
    price: float = Schema(..., gt=0, description="The price must be greater than zero")
    tax: float = None


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item = Body(..., embed=True),
):
    results = {"item_id": item_id, "item": item}
    return results
