from fastapi import FastAPI, APIRouter
from fastapi.testclient import TestClient


def test_mount_on_router():
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

    assert client.get("/api/app").status_code == 200
    assert client.get("/api/subapi/sub").status_code == 200