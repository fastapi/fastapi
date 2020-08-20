from fastapi import APIRouter, FastAPI
from fastapi.testclient import TestClient
from pytest import mark

app = FastAPI()
client = TestClient(app)

sub_router = APIRouter()
another_sub_router = APIRouter()

METHODS = ["get", "post", "put", "patch", "delete", "trace"]

for method in METHODS:

    @getattr(app, method)
    def route(m=method):
        return {"result": f"root-{m}"}

    @getattr(sub_router, method)
    def sub_route(m=method):
        return {"result": f"sub-no-params-{m}"}

    decorator = getattr(another_sub_router, method)

    @decorator()
    def another_sub_route(m=method):
        return {"result": f"sub-with-params-{m}"}


app.include_router(sub_router, prefix="/sub")
app.include_router(another_sub_router, prefix="/another-sub")


@mark.parametrize("method", METHODS)
def test_root_router(method):
    response = client.request(method, "/")
    assert response.json() == {"result": f"root-{method}"}


@mark.parametrize("method", METHODS)
def test_sub_router(method):
    response = client.request(method, "/sub")
    assert response.json() == {"result": f"sub-no-params-{method}"}


@mark.parametrize("method", METHODS)
def test_another_sub_router(method):
    response = client.request(method, "/another-sub")
    assert response.json() == {"result": f"sub-with-params-{method}"}
