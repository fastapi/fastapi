from typing import AsyncGenerator, Generator

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


class CallableDependency:
    def __call__(self, value: str) -> str:
        return value


class CallableGenDependency:
    def __call__(self, value: str) -> Generator[str, None, None]:
        yield value


class AsyncCallableDependency:
    async def __call__(self, value: str) -> str:
        return value


class AsyncCallableGenDependency:
    async def __call__(self, value: str) -> AsyncGenerator[str, None]:
        yield value


class MethodsDependency:
    def synchronous(self, value: str) -> str:
        return value

    async def asynchronous(self, value: str) -> str:
        return value

    def synchronous_gen(self, value: str) -> Generator[str, None, None]:
        yield value

    async def asynchronous_gen(self, value: str) -> AsyncGenerator[str, None]:
        yield value


callable_dependency = CallableDependency()
callable_gen_dependency = CallableGenDependency()
async_callable_dependency = AsyncCallableDependency()
async_callable_gen_dependency = AsyncCallableGenDependency()
methods_dependency = MethodsDependency()


@app.get("/callable-dependency")
async def get_callable_dependency(value: str = Depends(callable_dependency)):
    return value


@app.get("/callable-gen-dependency")
async def get_callable_gen_dependency(value: str = Depends(callable_gen_dependency)):
    return value


@app.get("/async-callable-dependency")
async def get_async_callable_dependency(
    value: str = Depends(async_callable_dependency),
):
    return value


@app.get("/async-callable-gen-dependency")
async def get_async_callable_gen_dependency(
    value: str = Depends(async_callable_gen_dependency),
):
    return value


@app.get("/synchronous-method-dependency")
async def get_synchronous_method_dependency(
    value: str = Depends(methods_dependency.synchronous),
):
    return value


@app.get("/synchronous-method-gen-dependency")
async def get_synchronous_method_gen_dependency(
    value: str = Depends(methods_dependency.synchronous_gen),
):
    return value


@app.get("/asynchronous-method-dependency")
async def get_asynchronous_method_dependency(
    value: str = Depends(methods_dependency.asynchronous),
):
    return value


@app.get("/asynchronous-method-gen-dependency")
async def get_asynchronous_method_gen_dependency(
    value: str = Depends(methods_dependency.asynchronous_gen),
):
    return value


client = TestClient(app)


@pytest.mark.parametrize(
    "route,value",
    [
        ("/callable-dependency", "callable-dependency"),
        ("/callable-gen-dependency", "callable-gen-dependency"),
        ("/async-callable-dependency", "async-callable-dependency"),
        ("/async-callable-gen-dependency", "async-callable-gen-dependency"),
        ("/synchronous-method-dependency", "synchronous-method-dependency"),
        ("/synchronous-method-gen-dependency", "synchronous-method-gen-dependency"),
        ("/asynchronous-method-dependency", "asynchronous-method-dependency"),
        ("/asynchronous-method-gen-dependency", "asynchronous-method-gen-dependency"),
    ],
)
def test_class_dependency(route, value):
    response = client.get(route, params={"value": value})
    assert response.status_code == 200, response.text
    assert response.json() == value
