"""
Test support for SecretBytes type with File() parameter.

This tests that SecretBytes can be used as a file upload type annotation,
similar to how bytes is used, with the content being read from the uploaded file.
Also tests NewType wrappers around bytes and SecretBytes.
"""

from pathlib import Path
from typing import List, NewType, Union

import pytest
from fastapi import FastAPI, File
from fastapi.testclient import TestClient
from pydantic import SecretBytes
from typing_extensions import Annotated

app = FastAPI()

# NewType wrappers for testing
SecretFileBytes = NewType("SecretFileBytes", SecretBytes)
CustomBytes = NewType("CustomBytes", bytes)


@app.post("/secret_file")
def post_secret_file(data: Annotated[SecretBytes, File()]):
    # SecretBytes wraps bytes and provides a get_secret_value() method
    return {"file_size": len(data.get_secret_value())}


@app.post("/secret_file_optional")
def post_secret_file_optional(data: Annotated[Union[SecretBytes, None], File()] = None):
    if data is None:
        return {"file_size": None}
    return {"file_size": len(data.get_secret_value())}


@app.post("/secret_file_default")
def post_secret_file_default(data: SecretBytes = File(default=None)):
    if data is None:
        return {"file_size": None}
    return {"file_size": len(data.get_secret_value())}


@app.post("/secret_file_list")
def post_secret_file_list(files: Annotated[List[SecretBytes], File()]):
    return {"file_sizes": [len(f.get_secret_value()) for f in files]}


@app.post("/newtype_secret_bytes")
def post_newtype_secret_bytes(data: Annotated[SecretFileBytes, File()]):
    # NewType wrapper around SecretBytes
    return {"file_size": len(data.get_secret_value())}


@app.post("/newtype_bytes")
def post_newtype_bytes(data: Annotated[CustomBytes, File()]):
    # NewType wrapper around bytes
    return {"file_size": len(data)}


client = TestClient(app)


@pytest.fixture
def tmp_file(tmp_path: Path) -> Path:
    f = tmp_path / "secret.txt"
    f.write_text("secret data content")
    return f


@pytest.fixture
def tmp_file_2(tmp_path: Path) -> Path:
    f = tmp_path / "secret2.txt"
    f.write_text("more secret data")
    return f


def test_secret_bytes_file(tmp_file: Path):
    """Test that SecretBytes works with File() annotation."""
    response = client.post(
        "/secret_file",
        files={"data": (tmp_file.name, tmp_file.read_bytes())},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": len("secret data content")}


def test_secret_bytes_file_optional_with_file(tmp_file: Path):
    """Test that SecretBytes | None works with File() annotation when file is provided."""
    response = client.post(
        "/secret_file_optional",
        files={"data": (tmp_file.name, tmp_file.read_bytes())},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": len("secret data content")}


def test_secret_bytes_file_optional_without_file():
    """Test that SecretBytes | None works with File() annotation when file is not provided."""
    response = client.post("/secret_file_optional")
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


def test_secret_bytes_file_default_with_file(tmp_file: Path):
    """Test that SecretBytes with default works when file is provided."""
    response = client.post(
        "/secret_file_default",
        files={"data": (tmp_file.name, tmp_file.read_bytes())},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": len("secret data content")}


def test_secret_bytes_file_default_without_file():
    """Test that SecretBytes with default works when file is not provided."""
    response = client.post("/secret_file_default")
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": None}


def test_secret_bytes_file_list(tmp_file: Path, tmp_file_2: Path):
    """Test that List[SecretBytes] works with File() annotation."""
    response = client.post(
        "/secret_file_list",
        files=[
            ("files", (tmp_file.name, tmp_file.read_bytes())),
            ("files", (tmp_file_2.name, tmp_file_2.read_bytes())),
        ],
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "file_sizes": [len("secret data content"), len("more secret data")]
    }


def test_newtype_secret_bytes_file(tmp_file: Path):
    """Test that NewType wrapping SecretBytes works with File() annotation."""
    response = client.post(
        "/newtype_secret_bytes",
        files={"data": (tmp_file.name, tmp_file.read_bytes())},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": len("secret data content")}


def test_newtype_bytes_file(tmp_file: Path):
    """Test that NewType wrapping bytes works with File() annotation."""
    response = client.post(
        "/newtype_bytes",
        files={"data": (tmp_file.name, tmp_file.read_bytes())},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"file_size": len("secret data content")}


def test_openapi_schema():
    """Test that the OpenAPI schema is correctly generated for SecretBytes file parameters."""
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()

    # Check that the paths are defined
    assert "/secret_file" in schema["paths"]
    assert "/secret_file_optional" in schema["paths"]
    assert "/secret_file_list" in schema["paths"]
    assert "/newtype_secret_bytes" in schema["paths"]
    assert "/newtype_bytes" in schema["paths"]

    # Check that the request body is multipart/form-data (File upload)
    secret_file_schema = schema["paths"]["/secret_file"]["post"]["requestBody"]
    assert "multipart/form-data" in secret_file_schema["content"]

    # Check NewType endpoints also use multipart/form-data
    newtype_secret_schema = schema["paths"]["/newtype_secret_bytes"]["post"][
        "requestBody"
    ]
    assert "multipart/form-data" in newtype_secret_schema["content"]

    newtype_bytes_schema = schema["paths"]["/newtype_bytes"]["post"]["requestBody"]
    assert "multipart/form-data" in newtype_bytes_schema["content"]
