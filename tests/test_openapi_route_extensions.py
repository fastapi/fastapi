from fastapi import FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot

app = FastAPI()


@app.get("/", openapi_extra={"x-custom-extension": "value"})
def route_with_extras():
    return {}


client = TestClient(app)


def test_get_route():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/": {
                    "get": {
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            },
                        },
                        "summary": "Route With Extras",
                        "operationId": "route_with_extras__get",
                        "x-custom-extension": "value",
                    }
                },
            },
        }
    )
