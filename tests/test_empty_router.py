import pytest
from fastapi import APIRouter, FastAPI
from fastapi.exceptions import FastAPIError
from fastapi.testclient import TestClient

app = FastAPI()

router = APIRouter()


@router.get("")
def get_empty():
    return ["OK"]


app.include_router(router, prefix="/prefix")


client = TestClient(app)


@pytest.mark.parametrize("prefix", ["/prefix", "/prefix/"])
def test_use_empty_with_prefix(prefix):
    with client:
        response = client.get(prefix)
        assert response.status_code == 200, response.text
        assert response.json() == ["OK"]


def test_include_empty():
    # if both include and router.path are empty - it should raise exception
    with pytest.raises(FastAPIError):
        app.include_router(router)
