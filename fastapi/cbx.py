import inspect
import logging
from collections.abc import Callable
from functools import partial
from typing import Any, Generic, TypeVar

from fastapi import APIRouter

T = TypeVar("T")


class CBV(Generic[T]):
    def __init__(self, cls: type[T], router: APIRouter):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.router = router
        self.cls = cls

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        self.instance = self.cls(*args, **kwargs)
        for name, status_code in {
            "head": 200,
            "get": 200,
            "post": 201,
            "put": 204,
            "delete": 204,
            "patch": 200,
            "options": 200,
            "trace": 200,
            "connect": 200,
        }.items():
            if hasattr(self.instance, name):
                method = getattr(self.instance, name)
                self.router.add_api_route(
                    path="",
                    endpoint=method,
                    status_code=status_code,
                    methods=[name.upper()],
                    summary=f"{name.upper()} {self.router.prefix}",
                )

        return self.instance

    def __dir__(self) -> list[str]:
        return dir(self.cls)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.cls, name)


class CBR(Generic[T]):
    def __init__(self, cls: type[T], router: APIRouter):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.router = router
        self.cls = cls

    def __call__(self, *args: Any, **kwargs: Any) -> T:
        self.instance = self.cls(*args, **kwargs)

        for _name, endpoint in inspect.getmembers(
            self.instance, lambda x: inspect.ismethod(x) or inspect.isfunction(x)
        ):
            if cbx_router := endpoint.__annotations__.get("cbx_router"):
                for router in cbx_router:
                    self.router.add_api_route(
                        path=router["path"],
                        endpoint=endpoint,
                        methods=[router["method"]],
                        **router["kwargs"],
                    )
        return self.instance

    def __dir__(self) -> list[str]:
        return dir(self.cls)

    def __getattr__(self, name: str) -> Any:
        return getattr(self.cls, name)


class cbv(Generic[T]):
    def __init__(self, router: APIRouter):
        self.router = router

    def __call__(self, cls: type[T]) -> CBV[T]:
        return CBV(cls, self.router)


class cbr(Generic[T]):
    class method:
        def __init__(self, method: str, path: str, **kwargs: Any):
            self.method = method
            self.path = path
            self.kwargs = kwargs

        def __call__(self, endpoint: Callable[..., Any]) -> Callable[..., Any]:
            if "cbx_router" in endpoint.__annotations__:
                cbx_router: list = endpoint.__annotations__["cbx_router"]
                cbx_router.append(
                    {"method": self.method, "path": self.path, "kwargs": self.kwargs}
                )

            else:
                cbx_router: list = [
                    {"method": self.method, "path": self.path, "kwargs": self.kwargs}
                ]
                endpoint.__annotations__.setdefault("cbx_router", cbx_router)
            return endpoint

    head = partial(method, "HEAD")
    get = partial(method, "GET")
    post = partial(method, "POST")
    put = partial(method, "PUT")
    delete = partial(method, "DELETE")
    patch = partial(method, "PATCH")
    options = partial(method, "OPTIONS")
    trace = partial(method, "TRACE")
    connect = partial(method, "CONNECT")

    def __init__(self, router: APIRouter):
        self.router = router

    def __call__(self, cls: type[T]) -> CBR[T]:
        return CBR(cls, self.router)
