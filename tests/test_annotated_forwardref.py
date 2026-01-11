from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


def test_annotated_forwardref_dependency():
    app = FastAPI()

    def get_item() -> Item:
        return Item(name="apple")

    @app.get("/")
    def read(item: Annotated[Item, Depends(get_item)]):
        return {"name": item.name}

    @dataclass
    class Item:
        name: str

    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"name": "apple"}
