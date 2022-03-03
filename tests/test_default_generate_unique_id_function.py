from fastapi import APIRouter, FastAPI
from fastapi.routing import APIRoute
from fastapi.testclient import TestClient


def custom_generate_unique_id(route: APIRoute):
    return f"foo_{route.name}"


def test_top_level_generate_unique_id():
    app = FastAPI(generate_unique_id_function=custom_generate_unique_id)
    router = APIRouter()

    @app.get("/")
    def get_root():
        return {"msg": "Hello World"}  # pragma: nocover

    @router.get("/router")
    def get_router():
        return {"msg": "Hello Router"}  # pragma: nocover

    app.include_router(router)
    client = TestClient(app)
    response = client.get("/openapi.json")
    data = response.json()
    assert data == {
        "openapi": "3.0.2",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/": {
                "get": {
                    "summary": "Get Root",
                    "operationId": "foo_get_root",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
            "/router": {
                "get": {
                    "summary": "Get Router",
                    "operationId": "foo_get_router",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                }
            },
        },
    }
