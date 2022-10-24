"""Test case for possible tag duplication to prevent issues with '/redoc'"""

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()
router = APIRouter(tags=["items", "items"])


@router.get("/items/")
def read_items(request: Request):
    return JSONResponse({"hello": "world"})


app.include_router(router)


@app.get("/test/", tags=["test", "test"])
def read_test():
    return "test"


client = TestClient(app)


def test_openapi_for_duplicates():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert '"tags":["items"]' in response.text
    assert '"tags":["test"]' in response.text


def test_items_url():
    response = client.get("/items")
    assert response.status_code == 200, response.text


def test_test_url():
    response = client.get("/test")
    assert response.status_code == 200, response.text
