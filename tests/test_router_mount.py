from fastapi import APIRouter, FastAPI
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient


def test_mount_subapp_under_router_prefix() -> None:
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/ping")
    def ping() -> dict[str, str]:
        return {"message": "pong"}

    sub_app = FastAPI()

    @sub_app.get("/sub")
    def read_sub() -> dict[str, str]:
        return {"message": "Hello World from sub API"}

    api_router.mount("/subapi", sub_app)
    app.include_router(api_router)

    client = TestClient(app)

    response = client.get("/api/ping")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "pong"}

    mounted_response = client.get("/api/subapi/sub")
    assert mounted_response.status_code == 200, mounted_response.text
    assert mounted_response.json() == {"message": "Hello World from sub API"}


def test_mount_starlette_route_under_router_prefix() -> None:
    app = FastAPI()
    router = APIRouter(prefix="/v1")

    def plain_asgi_app(scope, receive, send):
        response = JSONResponse({"ok": True})
        return response(scope, receive, send)

    router.mount("/internal", plain_asgi_app, name="internal")
    app.include_router(router, prefix="/api")

    client = TestClient(app)
    response = client.get("/api/v1/internal")
    assert response.status_code == 200, response.text
    assert response.json() == {"ok": True}
