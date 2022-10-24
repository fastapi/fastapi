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


@app.get('/test/', tags=["test", "test"])
def read_test():
    return "test"


client = TestClient(app)


def test_sub_router():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert '"tags":["items"]' in response.text
    assert '"tags":["test"]' in response.text
