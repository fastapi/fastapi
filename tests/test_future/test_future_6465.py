from __future__ import annotations

from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

from ..utils import needs_py310
from .login_tool import login_required

app = FastAPI()
client = TestClient(app)


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


@needs_py310
def test_future_6465():
    @app.get("/items/")
    @login_required
    def get_item(item_id: int) -> Item:
        return Item(name="name", price=42.42)

    res = client.get("/items?item_id=3")
    assert res.status_code == 200
