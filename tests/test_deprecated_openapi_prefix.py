from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

app = FastAPI(openapi_prefix="/api/v1")


@app.get("/app")
def read_main(request: Request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {
        "/api/v1/app": {
            "get": {
                "summary": "Read Main",
                "operationId": "read_main_app_get",
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


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_main():
    response = client.get("/app")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World", "root_path": "/api/v1"}
