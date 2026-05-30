import io
from pathlib import Path

import pytest
from fastapi import FastAPI, UploadFile
from fastapi.datastructures import Default, ValidationResult
from fastapi.testclient import TestClient
from starlette.datastructures import Headers
from starlette.exceptions import HTTPException


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

    testing_file_store: list[UploadFile] = []

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


@pytest.mark.anyio
async def test_upload_file_validate_size_pass():
    stream = io.BytesIO(b"small file")
    file = UploadFile(filename="test.txt", file=stream, size=10, max_size=100)
    result = await file.validate()
    assert result.is_valid
    assert result.file_size == 10
    assert result.content_type is None


@pytest.mark.anyio
async def test_upload_file_validate_size_fail():
    stream = io.BytesIO(b"x" * 200)
    file = UploadFile(filename="large.txt", file=stream, size=200, max_size=100)
    with pytest.raises(HTTPException) as exc:
        await file.validate()
    assert exc.value.status_code == 413


@pytest.mark.anyio
async def test_upload_file_validate_size_none():
    stream = io.BytesIO(b"x" * 999)
    file = UploadFile(filename="any.txt", file=stream, size=999, max_size=None)
    result = await file.validate()
    assert result.is_valid


@pytest.mark.anyio
async def test_upload_file_validate_content_type_pass():
    stream = io.BytesIO(b"some json")
    file = UploadFile(
        filename="data.json",
        file=stream,
        size=9,
        headers=Headers({"content-type": "application/json"}),
        allowed_content_types=["application/json", "text/plain"],
    )
    result = await file.validate()
    assert result.is_valid


@pytest.mark.anyio
async def test_upload_file_validate_content_type_fail():
    stream = io.BytesIO(b"some data")
    file = UploadFile(
        filename="data.xml",
        file=stream,
        size=9,
        headers=Headers({"content-type": "application/xml"}),
        allowed_content_types=["image/png"],
    )
    with pytest.raises(HTTPException) as exc:
        await file.validate()
    assert exc.value.status_code == 415


@pytest.mark.anyio
async def test_upload_file_validate_content_type_none():
    stream = io.BytesIO(b"any type")
    file = UploadFile(
        filename="data.bin",
        file=stream,
        size=8,
        headers=Headers({"content-type": "text/plain"}),
        allowed_content_types=None,
    )
    result = await file.validate()
    assert result.is_valid


@pytest.mark.anyio
async def test_upload_file_validate_both_constraints():
    stream = io.BytesIO(b"ok")
    file = UploadFile(
        filename="ok.txt",
        file=stream,
        size=2,
        max_size=100,
        headers=Headers({"content-type": "text/plain"}),
        allowed_content_types=["text/plain"],
    )
    result = await file.validate()
    assert result.is_valid


def test_upload_file_existing_usage_unchanged():
    stream = io.BytesIO(b"data")
    file = UploadFile(filename="file", file=stream, size=4)
    assert file.filename == "file"
    assert file.size == 4
    assert file.max_size is None
    assert file.allowed_content_types is None


def test_validation_result_dataclass():
    result = ValidationResult(is_valid=True, file_size=100, content_type="text/plain")
    assert result.is_valid
    assert result.file_size == 100
    assert result.content_type == "text/plain"
