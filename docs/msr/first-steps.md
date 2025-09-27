from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

app = FastAPI()

@app.get("/items/", response_model=List[Item])
async def read_items():
    return [{"name": "Foo", "price": 50.2}]
