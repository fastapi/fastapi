from typing import List, Set

from fastapi import FastAPI
from pydantic import BaseModel, UrlStr

app = FastAPI()


class Image(BaseModel):
    url: UrlStr
    name: str


class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: Set[str] = []
    images: List[Image] = None


class Offer(BaseModel):
    name: str
    description: str = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(*, offer: Offer):
    return offer
