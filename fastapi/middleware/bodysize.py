from __future__ import annotations

from typing import List
from starlette.types import ASGIApp, Receive, Scope, Send, Message


class BodySizeLimitMiddleware:
    """ASGI middleware to enforce a maximum request body size.

    - Applies to HTTP requests only.
    - Pre-reads up to the configured limit; if exceeded, responds 413 and does not invoke the app.
    - Otherwise, replays the buffered body to the downstream app.
    """

    def __init__(self, app: ASGIApp, max_body_size: int) -> None:
        self.app = app
        self.max_body_size = int(max_body_size)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope.get("type") != "http":
            await self.app(scope, receive, send)
            return

        total = 0
        chunks: List[bytes] = []
        more_body = True

        # Read the incoming body in chunks, enforcing the limit.
        while more_body:
            message = await receive()
            if message.get("type") != "http.request":
                # Pass through non-body messages (e.g., http.disconnect) to app behavior by aborting early.
                # In practice, FastAPI/Starlette don't expect them here before body, so we bail out.
                break
            body = message.get("body", b"")
            if body:
                total += len(body)
                if total > self.max_body_size:
                    # Drain the remaining body to allow the server to cleanly finish reading the request.
                    while message.get("more_body", False):
                        message = await receive()
                    await send({
                        "type": "http.response.start",
                        "status": 413,
                        "headers": [(b"content-type", b"text/plain; charset=utf-8")],
                    })
                    await send({
                        "type": "http.response.body",
                        "body": b"Payload Too Large",
                        "more_body": False,
                    })
                    return
                chunks.append(body)
            more_body = message.get("more_body", False)

        buffered = b"".join(chunks)
        sent_once = False

        async def cached_receive() -> Message:
            nonlocal sent_once
            if not sent_once:
                sent_once = True
                return {"type": "http.request", "body": buffered, "more_body": False}
            return {"type": "http.request", "body": b"", "more_body": False}

        await self.app(scope, cached_receive, send)
