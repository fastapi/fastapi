from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(
    servers=[
        {"url": "/", "description": "Default, relative server"},
        {
            "url": "http://staging.localhost.tiangolo.com:8000",
            "description": "Staging but actually localhost still",
        },
        {"url": "https://prod.example.com"},
    ]
)


@app.get("/foo")
def foo():
    return {"message": "Hello World"}


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "servers": [
        {"url": "/", "description": "Default, relative server"},
        {
            "url": "http://staging.localhost.tiangolo.com:8000",
            "description": "Staging but actually localhost still",
        },
        {"url": "https://prod.example.com"},
    ],
    "paths": {
        "/foo": {
            "get": {
                "summary": "Foo",
                "operationId": "foo_foo_get",
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {"application/json": {"schema": {}}},
                    }
                },
            }
        }
    },
}


def test_openapi_servers():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_app():
    response = client.get("/foo")
    assert response.status_code == 200, response.text
