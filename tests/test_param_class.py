from fastapi import FastAPI
from fastapi.params import Param
from starlette.testclient import TestClient

app = FastAPI()


@app.get("/items/")
def read_items(q: str = Param(None)):
    return {"q": q}


client = TestClient(app)


def test_default_param_query_none():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == {"q": None}


def test_default_param_query():
    response = client.get("/items/?q=foo")
    assert response.status_code == 200
    assert response.json() == {"q": "foo"}
