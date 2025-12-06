from typing import Union

from fastapi import FastAPI
from fastapi.temp_pydantic_v1_params import Body
from pydantic.v1 import BaseModel
from typing_extensions import Annotated


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    size: float


app = FastAPI()


@app.post("/items/")
async def create_item(item: Annotated[Item, Body(embed=True)]) -> Item:
    return item
