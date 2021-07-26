from typing import Any

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.testclient import TestClient


class Hotdog:
    ...


class RawResponse(PlainTextResponse):
    __handles_raw_response__ = True

    def render(self, content: Any) -> bytes:
        if isinstance(content, Hotdog):
            return "hotdog".encode("utf-8")
        else:
            return "not-hotdog".encode("utf-8")


app = FastAPI(default_response_class=RawResponse)


@app.get("/")
def get_root(want_dog: bool):
    if want_dog:
        return Hotdog()
    else:
        return "Hello World"


client = TestClient(app)


def test_uses_raw_response():
    with client:
        response = client.get("/?want_dog=True")
    assert response.text == "hotdog"
    with client:
        response = client.get("/?want_dog=False")
    assert response.text == "not-hotdog"
