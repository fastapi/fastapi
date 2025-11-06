from typing import Any

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.testclient import TestClient


def broken_dependency() -> Any:
    yield "s"
    raise RuntimeError("Caught exception after yield")


def caught_dependency() -> Any:
    yield "s"
    raise HTTPException(status_code=503, detail="Something went wrong")


app = FastAPI()

r_caught_function = APIRouter(
    prefix="/scope/function/caught",
    dependencies=[Depends(caught_dependency, scope="function")],
)
r_broken_function = APIRouter(
    prefix="/scope/function/broken",
    dependencies=[Depends(broken_dependency, scope="function")],
)

r_caught_request = APIRouter(
    prefix="/scope/request/caught",
    dependencies=[Depends(caught_dependency, scope="request")],
)
r_broken_request = APIRouter(
    prefix="/scope/request/broken",
    dependencies=[Depends(broken_dependency, scope="request")],
)


@r_caught_function.get("/orders")
@r_broken_function.get("/orders")
@r_caught_request.get("/orders")
@r_broken_request.get("/orders")
def get_orders() -> Any:
    return {"message": "Maybe not here!"}


app.include_router(r_caught_function)
app.include_router(r_broken_function)

app.include_router(r_caught_request)
app.include_router(r_broken_request)


def test_caught_dependency_scope_function():
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/scope/function/caught/orders")
        assert response.status_code == 503
        assert response.json() == {"detail": "Something went wrong"}


def test_broken_dependency_scope_function():
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/scope/function/broken/orders")
        assert response.status_code == 500
        assert response.content == b"Internal Server Error"


def test_caught_dependency_scope_request():
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/scope/request/caught/orders")
        assert response.status_code == 200
        assert response.json() == {"message": "Maybe not here!"}


def test_broken_dependency_scope_request():
    with TestClient(app, raise_server_exceptions=False) as client:
        response = client.get("/scope/request/broken/orders")
        assert response.status_code == 200
        assert response.json() == {"message": "Maybe not here!"}
