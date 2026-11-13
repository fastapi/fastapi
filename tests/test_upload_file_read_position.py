from io import BytesIO
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI, File, UploadFile
from fastapi.dependencies.utils import _read_file_bytes
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "content",
    [
        pytest.param(b"hello", id="memory"),
        pytest.param(b"x" * (1024 * 1024 + 1), id="disk"),
    ],
)
def test_file_bytes_shared_by_dependency_and_endpoint(content: bytes):
    app = FastAPI()

    def inspect_file(file: Annotated[bytes, File()]):
        return file.decode()

    @app.post("/")
    def upload(
        inspected: Annotated[str, Depends(inspect_file)],
        file: Annotated[bytes, File()],
    ):
        return {"dependency": inspected, "endpoint": file.decode()}

    client = TestClient(app)
    response = client.post("/", files={"file": ("hello.txt", content)})
    assert response.status_code == 200
    assert response.json() == {
        "dependency": content.decode(),
        "endpoint": content.decode(),
    }


def test_file_bytes_list_shared_by_dependency_and_endpoint():
    app = FastAPI()

    def inspect_files(files: Annotated[list[bytes], File()]):
        return [file.decode() for file in files]

    @app.post("/")
    def upload(
        inspected: Annotated[list[str], Depends(inspect_files)],
        files: Annotated[list[bytes], File()],
    ):
        return {"dependency": inspected, "endpoint": [file.decode() for file in files]}

    client = TestClient(app)
    response = client.post(
        "/",
        files=[
            ("files", ("one.txt", b"one")),
            ("files", ("two.txt", b"two")),
        ],
    )
    assert response.status_code == 200
    assert response.json() == {
        "dependency": ["one", "two"],
        "endpoint": ["one", "two"],
    }


def test_bytes_dependency_preserves_upload_file_for_endpoint():
    app = FastAPI()

    def inspect_file(file: Annotated[bytes, File()]):
        return file.decode()

    @app.post("/")
    async def upload(
        inspected: Annotated[str, Depends(inspect_file)],
        file: Annotated[UploadFile, File()],
    ):
        content = await file.read()
        second_read = await file.read()
        return {
            "dependency": inspected,
            "endpoint": content.decode(),
            "second_read": second_read.decode(),
        }

    client = TestClient(app)
    response = client.post("/", files={"file": ("hello.txt", b"hello")})
    assert response.status_code == 200
    assert response.json() == {
        "dependency": "hello",
        "endpoint": "hello",
        "second_read": "",
    }


def test_automatic_file_read_preserves_nonzero_position():
    app = FastAPI()

    async def read_prefix(file: Annotated[UploadFile, File()]):
        return (await file.read(2)).decode()

    def inspect_remainder(
        prefix: Annotated[str, Depends(read_prefix)],
        file: Annotated[bytes, File()],
    ):
        return {"prefix": prefix, "remainder": file.decode()}

    @app.post("/")
    async def upload(
        inspected: Annotated[dict[str, str], Depends(inspect_remainder)],
        file: Annotated[UploadFile, File()],
    ):
        position = file.file.tell()
        remainder = await file.read()
        return {
            "dependency": inspected,
            "position": position,
            "remainder": remainder.decode(),
        }

    client = TestClient(app)
    response = client.post("/", files={"file": ("hello.txt", b"hello")})
    assert response.status_code == 200
    assert response.json() == {
        "dependency": {"prefix": "he", "remainder": "llo"},
        "position": 2,
        "remainder": "llo",
    }


@pytest.mark.anyio
async def test_failed_automatic_file_read_restores_position(
    monkeypatch: pytest.MonkeyPatch,
):
    with BytesIO(b"hello") as stream:
        file = UploadFile(file=stream)
        stream.seek(2)

        async def failing_read(size: int = -1) -> bytes:
            stream.read(1)
            raise OSError("read failed")

        monkeypatch.setattr(file, "read", failing_read)
        with pytest.raises(OSError, match="read failed"):
            await _read_file_bytes(file)

        assert stream.tell() == 2
