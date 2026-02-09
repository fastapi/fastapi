from functools import wraps
from typing import Any, Callable


def route_middleware(*middlewares: Callable[..., Any]) -> Callable[..., Any]:
    def decorator(route_func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(route_func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            req = kwargs.get("req")
            if req is None:
                raise ValueError("Route must have 'request: Request' parameter")

            for middleware in middlewares:
                result = middleware(req)
                if callable(getattr(result, "__await__", None)):
                    await result

            return await route_func(*args, **kwargs)

        return wrapper

    return decorator
