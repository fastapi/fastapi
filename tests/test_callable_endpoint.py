from functools import partial
from typing import Optional

from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient


def main(some_arg, q: Optional[str] = None):
    return {"some_arg": some_arg, "q": q}


def partial_func(q: str):
    async def inner(data):
        return data

    return partial(inner, q + " extras")


def async_partial_deps_func(data: str = Depends(partial_func("test"))):
    return {"data": data}


endpoint = partial(main, "foo")

app = FastAPI()

app.get("/")(endpoint)

async_partial_deps_endpoint = async_partial_deps_func

app.get("/async_partial_dps")(async_partial_deps_endpoint)


client = TestClient(app)


def test_partial():
    response = client.get("/?q=bar")
    data = response.json()
    assert data == {"some_arg": "foo", "q": "bar"}
    response = client.get("/async_partial_dps")
    data = response.json()
    assert data == {"data": "test extras"}
