from typing import Optional

import pytest
from fastapi import FastAPI, Query
from pydantic import BaseModel


def test_invalid_sequence():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: list[Item] = Query(default=None)):
            pass  # pragma: no cover


def test_invalid_tuple():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: tuple[Item, Item] = Query(default=None)):
            pass  # pragma: no cover


def test_invalid_dict():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: dict[str, Item] = Query(default=None)):
            pass  # pragma: no cover


def test_invalid_simple_dict():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/")
        def read_items(q: Optional[dict] = Query(default=None)):
            pass  # pragma: no cover
