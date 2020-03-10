import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/a", responses={"hello": {"description": "Not a valid additional response"}})
async def a():
    pass  # pragma: no cover


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/a": {
            "get": {
                "responses": {
                    # this is how one would imagine the openapi schema to be
                    # but since the key is not valid, openapi.utils.get_openapi will raise ValueError
                    "hello": {"description": "Not a valid additional response"},
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    },
                },
                "summary": "A",
                "operationId": "a_a_get",
            }
        }
    },
}

client = TestClient(app)


def test_openapi_schema():
    with pytest.raises(ValueError):
        client.get("/openapi.json")
