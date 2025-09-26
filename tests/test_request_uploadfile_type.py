import io
from typing import Any, Dict, List

from fastapi import FastAPI, File, UploadFile
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile as StarletteUploadFile

app = FastAPI()


@app.post("/uploadfile")
async def uploadfile(uploadfile: UploadFile = File(...)) -> Dict[str, Any]:
    return {
        "filename": uploadfile.filename,
        "is_fastapi_uploadfile": isinstance(uploadfile, UploadFile),
        "is_starlette_uploadfile": isinstance(uploadfile, StarletteUploadFile),
        "class": f"{uploadfile.__class__.__module__}.{uploadfile.__class__.__name__}",
    }


@app.post("/uploadfiles")
async def uploadfiles(
    uploadfiles: List[UploadFile] = File(...),
) -> List[Dict[str, Any]]:
    return [
        {
            "filename": uploadfile.filename,
            "is_fastapi_uploadfile": isinstance(uploadfile, UploadFile),
            "is_starlette_uploadfile": isinstance(uploadfile, StarletteUploadFile),
            "class": f"{uploadfile.__class__.__module__}.{uploadfile.__class__.__name__}",
        }
        for uploadfile in uploadfiles
    ]


def test_uploadfile_type() -> None:
    client = TestClient(app)
    files = {"uploadfile": ("example.txt", io.BytesIO(b"test content"), "text/plain")}
    response = client.post("/uploadfile/", files=files)
    data = response.json()

    assert data["filename"] == "example.txt"
    assert data["is_fastapi_uploadfile"] is True
    assert data["is_starlette_uploadfile"] is True
    assert data["class"].startswith("fastapi.")


def test_uploadfiles_type() -> None:
    client = TestClient(app)
    files = [
        ("uploadfiles", ("example.txt", io.BytesIO(b"test content"), "text/plain"))
    ]
    response = client.post("/uploadfiles/", files=files)
    files_data = response.json()

    assert len(files_data) == 1

    data = files_data[0]

    assert data["filename"] == "example.txt"
    assert data["is_fastapi_uploadfile"] is True
    assert data["is_starlette_uploadfile"] is True
    assert data["class"].startswith("fastapi.")
