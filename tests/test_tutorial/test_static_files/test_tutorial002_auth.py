import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from tests.utils import workdir_lock


@pytest.fixture(scope="module")
def client():
    private_dir: Path = Path(os.getcwd()) / "private_files"
    private_dir.mkdir(exist_ok=True)
    sample_file = private_dir / "secret.txt"
    sample_file.write_text("This is a private file.")
    from docs_src.static_files.tutorial002_auth_py310 import app

    with TestClient(app) as client:
        yield client
    sample_file.unlink()
    private_dir.rmdir()


@workdir_lock
def test_without_auth(client: TestClient):
    response = client.get("/private/secret.txt")
    assert response.status_code == 401, response.text


@workdir_lock
def test_with_valid_auth(client: TestClient):
    response = client.get(
        "/private/secret.txt",
        headers={"Authorization": "Bearer mysecrettoken"},
    )
    assert response.status_code == 200, response.text
    assert response.text == "This is a private file."
