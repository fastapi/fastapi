import pytest
from fastapi import FastAPI
from pydantic import BaseModel


def test_invalid_sequence():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: list[Item]):
            pass  # pragma: no cover


def test_invalid_tuple():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: tuple[Item, Item]):
            pass  # pragma: no cover


def test_invalid_dict():
    with pytest.raises(AssertionError):
        app = FastAPI()

        class Item(BaseModel):
            title: str

        @app.get("/items/{id}")
        def read_items(id: dict[str, Item]):
            pass  # pragma: no cover


def test_invalid_simple_list():
    with pytest.raises(AssertionError):
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: list):
            pass  # pragma: no cover


def test_invalid_simple_tuple():
    with pytest.raises(AssertionError):
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: tuple):
            pass  # pragma: no cover


def test_invalid_simple_set():
    with pytest.raises(AssertionError):
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: set):
            pass  # pragma: no cover


def test_invalid_simple_dict():
    with pytest.raises(AssertionError):
        app = FastAPI()

        @app.get("/items/{id}")
        def read_items(id: dict):
            pass  # pragma: no cover
