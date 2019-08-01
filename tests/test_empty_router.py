import pytest
from fastapi import APIRouter, FastAPI
from starlette.testclient import TestClient

app = FastAPI()

router = APIRouter()


@router.get("")
def get_empty():
    return ["OK"]


app.include_router(router, prefix="/prefix")


client = TestClient(app)


def test_use_empty():
    with client:
        response = client.get("/prefix")
        assert response.json() == ["OK"]

        response = client.get("/prefix/")
        assert response.status_code == 404


def test_include_empty():
    # if both include and router.path are empty - it should raise exception
    with pytest.raises(Exception):
        app.include_router(router)
