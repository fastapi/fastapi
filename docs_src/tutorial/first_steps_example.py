from typing import List

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


@app.get("/items/", response_model=List[Item])
async def read_items():
    return [
        {"name": "Item 1", "description": "Desc 1", "price": 10.0, "tax": 0.5},
        {"name": "Item 2", "description": "Desc 2", "price": 20.0, "tax": 1.0},
    ]
