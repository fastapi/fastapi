from functools import partial

from fastapi import FastAPI
from starlette.testclient import TestClient


def main(some_arg, q: str = None):
    return {"some_arg": some_arg, "q": q}


endpoint = partial(main, "foo")

app = FastAPI()

app.get("/")(endpoint)


client = TestClient(app)


def test_partial():
    response = client.get("/?q=bar")
    data = response.json()
    assert data == {"some_arg": "foo", "q": "bar"}
