from collections.abc import AsyncIterable

from fastapi import Depends, FastAPI, Response
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: str | None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]


async def add_stream_headers(response: Response) -> None:
    response.headers["X-Stream-Source"] = "inventory"


@app.get("/items/stream", dependencies=[Depends(add_stream_headers)])
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
