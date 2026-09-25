import io
from typing import Any

import pytest
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile as StarletteUploadFile

app = FastAPI()


@app.post("/uploadfile")
async def uploadfile(uploadfile: UploadFile = File(...)) -> dict[str, Any]:
    return {
        "filename": uploadfile.filename,
        "is_fastapi_uploadfile": isinstance(uploadfile, UploadFile),
        "is_starlette_uploadfile": isinstance(uploadfile, StarletteUploadFile),
        "class": f"{uploadfile.__class__.__module__}.{uploadfile.__class__.__name__}",
    }


@app.post("/uploadfiles")
async def uploadfiles(
    uploadfiles: list[UploadFile] = File(...),
) -> list[dict[str, Any]]:
    return [
        {
            "filename": uploadfile.filename,
            "is_fastapi_uploadfile": isinstance(uploadfile, UploadFile),
            "is_starlette_uploadfile": isinstance(uploadfile, StarletteUploadFile),
            "class": f"{uploadfile.__class__.__module__}.{uploadfile.__class__.__name__}",
        }
        for uploadfile in uploadfiles
    ]


async def get_uploadfile_info(uploadfile: UploadFile = File(...)) -> dict[str, Any]:
    return {
        "filename": uploadfile.filename,
        "is_fastapi_uploadfile": isinstance(uploadfile, UploadFile),
        "is_starlette_uploadfile": isinstance(uploadfile, StarletteUploadFile),
        "class": f"{uploadfile.__class__.__module__}.{uploadfile.__class__.__name__}",
    }


@app.post("/uploadfile-dep")
async def uploadfile_dep(
    uploadfile_info: dict[str, Any] = Depends(get_uploadfile_info),
) -> dict[str, Any]:
    return uploadfile_info


async def get_uploadfiles_info(
    uploadfiles: list[UploadFile] = File(...),
) -> list[dict[str, Any]]:
    return [
        {
            "filename": uploadfile.filename,
            "is_fastapi_uploadfile": isinstance(uploadfile, UploadFile),
            "is_starlette_uploadfile": isinstance(uploadfile, StarletteUploadFile),
            "class": f"{uploadfile.__class__.__module__}.{uploadfile.__class__.__name__}",
        }
        for uploadfile in uploadfiles
    ]


@app.post("/uploadfiles-dep")
async def uploadfiles_dep(
    uploadfiles_info: list[dict[str, Any]] = Depends(get_uploadfiles_info),
) -> list[dict[str, Any]]:
    return uploadfiles_info


@pytest.mark.parametrize("endpoint", ["/uploadfile", "/uploadfile-dep"])
def test_uploadfile_type(endpoint: str) -> None:
    client = TestClient(app)
    files = {"uploadfile": ("example.txt", io.BytesIO(b"test content"), "text/plain")}
    response = client.post(f"{endpoint}", files=files)
    data = response.json()

    assert data["filename"] == "example.txt"
    assert data["is_fastapi_uploadfile"] is True
    assert data["is_starlette_uploadfile"] is True
    assert data["class"].startswith("fastapi.")


@pytest.mark.parametrize("endpoint", ["/uploadfiles", "/uploadfiles-dep"])
def test_uploadfiles_type(endpoint: str) -> None:
    client = TestClient(app)
    files = [
        ("uploadfiles", ("example.txt", io.BytesIO(b"test content"), "text/plain")),
        ("uploadfiles", ("example2.txt", io.BytesIO(b"test content"), "text/plain")),
    ]
    response = client.post(f"{endpoint}", files=files)
    files_data = response.json()

    assert len(files_data) == 2

    file1 = files_data[0]
    assert file1["filename"] == "example.txt"
    assert file1["is_fastapi_uploadfile"] is True
    assert file1["is_starlette_uploadfile"] is True
    assert file1["class"].startswith("fastapi.")

    file2 = files_data[1]
    assert file2["filename"] == "example2.txt"
    assert file2["is_fastapi_uploadfile"] is True
    assert file2["is_starlette_uploadfile"] is True
    assert file2["class"].startswith("fastapi.")
