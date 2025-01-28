import pytest
from anyio import open_file
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


async def get_username():
    try:
        async with await open_file("/path/to/sanchez.txt", "r") as f:
            yield await f.read()  # pragma: no cover
    except OSError as ex:
        raise RuntimeError("File something something, wubba lubba dub dub!") from ex


@app.get("/me")
def get_me(username: str = Depends(get_username)):
    return username  # pragma: no cover


client = TestClient(app)


@pytest.mark.anyio
def test_runtime_error():
    with pytest.raises(RuntimeError) as exc_info:
        client.get("/me")
    assert "File something something" in exc_info.value.args[0]
