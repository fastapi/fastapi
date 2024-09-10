import io
from pathlib import Path
from typing import List

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default
from fastapi.testclient import TestClient


# TODO: remove when deprecating Pydantic v1
def test_upload_file_invalid():
    with pytest.raises(ValueError):
        UploadFile.validate("not a Starlette UploadFile")


def test_upload_file_invalid_pydantic_v2():
    with pytest.raises(ValueError):
        UploadFile._validate("not a Starlette UploadFile", {})


def test_default_placeholder_equals():
    placeholder_1 = Default("a")
    placeholder_2 = Default("a")
    assert placeholder_1 == placeholder_2
    assert placeholder_1.value == placeholder_2.value


def test_default_placeholder_bool():
    placeholder_a = Default("a")
    placeholder_b = Default("")
    assert placeholder_a
    assert not placeholder_b


def test_upload_file_is_closed(tmp_path: Path):
    path = tmp_path / "test.txt"
    path.write_bytes(b"<file content>")
    app = FastAPI()

    testing_file_store: List[UploadFile] = []

    @app.post("/uploadfile/")
    def create_upload_file(file: UploadFile):
        testing_file_store.append(file)
        return {"filename": file.filename}

    client = TestClient(app)
    with path.open("rb") as file:
        response = client.post("/uploadfile/", files={"file": file})
    assert response.status_code == 200, response.text
    assert response.json() == {"filename": "test.txt"}

    assert testing_file_store
    assert testing_file_store[0].file.closed


# For UploadFile coverage, segments copied from Starlette tests


@pytest.mark.anyio
async def test_upload_file():
    stream = io.BytesIO(b"data")
    file = UploadFile(filename="file", file=stream, size=4)
    assert await file.read() == b"data"
    assert file.size == 4
    await file.write(b" and more data!")
    assert await file.read() == b""
    assert file.size == 19
    await file.seek(0)
    assert await file.read() == b"data and more data!"
    await file.close()
