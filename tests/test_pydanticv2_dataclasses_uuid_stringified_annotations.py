from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Union

from dirty_equals import IsUUID
from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


@dataclass
class Item:
    id: uuid.UUID
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    description: Union[str, None] = None
    tax: Union[float, None] = None


app = FastAPI()


@app.get("/item", response_model=Item)
async def read_item():
    return {
        "id": uuid.uuid4(),
        "name": "Island In The Moon",
        "price": 12.99,
        "description": "A place to be be playin' and havin' fun",
        "tags": ["breater"],
    }


client = TestClient(app)


def test_annotations():
    response = client.get("/item")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "id": IsUUID(),
            "name": "Island In The Moon",
            "price": 12.99,
            "tags": ["breater"],
            "description": "A place to be be playin' and havin' fun",
            "tax": None,
        }
    )
