"""Test for async wrapper around sync function.

This tests the issue reported in #14442 where using functools.wraps on an async
wrapper around a sync function causes FastAPI to incorrectly treat the handler
as sync, resulting in: ValueError: [TypeError("'coroutine' object is not iterable"), ...]

The issue is that Dependant.is_coroutine_callable uses inspect.unwrap() which follows
__wrapped__ back to the original sync function, instead of checking if the actual
registered handler is async.
"""

from functools import wraps

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


def async_wrap(func):
    """A decorator that wraps a sync function with an async handler."""

    @wraps(func)
    async def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        return "OK"

    return wrapper


app = FastAPI()


@app.get("/")
@async_wrap
def index():
    """A simple sync page function wrapped with async handler."""
    print("Hello!")


def sync_dependency():
    return "dep_value"


@app.get("/with-dependency")
@async_wrap
def with_dependency(value: str = Depends(sync_dependency)):
    """A sync function with dependency, wrapped with async handler."""
    print(f"Got: {value}")


client = TestClient(app)


def test_async_wrapper_around_sync_function():
    """Test that async wrapper around sync function works correctly."""
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == "OK"


def test_async_wrapper_with_dependency():
    """Test that async wrapper with dependency works correctly."""
    response = client.get("/with-dependency")
    assert response.status_code == 200, response.text
    assert response.json() == "OK"
