from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel as BaseModelV2
from pydantic.v1 import BaseModel


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float


class ItemV2(BaseModelV2):
    name: str
    description: Union[str, None] = None
    size: float


app = FastAPI()


@app.post("/items/", response_model=ItemV2)
async def create_item(item: Item):
    return item
