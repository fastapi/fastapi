from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient

app = FastAPI()
router = APIRouter()


@router.route("/items/")
def read_items(request: Request):
    return JSONResponse({"hello": "world"})


app.include_router(router)

client = TestClient(app)


def test_sub_router():
    response = client.get("/items/")
    assert response.status_code == 200, response.text
    assert response.json() == {"hello": "world"}
