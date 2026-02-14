"""Test mounting sub-applications under APIRouter."""

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient


def test_router_mount_basic():
    """Sub-applications mounted on a router should work when included in the app."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/main")
    def read_main():
        return {"message": "Hello from main"}

    subapi = FastAPI()

    @subapi.get("/sub")
    def read_sub():
        return {"message": "Hello from sub"}

    # Mount BEFORE include_router
    api_router.mount("/subapi", subapi)
    app.include_router(api_router)

    client = TestClient(app)

    # Main route should work
    response = client.get("/api/main")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from main"}

    # Sub-application route should also work
    response = client.get("/api/subapi/sub")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from sub"}


def test_router_mount_with_include_prefix():
    """Mount path should combine with both router prefix and include_router prefix."""
    app = FastAPI()
    api_router = APIRouter(prefix="/v1")

    subapi = FastAPI()

    @subapi.get("/endpoint")
    def sub_endpoint():
        return {"version": "1"}

    api_router.mount("/mounted", subapi)
    app.include_router(api_router, prefix="/api")

    client = TestClient(app)

    # Full path: /api + /v1 + /mounted + /endpoint
    response = client.get("/api/v1/mounted/endpoint")
    assert response.status_code == 200
    assert response.json() == {"version": "1"}


def test_router_mount_without_prefix():
    """Mount should work on router without prefix."""
    app = FastAPI()
    api_router = APIRouter()  # No prefix

    subapi = FastAPI()

    @subapi.get("/hello")
    def hello():
        return {"hello": "world"}

    api_router.mount("/sub", subapi)
    app.include_router(api_router)

    client = TestClient(app)

    response = client.get("/sub/hello")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_router_mount_applies_router_prefix():
    """Mount path should include the router's prefix."""
    router = APIRouter(prefix="/api")

    subapi = FastAPI()

    @subapi.get("/test")
    def test_route():
        return {"test": True}

    router.mount("/mounted", subapi)

    # Check that the mount path includes the router prefix
    mount_route = None
    for route in router.routes:
        if hasattr(route, "path") and "mounted" in route.path:
            mount_route = route
            break

    assert mount_route is not None
    assert mount_route.path == "/api/mounted"


def test_router_mount_multiple_subapps():
    """Multiple sub-applications can be mounted on the same router."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    subapi1 = FastAPI()
    subapi2 = FastAPI()

    @subapi1.get("/one")
    def route_one():
        return {"app": 1}

    @subapi2.get("/two")
    def route_two():
        return {"app": 2}

    api_router.mount("/first", subapi1)
    api_router.mount("/second", subapi2)
    app.include_router(api_router)

    client = TestClient(app)

    response1 = client.get("/api/first/one")
    assert response1.status_code == 200
    assert response1.json() == {"app": 1}

    response2 = client.get("/api/second/two")
    assert response2.status_code == 200
    assert response2.json() == {"app": 2}
