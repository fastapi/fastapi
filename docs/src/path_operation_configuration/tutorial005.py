from typing import Set

from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []


@app.post(
    "/items/",
    response_model=Item,
    summary="Create an item",
    response_description="The created item",
)
async def create_item(*, item: Item):
    """
    Create an item with all the information:
    
    * name: each item must have a name
    * description: a long description
    * price: required
    * tax: if the item doesn't have tax, you can omit this
    * tags: a set of unique tag strings for this item
    """
    return item
