from typing import Union

from fastapi import FastAPI
from pydantic.v1 import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
