import pytest
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.dependencies.utils import multipart_not_installed_error


def test_no_multipart_installed(monkeypatch):
    monkeypatch.delattr("python_multipart.__version__", raising=False)
    with pytest.raises(RuntimeError, match=multipart_not_installed_error):
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form()):
            return username  # pragma: nocover


def test_no_multipart_installed_file(monkeypatch):
    monkeypatch.delattr("python_multipart.__version__", raising=False)
    with pytest.raises(RuntimeError, match=multipart_not_installed_error):
        app = FastAPI()

        @app.post("/")
        async def root(f: UploadFile = File()):
            return f  # pragma: nocover


def test_no_multipart_installed_file_bytes(monkeypatch):
    monkeypatch.delattr("python_multipart.__version__", raising=False)
    with pytest.raises(RuntimeError, match=multipart_not_installed_error):
        app = FastAPI()

        @app.post("/")
        async def root(f: bytes = File()):
            return f  # pragma: nocover


def test_no_multipart_installed_multi_form(monkeypatch):
    monkeypatch.delattr("python_multipart.__version__", raising=False)
    with pytest.raises(RuntimeError, match=multipart_not_installed_error):
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form(), password: str = Form()):
            return username  # pragma: nocover


def test_no_multipart_installed_form_file(monkeypatch):
    monkeypatch.delattr("python_multipart.__version__", raising=False)
    with pytest.raises(RuntimeError, match=multipart_not_installed_error):
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form(), f: UploadFile = File()):
            return username  # pragma: nocover
