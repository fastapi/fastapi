import inspect
import sys
from collections.abc import AsyncGenerator, Generator
from functools import wraps

import pytest
from fastapi import Depends, FastAPI
from fastapi.concurrency import iterate_in_threadpool, run_in_threadpool
from fastapi.testclient import TestClient

if sys.version_info >= (3, 13):  # pragma: no cover
    from inspect import iscoroutinefunction
else:  # pragma: no cover
    from asyncio import iscoroutinefunction


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


class ClassInstanceDep:
    def __call__(self):
        return True


class_instance_dep = ClassInstanceDep()
wrapped_class_instance_dep = noop_wrap(class_instance_dep)
wrapped_class_instance_dep_async_wrapper = noop_wrap_async(class_instance_dep)


class ClassInstanceGenDep:
    def __call__(self):
        yield True


class_instance_gen_dep = ClassInstanceGenDep()
wrapped_class_instance_gen_dep = noop_wrap(class_instance_gen_dep)


class ClassInstanceWrappedDep:
    @noop_wrap
    def __call__(self):
        return True


class_instance_wrapped_dep = ClassInstanceWrappedDep()


class ClassInstanceWrappedAsyncDep:
    @noop_wrap_async
    def __call__(self):
        return True


class_instance_wrapped_async_dep = ClassInstanceWrappedAsyncDep()


class ClassInstanceWrappedGenDep:
    @noop_wrap
    def __call__(self):
        yield True


class_instance_wrapped_gen_dep = ClassInstanceWrappedGenDep()


class ClassInstanceWrappedAsyncGenDep:
    @noop_wrap_async
    def __call__(self):
        yield True


class_instance_wrapped_async_gen_dep = ClassInstanceWrappedAsyncGenDep()


class ClassDep:
    def __init__(self):
        self.value = True


wrapped_class_dep = noop_wrap(ClassDep)
wrapped_class_dep_async_wrapper = noop_wrap_async(ClassDep)


class ClassInstanceAsyncDep:
    async def __call__(self):
        return True


class_instance_async_dep = ClassInstanceAsyncDep()
wrapped_class_instance_async_dep = noop_wrap(class_instance_async_dep)
wrapped_class_instance_async_dep_async_wrapper = noop_wrap_async(
    class_instance_async_dep
)


class ClassInstanceAsyncGenDep:
    async def __call__(self):
        yield True


class_instance_async_gen_dep = ClassInstanceAsyncGenDep()
wrapped_class_instance_async_gen_dep = noop_wrap(class_instance_async_gen_dep)


class ClassInstanceAsyncWrappedDep:
    @noop_wrap
    async def __call__(self):
        return True


class_instance_async_wrapped_dep = ClassInstanceAsyncWrappedDep()


class ClassInstanceAsyncWrappedAsyncDep:
    @noop_wrap_async
    async def __call__(self):
        return True


class_instance_async_wrapped_async_dep = ClassInstanceAsyncWrappedAsyncDep()


class ClassInstanceAsyncWrappedGenDep:
    @noop_wrap
    async def __call__(self):
        yield True


class_instance_async_wrapped_gen_dep = ClassInstanceAsyncWrappedGenDep()


class ClassInstanceAsyncWrappedGenAsyncDep:
    @noop_wrap_async
    async def __call__(self):
        yield True


class_instance_async_wrapped_gen_async_dep = ClassInstanceAsyncWrappedGenAsyncDep()

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


@app.get("/wrapped-class-instance-dependency/")
async def get_wrapped_class_instance_dependency(
    value: bool = Depends(wrapped_class_instance_dep),
):
    return value


@app.get("/wrapped-class-instance-async-dependency/")
async def get_wrapped_class_instance_async_dependency(
    value: bool = Depends(wrapped_class_instance_async_dep),
):
    return value


@app.get("/wrapped-class-instance-gen-dependency/")
async def get_wrapped_class_instance_gen_dependency(
    value: bool = Depends(wrapped_class_instance_gen_dep),
):
    return value


@app.get("/wrapped-class-instance-async-gen-dependency/")
async def get_wrapped_class_instance_async_gen_dependency(
    value: bool = Depends(wrapped_class_instance_async_gen_dep),
):
    return value


@app.get("/class-instance-wrapped-dependency/")
async def get_class_instance_wrapped_dependency(
    value: bool = Depends(class_instance_wrapped_dep),
):
    return value


@app.get("/class-instance-wrapped-async-dependency/")
async def get_class_instance_wrapped_async_dependency(
    value: bool = Depends(class_instance_wrapped_async_dep),
):
    return value


@app.get("/class-instance-async-wrapped-dependency/")
async def get_class_instance_async_wrapped_dependency(
    value: bool = Depends(class_instance_async_wrapped_dep),
):
    return value


@app.get("/class-instance-async-wrapped-async-dependency/")
async def get_class_instance_async_wrapped_async_dependency(
    value: bool = Depends(class_instance_async_wrapped_async_dep),
):
    return value


@app.get("/class-instance-wrapped-gen-dependency/")
async def get_class_instance_wrapped_gen_dependency(
    value: bool = Depends(class_instance_wrapped_gen_dep),
):
    return value


@app.get("/class-instance-wrapped-async-gen-dependency/")
async def get_class_instance_wrapped_async_gen_dependency(
    value: bool = Depends(class_instance_wrapped_async_gen_dep),
):
    return value


@app.get("/class-instance-async-wrapped-gen-dependency/")
async def get_class_instance_async_wrapped_gen_dependency(
    value: bool = Depends(class_instance_async_wrapped_gen_dep),
):
    return value


@app.get("/class-instance-async-wrapped-gen-async-dependency/")
async def get_class_instance_async_wrapped_gen_async_dependency(
    value: bool = Depends(class_instance_async_wrapped_gen_async_dep),
):
    return value


@app.get("/wrapped-class-dependency/")
async def get_wrapped_class_dependency(value: ClassDep = Depends(wrapped_class_dep)):
    return value.value


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


@app.get("/wrapped-class-instance-dependency-async-wrapper/")
async def get_wrapped_class_instance_dependency_async_wrapper(
    value: bool = Depends(wrapped_class_instance_dep_async_wrapper),
):
    return value


@app.get("/wrapped-class-instance-async-dependency-async-wrapper/")
async def get_wrapped_class_instance_async_dependency_async_wrapper(
    value: bool = Depends(wrapped_class_instance_async_dep_async_wrapper),
):
    return value


@app.get("/wrapped-class-dependency-async-wrapper/")
async def get_wrapped_class_dependency_async_wrapper(
    value: ClassDep = Depends(wrapped_class_dep_async_wrapper),
):
    return value.value


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
        "/wrapped-class-instance-dependency/",
        "/wrapped-class-instance-async-dependency/",
        "/wrapped-class-instance-gen-dependency/",
        "/wrapped-class-instance-async-gen-dependency/",
        "/class-instance-wrapped-dependency/",
        "/class-instance-wrapped-async-dependency/",
        "/class-instance-async-wrapped-dependency/",
        "/class-instance-async-wrapped-async-dependency/",
        "/class-instance-wrapped-gen-dependency/",
        "/class-instance-wrapped-async-gen-dependency/",
        "/class-instance-async-wrapped-gen-dependency/",
        "/class-instance-async-wrapped-gen-async-dependency/",
        "/wrapped-class-dependency/",
        "/wrapped-endpoint/",
        "/async-wrapped-endpoint/",
        "/wrapped-dependency-async-wrapper/",
        "/wrapped-gen-dependency-async-wrapper/",
        "/async-wrapped-dependency-async-wrapper/",
        "/async-wrapped-gen-dependency-async-wrapper/",
        "/wrapped-class-instance-dependency-async-wrapper/",
        "/wrapped-class-instance-async-dependency-async-wrapper/",
        "/wrapped-class-dependency-async-wrapper/",
        "/wrapped-endpoint-async-wrapper/",
        "/async-wrapped-endpoint-async-wrapper/",
    ],
)
def test_class_dependency(route):
    response = client.get(route)
    assert response.status_code == 200, response.text
    assert response.json() is True
