from collections.abc import AsyncIterable

from fastapi import APIRouter, FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.testclient import TestClient

app = FastAPI()
router = APIRouter()


@app.get("/returned-response", response_class=EventSourceResponse)
async def returned_response() -> EventSourceResponse:
    async def gen() -> AsyncIterable[bytes]:
        yield b"data: hi\n\n"

    return EventSourceResponse(gen())


@app.get("/async-endpoint", response_class=EventSourceResponse)
async def async_endpoint():
    return {"msg": "hello"}


@app.get("/sync-endpoint", response_class=EventSourceResponse)
def sync_endpoint():
    return {"msg": "hello"}


@app.get("/generator", response_class=EventSourceResponse)
async def generator() -> AsyncIterable[str]:
    yield "a"


@router.get("/router-non-generator", response_class=EventSourceResponse)
async def router_non_generator():
    return {"msg": "hello"}


@router.get("/router-generator", response_class=EventSourceResponse)
async def router_generator() -> AsyncIterable[str]:
    yield "a"


app.include_router(router)

client = TestClient(app)


def test_returned_event_source_response():
    """A non-generator endpoint may return an `EventSourceResponse` directly."""
    response = client.get("/returned-response")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text == "data: hi\n\n"


def test_async_non_generator_endpoint_is_not_sse_framed():
    """A non-generator must not be pushed through the SSE producer.

    Before the fix the coroutine was handed to the producer, which raised
    `TypeError: 'coroutine' object is not iterable` after the `200` and its headers
    had already been flushed, leaving an empty body.
    """
    response = client.get("/async-endpoint")
    assert response.status_code == 200, response.text
    assert "data:" not in response.text


def test_sync_non_generator_endpoint_is_not_sse_framed():
    """A sync non-generator must not have its return value framed as SSE events.

    Unlike the async case this one failed silently: the return value was passed to
    `iterate_in_threadpool`, so a returned dict streamed its *keys* as `data:` events.
    """
    response = client.get("/sync-endpoint")
    assert response.status_code == 200, response.text
    assert "data:" not in response.text


def test_generator_endpoint_still_streams_sse():
    response = client.get("/generator")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text == 'data: "a"\n\n'


def test_included_router_non_generator_is_not_sse_framed():
    """The generator check must also hold for routes added via `include_router`."""
    response = client.get("/router-non-generator")
    assert response.status_code == 200, response.text
    assert "data:" not in response.text


def test_included_router_generator_still_streams_sse():
    response = client.get("/router-generator")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text == 'data: "a"\n\n'
