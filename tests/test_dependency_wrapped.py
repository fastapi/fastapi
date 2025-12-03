import inspect
from asyncio import iscoroutinefunction
from functools import wraps
from typing import AsyncGenerator, Generator

import pytest
from fastapi import Depends, FastAPI
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from fastapi.testclient import TestClient


def noop_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


def noop_wrap_async(func):
    if inspect.isgeneratorfunction(func):

        @wraps(func)
        async def gen_wrapper(*args, **kwargs):
            async for item in iterate_in_threadpool(func(*args, **kwargs)):
                yield item

        return gen_wrapper

    elif inspect.isasyncgenfunction(func):

        @wraps(func)
        async def async_gen_wrapper(*args, **kwargs):
            async for item in func(*args, **kwargs):
                yield item

        return async_gen_wrapper

    @wraps(func)
    async def wrapper(*args, **kwargs):
        if inspect.isroutine(func) and iscoroutinefunction(func):
            return await func(*args, **kwargs)
        if inspect.isclass(func):
            return await run_in_threadpool(func, *args, **kwargs)
        dunder_call = getattr(func, "__call__", None)  # noqa: B004
        if iscoroutinefunction(dunder_call):
            return await dunder_call(*args, **kwargs)
        return await run_in_threadpool(func, *args, **kwargs)

    return wrapper


class ClassDep:
    def __call__(self):
        return True


class_dep = ClassDep()
wrapped_class_dep = noop_wrap(class_dep)
wrapped_class_dep_async_wrapper = noop_wrap_async(class_dep)


app = FastAPI()

# Sync wrapper


@noop_wrap
def wrapped_dependency() -> bool:
    return True


@noop_wrap
def wrapped_gen_dependency() -> Generator[bool, None, None]:
    yield True


@noop_wrap
async def async_wrapped_dependency() -> bool:
    return True


@noop_wrap
async def async_wrapped_gen_dependency() -> AsyncGenerator[bool, None]:
    yield True


@app.get("/wrapped-dependency/")
async def get_wrapped_dependency(value: bool = Depends(wrapped_dependency)):
    return value


@app.get("/wrapped-gen-dependency/")
async def get_wrapped_gen_dependency(value: bool = Depends(wrapped_gen_dependency)):
    return value


@app.get("/async-wrapped-dependency/")
async def get_async_wrapped_dependency(value: bool = Depends(async_wrapped_dependency)):
    return value


@app.get("/async-wrapped-gen-dependency/")
async def get_async_wrapped_gen_dependency(
    value: bool = Depends(async_wrapped_gen_dependency),
):
    return value


@app.get("/wrapped-class-dependency/")
async def get_wrapped_class_dependency(value: bool = Depends(wrapped_class_dep)):
    return value


@app.get("/wrapped-endpoint/")
@noop_wrap
def get_wrapped_endpoint():
    return True


@app.get("/async-wrapped-endpoint/")
@noop_wrap
async def get_async_wrapped_endpoint():
    return True


# Async wrapper


@noop_wrap_async
def wrapped_dependency_async_wrapper() -> bool:
    return True


@noop_wrap_async
def wrapped_gen_dependency_async_wrapper() -> Generator[bool, None, None]:
    yield True


@noop_wrap_async
async def async_wrapped_dependency_async_wrapper() -> bool:
    return True


@noop_wrap_async
async def async_wrapped_gen_dependency_async_wrapper() -> AsyncGenerator[bool, None]:
    yield True


@app.get("/wrapped-dependency-async-wrapper/")
async def get_wrapped_dependency_async_wrapper(
    value: bool = Depends(wrapped_dependency_async_wrapper),
):
    return value


@app.get("/wrapped-gen-dependency-async-wrapper/")
async def get_wrapped_gen_dependency_async_wrapper(
    value: bool = Depends(wrapped_gen_dependency_async_wrapper),
):
    return value


@app.get("/async-wrapped-dependency-async-wrapper/")
async def get_async_wrapped_dependency_async_wrapper(
    value: bool = Depends(async_wrapped_dependency_async_wrapper),
):
    return value


@app.get("/async-wrapped-gen-dependency-async-wrapper/")
async def get_async_wrapped_gen_dependency_async_wrapper(
    value: bool = Depends(async_wrapped_gen_dependency_async_wrapper),
):
    return value


@app.get("/wrapped-class-dependency-async-wrapper/")
async def get_wrapped_class_dependency_async_wrapper(
    value: bool = Depends(wrapped_class_dep_async_wrapper),
):
    return value


@app.get("/wrapped-endpoint-async-wrapper/")
@noop_wrap_async
def get_wrapped_endpoint_async_wrapper():
    return True


@app.get("/async-wrapped-endpoint-async-wrapper/")
@noop_wrap_async
async def get_async_wrapped_endpoint_async_wrapper():
    return True


client = TestClient(app)


@pytest.mark.parametrize(
    "route",
    [
        "/wrapped-dependency/",
        "/wrapped-gen-dependency/",
        "/async-wrapped-dependency/",
        "/async-wrapped-gen-dependency/",
        "/wrapped-class-dependency/",
        "/wrapped-endpoint/",
        "/async-wrapped-endpoint/",
        "/wrapped-dependency-async-wrapper/",
        "/wrapped-gen-dependency-async-wrapper/",
        "/async-wrapped-dependency-async-wrapper/",
        "/async-wrapped-gen-dependency-async-wrapper/",
        "/wrapped-class-dependency-async-wrapper/",
        "/wrapped-endpoint-async-wrapper/",
        "/async-wrapped-endpoint-async-wrapper/",
    ],
)
def test_class_dependency(route):
    response = client.get(route)
    assert response.status_code == 200, response.text
    assert response.json() is True
