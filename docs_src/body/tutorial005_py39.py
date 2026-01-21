from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    description: Optional[str]

@app.post("/items/")
async def create_item(item: Item):
    return item
