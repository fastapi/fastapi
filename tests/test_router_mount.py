"""
Tests for issue #10180: mounting sub-applications under APIRouter.

Sub-apps mounted on an APIRouter (with a prefix) must be reachable via the
combined prefix + mount-path after include_router().
"""

from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient


def make_sub_app() -> FastAPI:
    sub = FastAPI()

    @sub.get("/sub")
    def read_sub():
        return {"message": "Hello World from sub API"}

    return sub


# ---------------------------------------------------------------------------
# Router prefix baked into APIRouter(prefix=...) itself
# ---------------------------------------------------------------------------


def test_router_prefix_mount_routing():
    """Request to /api/subapi/sub must return 200 (issue #10180 exact repro)."""
    router = APIRouter(prefix="/api")

    @router.get("/app")
    def read_app():
        return {"message": "Hello World from main app"}

    router.mount("/subapi", make_sub_app())

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    assert client.get("/api/app").status_code == 200
    assert client.get("/api/subapi/sub").status_code == 200
    assert client.get("/api/subapi/sub").json() == {
        "message": "Hello World from sub API"
    }


# ---------------------------------------------------------------------------
# Prefix supplied via include_router(prefix=...)
# ---------------------------------------------------------------------------


def test_include_router_prefix_mount_routing():
    """Prefix from include_router() is applied to mounted sub-apps."""
    router = APIRouter()
    router.mount("/subapi", make_sub_app())

    app = FastAPI()
    app.include_router(router, prefix="/api")

    client = TestClient(app)
    assert client.get("/api/subapi/sub").status_code == 200
    assert client.get("/api/subapi/sub").json() == {
        "message": "Hello World from sub API"
    }


# ---------------------------------------------------------------------------
# Combination: both router prefix AND include_router prefix
# ---------------------------------------------------------------------------


def test_combined_prefix_mount_routing():
    """Router prefix and include_router prefix are both applied to mounts."""
    router = APIRouter(prefix="/api")
    router.mount("/subapi", make_sub_app())

    app = FastAPI()
    app.include_router(router, prefix="/v1")

    client = TestClient(app)
    assert client.get("/v1/api/subapi/sub").status_code == 200


# ---------------------------------------------------------------------------
# Nested routers
# ---------------------------------------------------------------------------


def test_nested_router_mount_routing():
    """Mounts survive two levels of include_router nesting."""
    inner = APIRouter(prefix="/inner")
    inner.mount("/subapi", make_sub_app())

    outer = APIRouter(prefix="/outer")
    outer.include_router(inner)

    app = FastAPI()
    app.include_router(outer)

    client = TestClient(app)
    assert client.get("/outer/inner/subapi/sub").status_code == 200


# ---------------------------------------------------------------------------
# Sub-app openapi.json is reachable at the correct path
# ---------------------------------------------------------------------------


def test_router_prefix_mount_openapi():
    """Sub-app's OpenAPI spec is accessible at the combined prefix path."""
    router = APIRouter(prefix="/api")
    router.mount("/subapi", make_sub_app())

    app = FastAPI()
    app.include_router(router)

    client = TestClient(app)
    response = client.get("/api/subapi/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert data["openapi"] == "3.1.0"
    assert "/sub" in data["paths"]
    # root_path is reflected in the servers list
    assert any("/api/subapi" in s["url"] for s in data.get("servers", []))


# ---------------------------------------------------------------------------
# Mounts directly on FastAPI app are unaffected
# ---------------------------------------------------------------------------


def test_direct_app_mount_unaffected():
    """Existing behaviour: mounting directly on FastAPI still works."""
    app = FastAPI()
    app.mount("/subapi", make_sub_app())

    client = TestClient(app)
    assert client.get("/subapi/sub").status_code == 200
