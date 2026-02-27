"""
Test that async streaming endpoints can be cancelled without hanging.

Ref: https://github.com/fastapi/fastapi/issues/14680
"""

from collections.abc import AsyncIterable

import anyio
import pytest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

pytestmark = [
    pytest.mark.anyio,
    pytest.mark.filterwarnings("ignore::pytest.PytestUnraisableExceptionWarning"),
]


app = FastAPI()


@app.get("/stream-raw", response_class=StreamingResponse)
async def stream_raw() -> AsyncIterable[str]:
    """Async generator with no internal await - would hang without checkpoint."""
    i = 0
    while True:
        yield f"item {i}\n"
        i += 1


@app.get("/stream-jsonl")
async def stream_jsonl() -> AsyncIterable[int]:
    """JSONL async generator with no internal await."""
    i = 0
    while True:
        yield i
        i += 1


async def _run_asgi_and_cancel(app: FastAPI, path: str, timeout: float) -> bool:
    """Call the ASGI app for *path* and cancel after *timeout* seconds.

    Returns `True` if the cancellation was delivered (i.e. it did not hang).
    """
    chunks: list[bytes] = []

    async def receive():  # type: ignore[no-untyped-def]
        # Simulate a client that never disconnects, rely on cancellation
        await anyio.sleep(float("inf"))
        return {"type": "http.disconnect"}

    async def send(message: dict) -> None:  # type: ignore[type-arg]
        if message["type"] == "http.response.body":
            chunks.append(message.get("body", b""))

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.0"},
        "http_version": "1.1",
        "method": "GET",
        "path": path,
        "query_string": b"",
        "root_path": "",
        "headers": [],
        "server": ("test", 80),
    }

    with anyio.move_on_after(timeout) as cancel_scope:
        await app(scope, receive, send)  # type: ignore[arg-type]

    # If we got here within the timeout the generator was cancellable.
    # cancel_scope.cancelled_caught is True when move_on_after fired.
    return cancel_scope.cancelled_caught or len(chunks) > 0


async def test_raw_stream_cancellation() -> None:
    """Raw streaming endpoint should be cancellable within a reasonable time."""
    cancelled = await _run_asgi_and_cancel(app, "/stream-raw", timeout=3.0)
    # The key assertion: we reached this line at all (didn't hang).
    # cancelled will be True because the infinite generator was interrupted.
    assert cancelled


async def test_jsonl_stream_cancellation() -> None:
    """JSONL streaming endpoint should be cancellable within a reasonable time."""
    cancelled = await _run_asgi_and_cancel(app, "/stream-jsonl", timeout=3.0)
    assert cancelled
