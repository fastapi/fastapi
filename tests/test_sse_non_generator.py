from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.responses import EventSourceResponse
from fastapi.testclient import TestClient

app = FastAPI()


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


client = TestClient(app)


def test_returned_event_source_response():
    """A non-generator endpoint may return an `EventSourceResponse` directly."""
    response = client.get("/returned-response")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text == "data: hi\n\n"


def test_non_generator_endpoint_does_not_crash():
    """A non-generator endpoint must not be pushed through the SSE producer."""
    response = client.get("/async-endpoint")
    assert response.status_code == 200, response.text


def test_sync_non_generator_endpoint_is_not_iterated():
    """A sync non-generator must not have its return value iterated as SSE events.

    Unlike the async case, this one fails silently: the return value is passed to
    `iterate_in_threadpool`, so a returned dict streams its *keys* as events.
    """
    response = client.get("/sync-endpoint")
    assert response.status_code == 200, response.text
    assert "data:" not in response.text


def test_generator_endpoint_still_streams_sse():
    response = client.get("/generator")
    assert response.status_code == 200, response.text
    assert response.headers["content-type"].startswith("text/event-stream")
    assert response.text == 'data: "a"\n\n'
