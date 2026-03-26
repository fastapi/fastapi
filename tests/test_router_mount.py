from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from inline_snapshot import snapshot


def get_sub_app() -> FastAPI:
    sub_app = FastAPI()

    @sub_app.get("/sub")
    def read_sub():
        return {"message": "Hello World from sub API"}

    return sub_app


def test_mount_sub_application_with_router_prefix():
    router = APIRouter(prefix="/api")
    router.mount("/subapi", get_sub_app())

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    response = client.get("/api/subapi/sub")

    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World from sub API"}


def test_mount_sub_application_with_include_router_prefix():
    router = APIRouter()
    router.mount("/subapi", get_sub_app())

    app = FastAPI()
    app.include_router(router, prefix="/api")

    client = TestClient(app)
    response = client.get("/api/subapi/sub")

    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World from sub API"}


def test_mount_sub_application_openapi_with_included_router():
    router = APIRouter(prefix="/api")
    router.mount("/subapi", get_sub_app())

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    response = client.get("/api/subapi/openapi.json")

    assert response.status_code == 200, response.text
    assert response.json() == snapshot(
        {
            "openapi": "3.1.0",
            "info": {"title": "FastAPI", "version": "0.1.0"},
            "paths": {
                "/sub": {
                    "get": {
                        "summary": "Read Sub",
                        "operationId": "read_sub_sub_get",
                        "responses": {
                            "200": {
                                "description": "Successful Response",
                                "content": {"application/json": {"schema": {}}},
                            }
                        },
                    }
                }
            },
            "servers": [{"url": "/api/subapi"}],
        }
    )
