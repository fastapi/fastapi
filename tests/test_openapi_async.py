from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_allow_async_openapi():
    async def async_openapi():
        return {"foo": "bar"}

    mod_app = FastAPI()  # use fresh instance to not affect other tests
    mod_app.openapi = async_openapi
    mod_client = TestClient(mod_app)
    response = mod_client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {"foo": "bar"}
