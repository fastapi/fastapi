from functools import wraps
from fastapi import Request
from typing import Callable

def route_middleware(*middlewares:Callable):
    def decorator(route_func:Callable):
        @wraps(route_func)
        async def wrapper(*args, **kwargs):
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



# Example middlewares
async def verify_jwt(req: Request):
    # just a mock
    if not (req.query_params.get("is_true") == "true"):
        req.user={"name":"xyz","admin":True}
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid JWT")

def log_route(req: Request):
    print(f"[LOG] Path: {req.url.path}")