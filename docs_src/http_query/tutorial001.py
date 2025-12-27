from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class ItemSearch(BaseModel):
    keyword: str
    min_price: Optional[float] = None
    max_price: Optional[float] = None


@app.query("/items/")
async def search_items(search_params: ItemSearch):
    return {"message": "Searching items", "search_params": search_params}
