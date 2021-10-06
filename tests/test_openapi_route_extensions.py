from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/", openapi_extra={"x-custom-extension": "value"})
def route_with_extras():
    return {}


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
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


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_get_route():
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {}
