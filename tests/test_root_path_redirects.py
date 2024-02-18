from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient


def test_redirects_without_root_path():
    app = FastAPI()
    router = APIRouter()

    @router.get("/hello/")
    def hello_page() -> str:
        return "Hello, World!"

    app.include_router(router)

    client = TestClient(app, base_url="http://testserver")

    response = client.get("/hello", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "http://testserver/hello/"


def test_redirects_with_root_path():
    app = FastAPI(root_path="/api")
    router = APIRouter()

    @router.get("/hello/")
    def hello_page() -> str:
        return "Hello, World!"

    app.include_router(router)

    client = TestClient(app, base_url="http://testserver")

    response = client.get("/hello", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "http://testserver/api/hello/"
