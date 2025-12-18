from collections.abc import AsyncGenerator, Generator
from functools import partial
from typing import Annotated

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


def function_dependency(value: str) -> str:
    return value


async def async_function_dependency(value: str) -> str:
    return value


def gen_dependency(value: str) -> Generator[str, None, None]:
    yield value


async def async_gen_dependency(value: str) -> AsyncGenerator[str, None]:
    yield value


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


@app.get("/partial-function-dependency")
async def get_partial_function_dependency(
    value: Annotated[
        str, Depends(partial(function_dependency, "partial-function-dependency"))
    ],
) -> str:
    return value


@app.get("/partial-async-function-dependency")
async def get_partial_async_function_dependency(
    value: Annotated[
        str,
        Depends(
            partial(async_function_dependency, "partial-async-function-dependency")
        ),
    ],
) -> str:
    return value


@app.get("/partial-gen-dependency")
async def get_partial_gen_dependency(
    value: Annotated[str, Depends(partial(gen_dependency, "partial-gen-dependency"))],
) -> str:
    return value


@app.get("/partial-async-gen-dependency")
async def get_partial_async_gen_dependency(
    value: Annotated[
        str, Depends(partial(async_gen_dependency, "partial-async-gen-dependency"))
    ],
) -> str:
    return value


@app.get("/partial-callable-dependency")
async def get_partial_callable_dependency(
    value: Annotated[
        str, Depends(partial(callable_dependency, "partial-callable-dependency"))
    ],
) -> str:
    return value


@app.get("/partial-callable-gen-dependency")
async def get_partial_callable_gen_dependency(
    value: Annotated[
        str,
        Depends(partial(callable_gen_dependency, "partial-callable-gen-dependency")),
    ],
) -> str:
    return value


@app.get("/partial-async-callable-dependency")
async def get_partial_async_callable_dependency(
    value: Annotated[
        str,
        Depends(
            partial(async_callable_dependency, "partial-async-callable-dependency")
        ),
    ],
) -> str:
    return value


@app.get("/partial-async-callable-gen-dependency")
async def get_partial_async_callable_gen_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                async_callable_gen_dependency, "partial-async-callable-gen-dependency"
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-synchronous-method-dependency")
async def get_partial_synchronous_method_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.synchronous, "partial-synchronous-method-dependency"
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-synchronous-method-gen-dependency")
async def get_partial_synchronous_method_gen_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.synchronous_gen,
                "partial-synchronous-method-gen-dependency",
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-asynchronous-method-dependency")
async def get_partial_asynchronous_method_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.asynchronous,
                "partial-asynchronous-method-dependency",
            )
        ),
    ],
) -> str:
    return value


@app.get("/partial-asynchronous-method-gen-dependency")
async def get_partial_asynchronous_method_gen_dependency(
    value: Annotated[
        str,
        Depends(
            partial(
                methods_dependency.asynchronous_gen,
                "partial-asynchronous-method-gen-dependency",
            )
        ),
    ],
) -> str:
    return value


client = TestClient(app)


@pytest.mark.parametrize(
    "route,value",
    [
        ("/partial-function-dependency", "partial-function-dependency"),
        (
            "/partial-async-function-dependency",
            "partial-async-function-dependency",
        ),
        ("/partial-gen-dependency", "partial-gen-dependency"),
        ("/partial-async-gen-dependency", "partial-async-gen-dependency"),
        ("/partial-callable-dependency", "partial-callable-dependency"),
        ("/partial-callable-gen-dependency", "partial-callable-gen-dependency"),
        ("/partial-async-callable-dependency", "partial-async-callable-dependency"),
        (
            "/partial-async-callable-gen-dependency",
            "partial-async-callable-gen-dependency",
        ),
        (
            "/partial-synchronous-method-dependency",
            "partial-synchronous-method-dependency",
        ),
        (
            "/partial-synchronous-method-gen-dependency",
            "partial-synchronous-method-gen-dependency",
        ),
        (
            "/partial-asynchronous-method-dependency",
            "partial-asynchronous-method-dependency",
        ),
        (
            "/partial-asynchronous-method-gen-dependency",
            "partial-asynchronous-method-gen-dependency",
        ),
    ],
)
def test_dependency_types_with_partial(route: str, value: str) -> None:
    response = client.get(route)
    assert response.status_code == 200, response.text
    assert response.json() == value
