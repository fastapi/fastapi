from dataclasses import dataclass
from typing import Optional

from fastapi import FastAPI


@dataclass
class Item:
    name: str
    price: float
    description: Optional[str] = None
    tax: Optional[float] = None


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    return item
