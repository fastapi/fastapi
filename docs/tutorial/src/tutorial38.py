from fastapi import Body, FastAPI, Path, Query
from pydantic import BaseModel
from pydantic.types import UrlStr
from typing import Set, List

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
