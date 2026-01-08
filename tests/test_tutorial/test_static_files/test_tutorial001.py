import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    static_dir: Path = Path(os.getcwd()) / "static"
    static_dir.mkdir(exist_ok=True)
    sample_file = static_dir / "sample.txt"
    sample_file.write_text("This is a sample static file.")
    from docs_src.static_files.tutorial001_py39 import app

    with TestClient(app) as client:
        yield client
    sample_file.unlink()
    static_dir.rmdir()


def test_static_files(client: TestClient):
    response = client.get("/static/sample.txt")
    assert response.status_code == 200, response.text
    assert response.text == "This is a sample static file."


def test_static_files_not_found(client: TestClient):
    response = client.get("/static/non_existent_file.txt")
    assert response.status_code == 404, response.text


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {},
    }
