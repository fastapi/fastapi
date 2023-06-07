from typing import Awaitable, Callable, Optional

from fastapi.concurrency import AsyncExitStack
from starlette.requests import Request
from starlette.responses import Response


class AsyncExitStackMiddleware:
    def __init__(
        self,
        endpoint: Callable[[Request], Awaitable[Response]],
        context_name: str = "fastapi_astack",
    ) -> None:
        self.context_name = context_name
        self.endpoint = endpoint

    async def __call__(self, request: Request) -> Response:  # type: ignore[return]
        if AsyncExitStack:
            dependency_exception: Optional[Exception] = None
            async with AsyncExitStack() as stack:
                request.scope[self.context_name] = stack
                try:
                    response = await self.endpoint(request)
                    return response
                except Exception as e:
                    dependency_exception = e
                    raise e
            if dependency_exception:
                # This exception was possibly handled by the dependency but it should
                # still bubble up so that the ServerErrorMiddleware can return a 500
                # or the ExceptionMiddleware can catch and handle any other exceptions
                raise dependency_exception
        else:
            return await self.endpoint(request)  # pragma: no cover
