from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(
    openapi_schema_exclude_unset=True,
    openapi_schema_exclude_none=False,
)


@app.get(
    "/items",
    responses={
        200: {"content": {"application/json": {"example": {"id": None, "value": 50}}}}
    },
)
def get_items():
    return {"id": "foo", "value": 50}


client = TestClient(app)


openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/items": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {
                                "schema": {},
                                "example": {"id": None, "value": 50},
                            }
                        },
                    }
                },
                "summary": "Get Items",
                "operationId": "get_items_items_get",
            }
        }
    },
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == openapi_schema


def test_default_get_items():
    response = client.get("/items")
    assert response.status_code == 200, response.text
    assert response.json() == {"id": "foo", "value": 50}
