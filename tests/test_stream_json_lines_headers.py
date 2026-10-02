from collections.abc import AsyncIterator, Iterator

from fastapi import Depends, FastAPI, Response
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str


app = FastAPI()


@app.get("/items/stream")
async def stream_items() -> AsyncIterator[Item]:
    yield Item(name="foo")


@app.get("/items/stream-sync")
def stream_items_sync() -> Iterator[Item]:
    yield Item(name="bar")


def enable_proxy_buffering(response: Response) -> None:
    response.headers["X-Accel-Buffering"] = "yes"


@app.get(
    "/items/stream-buffering-enabled", dependencies=[Depends(enable_proxy_buffering)]
)
async def stream_items_buffering_enabled() -> AsyncIterator[Item]:
    yield Item(name="baz")


client = TestClient(app)


def test_stream_disables_proxy_buffering():
    response = client.get("/items/stream")
    assert response.status_code == 200, response.text
    assert response.headers["x-accel-buffering"] == "no"


def test_stream_sync_disables_proxy_buffering():
    response = client.get("/items/stream-sync")
    assert response.status_code == 200, response.text
    assert response.headers["x-accel-buffering"] == "no"


def test_stream_buffering_header_can_be_overridden():
    response = client.get("/items/stream-buffering-enabled")
    assert response.status_code == 200, response.text
    assert response.headers["x-accel-buffering"] == "yes"
    assert response.headers.get_list("x-accel-buffering") == ["yes"]
