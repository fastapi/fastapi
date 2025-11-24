import pytest
from anyio import open_file
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def get_username_reraises():
    try:
        async with await open_file("/nonexistent/path.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError as ex:
        raise RuntimeError("File read error") from ex


async def get_username_doesnt_reraise():
    try:
        async with await open_file("/nonexistent/path.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError:
        print("Didn't re-raise")


@app.get("/reraises")
def get_me_reraises(username: str = Depends(get_username_reraises)):
    return username  # pragma: no cover


@app.get("/doesnt-reraise")
def get_me_doesnt_reraise(username: str = Depends(get_username_doesnt_reraise)):
    return username  # pragma: no cover


client = TestClient(app)


@pytest.mark.anyio
def test_runtime_error_reraises():
    with pytest.raises(RuntimeError) as exc_info:
        client.get("/reraises")
    assert str(exc_info.value) == "File read error"


@pytest.mark.anyio
def test_runtime_error_doesnt_reraise():
    with pytest.raises(RuntimeError) as exc_info:
        client.get("/doesnt-reraise")
    assert str(exc_info.value).startswith(
        "Dependency get_username_doesnt_reraise raised: generator didn't yield. "
        "There's a high chance that this is a dependency with yield that catches an "
        "exception using except, but doesn't raise the exception again."
    )
