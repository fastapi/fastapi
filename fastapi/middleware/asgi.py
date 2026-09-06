from typing import Annotated

from annotated_doc import Doc
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Message, Receive, Scope, Send


class ASGIMiddleware:
    """
    A base class to create middleware, with the same features as
    `@app.middleware("http")` but without its performance cost and its `contextvars`
    limitation.

    Subclass it, implement `on_request()`, `on_response()`, or both, and add it with
    `app.add_middleware()`.

    Read more about it in the
    [FastAPI docs for Advanced Middleware](https://fastapi.tiangolo.com/advanced/middleware/#creating-asgi-middlewares).

    ## Example

    ```python
    import time

    from fastapi import FastAPI, Request
    from fastapi.datastructures import MutableHeaders
    from fastapi.middleware.asgi import ASGIMiddleware

    app = FastAPI()


    class ProcessTimeMiddleware(ASGIMiddleware):
        async def on_request(self, request: Request) -> None:
            request.state.start_time = time.perf_counter()

        async def on_response(
            self, request: Request, status_code: int, headers: MutableHeaders
        ) -> None:
            process_time = time.perf_counter() - request.state.start_time
            headers["X-Process-Time"] = str(process_time)


    app.add_middleware(ProcessTimeMiddleware)
    ```
    """

    def __init__(
        self,
        app: Annotated[ASGIApp, Doc("The next app in the middleware stack.")],
    ) -> None:
        self.app = app

    async def on_request(
        self,
        request: Annotated[Request, Doc("The incoming request.")],
    ) -> Annotated[
        Response | None, Doc("An optional response to answer with right away.")
    ]:
        """
        Called with each request, before it is handled by a *path operation*.

        Anything stored in `request.state` here is available to the *path operation*
        and to `on_response()`.

        Returning a `Response` answers the request right away, and the *path
        operation* is never called.
        """
        return None

    async def on_response(
        self,
        request: Annotated[Request, Doc("The request that produced this response.")],
        status_code: Annotated[int, Doc("The status code of the response.")],
        headers: Annotated[
            MutableHeaders, Doc("The response headers, still editable.")
        ],
    ) -> None:
        """
        Called with each response, right before its first byte is sent.

        The response body is never buffered, so this also works with streaming
        responses.
        """

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        buffer: list[Message] = []

        async def buffering_receive() -> Message:
            message = await receive()
            buffer.append(message)
            return message

        request = Request(scope, buffering_receive)
        early_response = await self.on_request(request)
        if early_response is not None:
            await early_response(scope, receive, send)
            return

        async def replaying_receive() -> Message:
            return buffer.pop(0) if buffer else await receive()

        async def send_with_hook(message: Message) -> None:
            if message["type"] == "http.response.start":
                await self.on_response(
                    request, message["status"], MutableHeaders(scope=message)
                )
            await send(message)

        await self.app(scope, replaying_receive if buffer else receive, send_with_hook)
