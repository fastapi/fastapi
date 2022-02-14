from fastapi.concurrency import AsyncExitStack
from starlette.types import ASGIApp, Receive, Scope, Send


class AsyncExitStackMiddleware:
    def __init__(self, app: ASGIApp, context_name: str = "fastapi_astack") -> None:
        self.app = app
        self.context_name = context_name

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if AsyncExitStack:
            async with AsyncExitStack() as stack:
                scope[self.context_name] = stack
                await self.app(scope, receive, send)
        else:
            await self.app(scope, receive, send)  # pragma: no cover
