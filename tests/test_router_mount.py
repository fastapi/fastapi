"""Tests for mounting sub-applications under APIRouter (issue #10180)."""
from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles
from starlette.testclient import TestClient


def test_mount_subapp_under_router_with_prefix() -> None:
    """APIRouter with prefix should propagate Mount to the main app."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/app")
    def read_main() -> dict:
        return {"message": "Hello World from main app"}

    subapi = FastAPI()

    @subapi.get("/sub")
    def read_sub() -> dict:
        return {"message": "Hello World from sub API"}

    api_router.mount("/subapi", subapi)
    app.include_router(api_router)

    client = TestClient(app)

    # Regular route should still work
    r = client.get("/api/app")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello World from main app"}

    # Mounted sub-app should be accessible under router prefix
    r = client.get("/api/subapi/sub")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello World from sub API"}


def test_mount_subapp_under_router_without_prefix() -> None:
    """APIRouter without prefix should propagate Mount correctly."""
    app = FastAPI()
    router = APIRouter()

    subapi = FastAPI()

    @subapi.get("/hello")
    def hello() -> dict:
        return {"msg": "hello"}

    router.mount("/sub", subapi)
    app.include_router(router)

    client = TestClient(app)

    r = client.get("/sub/hello")
    assert r.status_code == 200
    assert r.json() == {"msg": "hello"}


def test_mount_subapp_with_include_router_prefix() -> None:
    """include_router prefix should be combined with router prefix and mount path."""
    app = FastAPI()
    router = APIRouter(prefix="/api")

    subapi = FastAPI()

    @subapi.get("/test")
    def test_endpoint() -> dict:
        return {"msg": "test"}

    router.mount("/sub", subapi)
    app.include_router(router, prefix="/v1")

    client = TestClient(app)

    r = client.get("/v1/api/sub/test")
    assert r.status_code == 200
    assert r.json() == {"msg": "test"}


def test_mount_preserves_regular_routes() -> None:
    """Adding Mount support should not break existing APIRoute handling."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/items")
    def list_items() -> dict:
        return {"items": [1, 2, 3]}

    @api_router.post("/items")
    def create_item() -> dict:
        return {"created": True}

    subapi = FastAPI()

    @subapi.get("/status")
    def status() -> dict:
        return {"status": "ok"}

    api_router.mount("/health", subapi)
    app.include_router(api_router)

    client = TestClient(app)

    assert client.get("/api/items").status_code == 200
    assert client.post("/api/items").status_code == 200
    assert client.get("/api/health/status").status_code == 200
