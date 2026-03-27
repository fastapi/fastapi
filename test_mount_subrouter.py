"""Test for issue #10180: Mounting sub-applications under APIRouter."""

from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient


def test_mount_subapp_under_router():
    """Sub-application mounted under APIRouter should be reachable."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    @api_router.get("/app")
    def read_main():
        return {"message": "Hello World from main app"}

    subapi = FastAPI()

    @subapi.get("/sub")
    def read_sub():
        return {"message": "Hello World from sub API"}

    api_router.mount("/subapi", subapi)
    app.include_router(api_router)

    client = TestClient(app)

    response = client.get("/api/app")
    assert response.status_code == 200

    response = client.get("/api/subapi/sub")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from sub API"}


def test_mount_subapp_docs():
    """Sub-application should have its own OpenAPI docs."""
    app = FastAPI()
    api_router = APIRouter(prefix="/api")

    subapi = FastAPI()

    @subapi.get("/sub")
    def read_sub():
        return {"message": "sub"}

    api_router.mount("/subapi", subapi)
    app.include_router(api_router)

    client = TestClient(app)
    response = client.get("/api/subapi/docs")
    assert response.status_code == 200


def test_mount_multiple_subapps():
    """Multiple sub-apps under the same router."""
    app = FastAPI()
    api_router = APIRouter(prefix="/v1")

    sub1 = FastAPI()

    @sub1.get("/hello")
    def hello():
        return {"msg": "hello"}

    sub2 = FastAPI()

    @sub2.get("/world")
    def world():
        return {"msg": "world"}

    api_router.mount("/a", sub1)
    api_router.mount("/b", sub2)
    app.include_router(api_router)

    client = TestClient(app)
    assert client.get("/v1/a/hello").status_code == 200
    assert client.get("/v1/b/world").status_code == 200
