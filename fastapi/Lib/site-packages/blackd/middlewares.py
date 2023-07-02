from typing import TYPE_CHECKING, Any, Awaitable, Callable, Iterable, TypeVar

from aiohttp.web_request import Request
from aiohttp.web_response import StreamResponse

if TYPE_CHECKING:
    F = TypeVar("F", bound=Callable[..., Any])
    middleware: Callable[[F], F]
else:
    try:
        from aiohttp.web_middlewares import middleware
    except ImportError:
        # @middleware is deprecated and its behaviour is the default since aiohttp 4.0
        # so if it doesn't exist anymore, define a no-op for forward compatibility.
        middleware = lambda x: x  # noqa: E731

Handler = Callable[[Request], Awaitable[StreamResponse]]
Middleware = Callable[[Request, Handler], Awaitable[StreamResponse]]


def cors(allow_headers: Iterable[str]) -> Middleware:
    @middleware
    async def impl(request: Request, handler: Handler) -> StreamResponse:
        is_options = request.method == "OPTIONS"
        is_preflight = is_options and "Access-Control-Request-Method" in request.headers
        if is_preflight:
            resp = StreamResponse()
        else:
            resp = await handler(request)

        origin = request.headers.get("Origin")
        if not origin:
            return resp

        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Expose-Headers"] = "*"
        if is_options:
            resp.headers["Access-Control-Allow-Headers"] = ", ".join(allow_headers)
            resp.headers["Access-Control-Allow-Methods"] = ", ".join(
                ("OPTIONS", "POST")
            )

        return resp

    return impl
