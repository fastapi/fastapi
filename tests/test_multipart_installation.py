import warnings

import pytest
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.dependencies.utils import (
    _version_str_to_tuple,
    multipart_incorrect_install_error,
    multipart_not_installed_error,
)


def test_incorrect_multipart_installed_form(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.multipart.parse_options_header", raising=False)
    with pytest.raises(RuntimeError, match=multipart_incorrect_install_error):
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form()):
            return username  # pragma: nocover


def test_incorrect_multipart_installed_file_upload(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.multipart.parse_options_header", raising=False)
    with pytest.raises(RuntimeError, match=multipart_incorrect_install_error):
        app = FastAPI()

        @app.post("/")
        async def root(f: UploadFile = File()):
            return f  # pragma: nocover


def test_incorrect_multipart_installed_file_bytes(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.multipart.parse_options_header", raising=False)
    with pytest.raises(RuntimeError, match=multipart_incorrect_install_error):
        app = FastAPI()

        @app.post("/")
        async def root(f: bytes = File()):
            return f  # pragma: nocover


def test_incorrect_multipart_installed_multi_form(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.multipart.parse_options_header", raising=False)
    with pytest.raises(RuntimeError, match=multipart_incorrect_install_error):
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form(), password: str = Form()):
            return username  # pragma: nocover


def test_incorrect_multipart_installed_form_file(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.multipart.parse_options_header", raising=False)
    with pytest.raises(RuntimeError, match=multipart_incorrect_install_error):
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form(), f: UploadFile = File()):
            return username  # pragma: nocover


def test_no_multipart_installed(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.__version__", raising=False)
        with pytest.raises(RuntimeError, match=multipart_not_installed_error):
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form()):
                return username  # pragma: nocover


def test_no_multipart_installed_file(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.__version__", raising=False)
        with pytest.raises(RuntimeError, match=multipart_not_installed_error):
            app = FastAPI()

            @app.post("/")
            async def root(f: UploadFile = File()):
                return f  # pragma: nocover


def test_no_multipart_installed_file_bytes(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.__version__", raising=False)
        with pytest.raises(RuntimeError, match=multipart_not_installed_error):
            app = FastAPI()

            @app.post("/")
            async def root(f: bytes = File()):
                return f  # pragma: nocover


def test_no_multipart_installed_multi_form(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.__version__", raising=False)
        with pytest.raises(RuntimeError, match=multipart_not_installed_error):
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form(), password: str = Form()):
                return username  # pragma: nocover


def test_no_multipart_installed_form_file(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        monkeypatch.delattr("multipart.__version__", raising=False)
        with pytest.raises(RuntimeError, match=multipart_not_installed_error):
            app = FastAPI()

            @app.post("/")
            async def root(username: str = Form(), f: UploadFile = File()):
                return username  # pragma: nocover


def test_old_multipart_installed(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.12")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form()):
            return username  # pragma: nocover


def test_new_multipart_version_without_multipart_alias(monkeypatch):
    monkeypatch.setattr("python_multipart.__version__", "0.0.100")
    with warnings.catch_warnings(record=True):
        warnings.simplefilter("always")
        app = FastAPI()

        @app.post("/")
        async def root(username: str = Form()):
            return username  # pragma: nocover


def test_version_str_to_tuple():
    assert _version_str_to_tuple("0.0.12") == (0, 0, 12)
    assert _version_str_to_tuple("0.0.100") == (0, 0, 100)
    assert _version_str_to_tuple("1.2.3a1") == (1, 2, 3)
    assert _version_str_to_tuple("") == ()
