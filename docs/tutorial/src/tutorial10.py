from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None


app = FastAPI()

@app.post("/items/")
async def create_item(item: Item):
    return item
