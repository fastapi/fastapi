"""
Test that async streaming endpoints can be cancelled without hanging.

Ref: https://github.com/fastapi/fastapi/issues/14680
"""

from collections.abc import AsyncIterable

import anyio
import pytest
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from starlette.types import Message, Scope

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
        i += 1  # pragma: no cover


@app.get("/stream-jsonl")
async def stream_jsonl() -> AsyncIterable[int]:
    """JSONL async generator with no internal await."""
    i = 0
    while True:
        yield i
        i += 1  # pragma: no cover


async def _run_asgi_and_cancel(
    app: FastAPI, path: str, *, timeout: float = 10.0
) -> bool:
    """Call the ASGI app for *path* and cancel as soon as the first body chunk arrives.

    Returns `True` if cancellation was delivered at a checkpoint (and the stream
    actually produced data). A *timeout* safety net prevents the test from hanging
    if cancellation never gets delivered.
    """
    chunks: list[bytes] = []
    cancel_scope: anyio.CancelScope | None = None

    async def receive() -> Message:
        # Simulate a client that never disconnects, rely on cancellation
        await anyio.sleep(float("inf"))
        return {"type": "http.disconnect"}  # pragma: no cover

    async def send(message: Message) -> None:
        nonlocal cancel_scope
        if message["type"] == "http.response.body":
            chunks.append(message.get("body", b""))
            if cancel_scope is not None and not cancel_scope.cancel_called:
                cancel_scope.cancel()

    scope: Scope = {
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

    with anyio.move_on_after(timeout):
        with anyio.CancelScope() as cancel_scope:
            await app(scope, receive, send)

    return cancel_scope.cancelled_caught and len(chunks) > 0


async def test_raw_stream_cancellation() -> None:
    """Raw streaming endpoint should be cancellable within a reasonable time."""
    cancelled = await _run_asgi_and_cancel(app, "/stream-raw")
    assert cancelled


async def test_jsonl_stream_cancellation() -> None:
    """JSONL streaming endpoint should be cancellable within a reasonable time."""
    cancelled = await _run_asgi_and_cancel(app, "/stream-jsonl")
    assert cancelled
