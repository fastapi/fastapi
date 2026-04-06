from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI

app = FastAPI()


def get_potato() -> Potato:
    return Potato(color="red", size=5)


@app.get("/")
async def read_root(potato: Annotated[Potato, Depends(get_potato)]):
    return {"Hello": "World"}


@dataclass
class Potato:
    color: str
    size: int
