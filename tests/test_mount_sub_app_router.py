from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from starlette.routing import Mount


def test_sub_app_mounted_on_router_is_accessible():
    """Sub-apps mounted on an APIRouter should be reachable after include_router."""
    sub_app = FastAPI()

    @sub_app.get("/status")
    def sub_status():
        return {"status": "ok"}

    router = APIRouter()
    router.mount("/sub", sub_app)

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    response = client.get("/sub/status")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_sub_app_with_router_prefix():
    """The include_router prefix should be prepended to the mount path."""
    sub_app = FastAPI()

    @sub_app.get("/info")
    def sub_info():
        return {"info": "value"}

    router = APIRouter()
    router.mount("/sub", sub_app)

    app = FastAPI()
    app.include_router(router, prefix="/api")

    client = TestClient(app)
    response = client.get("/api/sub/info")
    assert response.status_code == 200
    assert response.json() == {"info": "value"}


def test_mount_preserved_in_routes():
    """Verify the Mount object ends up in app.routes."""
    sub_app = FastAPI()
    router = APIRouter()
    router.mount("/sub", sub_app)

    app = FastAPI()
    app.include_router(router)

    mount_routes = [
        r for r in app.routes if isinstance(r, Mount) and "/sub" in r.path
    ]
    assert len(mount_routes) == 1
