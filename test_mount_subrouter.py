"""Test for issue #10180: Mounting sub-applications under APIRouter."""
from fastapi import FastAPI, APIRouter
from starlette.testclient import TestClient


def test_mount_subapp_under_router():
    """Sub-application mounted under APIRouter should be reachable."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/app")
    def read_main():
        return {"message": "Hello World from main app"}

    app.include_router(api_router)

    subapi = FastAPI()

    @subapi.get("/sub")
    def read_sub():
        return {"message": "Hello World from sub API"}

    api_router.mount("/subapi", subapi)

    client = TestClient(app)

    # Main app endpoint works
    response = client.get("/api/app")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from main app"}

    # Sub-application endpoint should work (this is the bug)
    response = client.get("/api/subapi/sub")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from sub API"}


def test_mount_subapp_docs():
    """Sub-application should have its own OpenAPI docs."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")
    app.include_router(api_router)

    subapi = FastAPI()

    @subapi.get("/sub")
    def read_sub():
        return {"message": "sub"}

    api_router.mount("/subapi", subapi)

    client = TestClient(app)

    # Sub-app docs should be accessible
    response = client.get("/api/subapi/docs")
    assert response.status_code == 200


def test_mount_subapp_after_include():
    """Mounting a sub-app after include_router should still work."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/main")
    def read_main():
        return {"ok": True}

    # Mount sub-app BEFORE include_router
    subapi = FastAPI()

    @subapi.get("/endpoint")
    def read_endpoint():
        return {"sub": True}

    api_router.mount("/sub", subapi)
    app.include_router(api_router)

    client = TestClient(app)
    assert client.get("/api/main").status_code == 200
    assert client.get("/api/sub/endpoint").status_code == 200
