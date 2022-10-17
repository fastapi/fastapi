from functools import partial
from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient


class CallableObjectEndpoint:
    def __call__(self, some_arg, q: Optional[str] = None):
        return {"some_arg": some_arg, "q": q}


class AsyncCallableObjectEndpoint:
    async def __call__(self, some_arg, q: Optional[str] = None):
        return {"some_arg": some_arg, "q": q}


def main(some_arg, q: Optional[str] = None):
    return {"some_arg": some_arg, "q": q}


endpoint = partial(main, "foo")
obj_endpoint = partial(CallableObjectEndpoint(), "foo")
async_obj_endpoint = partial(AsyncCallableObjectEndpoint(), "foo")

app = FastAPI()

app.get("/")(endpoint)
app.get("/obj")(obj_endpoint)
app.get("/async_obj")(async_obj_endpoint)


client = TestClient(app)


def test_partial():
    response = client.get("/?q=bar")
    data = response.json()
    assert data == {"some_arg": "foo", "q": "bar"}

    response = client.get("/obj?q=bar")
    data = response.json()
    assert data == {"some_arg": "foo", "q": "bar"}

    response = client.get("/async_obj?q=bar")
    data = response.json()
    assert data == {"some_arg": "foo", "q": "bar"}
