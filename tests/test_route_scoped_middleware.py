from fastapi import APIRouter, FastAPI, Request
from fastapi.testclient import TestClient
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware


class SubrouteMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        return {"message": "Middleware"}


app = FastAPI()

router = APIRouter(prefix="/route", middleware=[Middleware(SubrouteMiddleware)])


@router.get("/hello")
def hello():
    return {"message": "Subroute"}


app.include_router(router)


@app.get("/hello")
async def main():
    return {"message": "World"}


client = TestClient(app)


def test_router_scoped_middleware():
    client = TestClient(app)

    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "World"}

    response = client.get("/route/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Middleware"}
