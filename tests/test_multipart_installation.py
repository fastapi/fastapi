import pytest
from fastapi import FastAPI, Form


def test_incorrect_multipart_installed(monkeypatch):
    def raise_attribute_error(*args):
        raise ModuleNotFoundError

    monkeypatch.setattr(
        "multipart.QuerystringParser", raise_attribute_error, raising=False
    )
    with pytest.raises(RuntimeError):
        app = FastAPI()

        @app.post("/login")
        async def login(username: str = Form(...)):
            return {"username": username}  # pragma: nocover


def test_no_multipart_installed(monkeypatch):
    def raise_attribute_error(*args):
        raise ImportError

    monkeypatch.setattr(
        "multipart.QuerystringParser", raise_attribute_error, raising=False
    )
    with pytest.raises(RuntimeError):
        app = FastAPI()

        @app.post("/login")
        async def login(username: str = Form(...)):
            return {"username": username}  # pragma: nocover
