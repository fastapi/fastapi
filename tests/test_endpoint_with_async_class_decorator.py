from functools import update_wrapper

from fastapi import FastAPI
from fastapi.testclient import TestClient


class SomeDecorator:
    def __init__(self, original_route):
        update_wrapper(wrapper=self, wrapped=original_route)
        self.route = original_route

    async def __call__(self, *args, **kwargs):
        return await self.route(*args, **kwargs)


app = FastAPI()

@app.get("/")
@SomeDecorator
async def route1():
    return {"working": True}

client = TestClient(app)


def test_endpoint_with_async_class_decorator():
    response = client.get("/")
    assert response.json() == {"working": True}
