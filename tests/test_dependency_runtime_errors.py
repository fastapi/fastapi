import pytest
from anyio import open_file
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app_reraises = FastAPI()
app_doesnt_reraise = FastAPI()


async def get_username_reraises():
    try:
        async with await open_file("/non_existing/path.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError as ex:
        raise RuntimeError("File something something, wubba lubba dub dub!") from ex


async def get_username_doesnt_reraise():
    try:
        async with await open_file("/path/to/sanchez.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError:
        print("We didn't re-raise, wubba lubba dub dub!")


@app_reraises.get("/me")
def get_me_reraises(username: str = Depends(get_username_reraises)):
    return username  # pragma: no cover


@app_doesnt_reraise.get("/me")
def get_me_doesnt_reraise(username: str = Depends(get_username_doesnt_reraise)):
    return username  # pragma: no cover


client_reraises = TestClient(app_reraises)
client_doesnt_reraise = TestClient(app_doesnt_reraise)


@pytest.mark.anyio
def test_runtime_error_reraises():
    with pytest.raises(RuntimeError) as exc_info:
        client_reraises.get("/me")
    assert str(exc_info.value) == "File something something, wubba lubba dub dub!"


@pytest.mark.anyio
def test_runtime_error_doesnt_reraise():
    with pytest.raises(RuntimeError) as exc_info:
        client_doesnt_reraise.get("/me")
    assert str(exc_info.value).startswith(
        "Dependency get_username_doesnt_reraise raised: generator didn't yield. "
        "There's a high chance that this is a dependency with yield that catches an "
        "exception using except, but doesn't raise the exception again."
    )
