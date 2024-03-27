from __future__ import annotations

import sys

from ..utils import needs_py310

if sys.version_info > (3, 10):
    from typing import Optional

    from fastapi import FastAPI
    from fastapi.testclient import TestClient
    from pydantic import BaseModel

    from .loging_tool import login_required

    app = FastAPI()
    client = TestClient(app)

    class Item(BaseModel):
        name: str
        description: Optional[str] = None
        price: float
        tax: Optional[float] = None

    @app.get("/items/")
    @login_required
    def get_item(id: int) -> Item:
        return Item(name="name", price=42.42)


@needs_py310
def test_future_6465():
    res = client.get("/items?id=3")
    assert res.status_code == 200
