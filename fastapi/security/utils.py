from functools import wraps
from typing import Any, Awaitable, Callable, Optional, Tuple, TypeVar

from fastapi.exceptions import HTTPException, WebSocketException
from starlette.requests import HTTPConnection
from starlette.status import WS_1008_POLICY_VIOLATION
from starlette.websockets import WebSocket


def get_authorization_scheme_param(
    authorization_header_value: Optional[str],
) -> Tuple[str, str]:
    if not authorization_header_value:
        return "", ""
    scheme, _, param = authorization_header_value.partition(" ")
    return scheme, param


_SecurityDepFunc = TypeVar(
    "_SecurityDepFunc", bound=Callable[[Any, HTTPConnection], Awaitable[Any]]
)


def handle_exc_for_ws(func: _SecurityDepFunc) -> _SecurityDepFunc:
    @wraps(func)
    async def wrapper(self: Any, request: HTTPConnection) -> Any:
        try:
            return await func(self, request)
        except HTTPException as e:
            if not isinstance(request, WebSocket):
                raise e
            await request.accept()
            raise WebSocketException(
                code=WS_1008_POLICY_VIOLATION, reason=e.detail
            ) from None

    return wrapper  # type: ignore
