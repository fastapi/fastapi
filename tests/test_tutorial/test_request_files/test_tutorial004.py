import importlib
import io

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ...utils import needs_py39, needs_py310


@pytest.fixture(
    name="app",
    params=[
        "tutorial004",
        pytest.param("tutorial004_an_py39", marks=needs_py39),
        pytest.param("tutorial004_an_py310", marks=needs_py310),
    ],
)
def get_app(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_files.{request.param}")

    return mod.app


@pytest.fixture(name="client")
def get_client(app: FastAPI):
    client = TestClient(app)
    return client


def test_post_upload_images_valid(client: TestClient):
    # Create fake image files
    file1 = ("test1.jpg", io.BytesIO(b"fake image content"), "image/jpeg")
    file2 = ("test2.png", io.BytesIO(b"another fake image"), "image/png")

    response = client.post(
        "/upload-images/",
        files=[
            ("files", file1),
            ("files", file2),
        ],
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["uploaded"] == 2
    assert len(data["files"]) == 2
    assert data["files"][0]["filename"] == "test1.jpg"
    assert data["files"][0]["content_type"] == "image/jpeg"
    assert data["files"][1]["filename"] == "test2.png"
    assert data["files"][1]["content_type"] == "image/png"


def test_post_upload_images_invalid_type(client: TestClient):
    # Upload a non-image file
    file1 = ("test.txt", io.BytesIO(b"text content"), "text/plain")

    response = client.post(
        "/upload-images/",
        files=[("files", file1)],
    )
    assert response.status_code == 400, response.text
    assert "Invalid file type" in response.json()["detail"]


def test_post_upload_images_too_large(client: TestClient):
    # Create a file larger than 5MB
    large_content = b"x" * (6 * 1024 * 1024)  # 6MB
    file1 = ("large.jpg", io.BytesIO(large_content), "image/jpeg")

    response = client.post(
        "/upload-images/",
        files=[("files", file1)],
    )
    assert response.status_code == 400, response.text
    assert "too large" in response.json()["detail"].lower()


def test_post_upload_images_too_many_files(client: TestClient):
    # Try to upload 11 files (max is 10)
    files = [
        ("files", (f"test{i}.jpg", io.BytesIO(b"content"), "image/jpeg"))
        for i in range(11)
    ]

    response = client.post("/upload-images/", files=files)
    assert response.status_code == 400, response.text
    assert "Too many files" in response.json()["detail"]
