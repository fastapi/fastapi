from functools import wraps
from typing import AsyncGenerator, Generator

import pytest
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


def noop_wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper


app = FastAPI()


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


client = TestClient(app)


@pytest.mark.parametrize(
    "route",
    [
        "/wrapped-dependency",
        "/wrapped-gen-dependency",
        "/async-wrapped-dependency",
        "/async-wrapped-gen-dependency",
    ],
)
def test_class_dependency(route):
    response = client.get(route)
    assert response.status_code == 200, response.text
    assert response.json() is True
