from typing import List, Set

from pydantic import BaseModel
from pydantic.types import UrlStr

from fastapi import FastAPI

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
    image: List[Image] = None


class Offer(BaseModel):
    name: str
    description: str = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(*, offer: Offer):
    return offer
