from contextlib import AsyncExitStack

from starlette.types import ASGIApp, Receive, Scope, Send


class AsyncExitStackMiddleware:
    def __init__(
        self, app: ASGIApp, context_name: str = "fastapi_middleware_astack"
    ) -> None:
        self.app = app
        self.context_name = context_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        async with AsyncExitStack() as stack:
            scope[self.context_name] = stack
            await self.app(scope, receive, send)
