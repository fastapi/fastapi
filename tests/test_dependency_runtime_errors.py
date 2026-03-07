import pytest
from anyio import open_file
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def get_username_reraises():
    try:
        with open("/nonexistent/path.txt") as f:
            yield f.read()  # pragma: no cover
    except OSError as ex:
        raise RuntimeError("File read error") from ex


def get_username_doesnt_reraise():
    try:
        with open("/nonexistent/path.txt") as f:
            yield f.read()  # pragma: no cover
    except OSError:
        print("Didn't re-raise")


async def get_username_reraises_async():
    try:
        async with await open_file("/nonexistent/path.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError as ex:
        raise RuntimeError("File read error") from ex


async def get_username_doesnt_reraise_async():
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


@app.get("/reraises-async")
def get_me_reraises_async(username: str = Depends(get_username_reraises_async)):
    return username  # pragma: no cover


@app.get("/doesnt-reraise-async")
def get_me_doesnt_reraise_async(
    username: str = Depends(get_username_doesnt_reraise_async),
):
    return username  # pragma: no cover


client = TestClient(app)


@pytest.mark.anyio
@pytest.mark.parametrize("path", ["/reraises", "/reraises-async"])
def test_runtime_error_reraises(path: str):
    with pytest.raises(RuntimeError) as exc_info:
        client.get(path)
    assert str(exc_info.value) == "File read error"


@pytest.mark.anyio
@pytest.mark.parametrize(
    ("path", "fn_name"),
    [
        ("/doesnt-reraise", "get_username_doesnt_reraise"),
        ("/doesnt-reraise-async", "get_username_doesnt_reraise_async"),
    ],
)
def test_runtime_error_doesnt_reraise(path: str, fn_name: str):
    with pytest.raises(RuntimeError) as exc_info:
        client.get(path)
    assert str(exc_info.value).startswith(
        f"Dependency {fn_name} raised: generator didn't yield. "
        "There's a high chance that this is a dependency with yield that catches an "
        "exception using except, but doesn't raise the exception again."
    )
