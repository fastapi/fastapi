import inspect
import logging
from collections.abc import Callable
from functools import partial
from typing import Any

from fastapi import APIRouter
from typing_extensions import Self


class CBV:
    def __init__(self, cls: type[Any], router: APIRouter):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.router = router
        self.cls = cls

    def __call__(self, *args: Any, **kwargs: Any) -> Self:
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
                    response_model=method.__annotations__.get("return"),
                    status_code=status_code,
                    methods=[name.upper()],
                    summary=f"{name.upper()} {self.router.prefix}",
                )

        return self


class CBR:
    def __init__(self, cls: type[Any], router: APIRouter):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.router = router
        self.cls = cls

    def __call__(self, *args: Any, **kwargs: Any) -> Self:
        self.instance = self.cls(*args, **kwargs)

        for _name, endpoint in inspect.getmembers(
            self.instance, lambda x: inspect.ismethod(x) or inspect.isfunction(x)
        ):
            if cbx_router := endpoint.__annotations__.get("cbx_router"):
                self.router.add_api_route(
                    path=cbx_router["path"],
                    endpoint=endpoint,
                    methods=[cbx_router["method"]],
                    **cbx_router["kwargs"],
                )
        return self


class cbv:
    def __init__(self, router: APIRouter):
        self.router = router

    def __call__(self, cls: type[Any]) -> CBV:
        return CBV(cls, self.router)


class cbr:
    class method:
        def __init__(self, method: str, path: str, **kwargs: Any):
            self.method = method
            self.path = path
            self.kwargs = kwargs

        def __call__(self, endpoint: Callable[..., Any]) -> Callable[..., Any]:
            endpoint.__annotations__.setdefault(
                "cbx_router",
                {"method": self.method, "path": self.path, "kwargs": self.kwargs},
            )
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

    def __call__(self, cls: type[Any]) -> CBR:
        return CBR(cls, self.router)
