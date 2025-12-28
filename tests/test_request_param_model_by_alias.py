from dirty_equals import IsPartialDict
from fastapi import Cookie, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class Model(BaseModel):
    param: str = Field(alias="param_alias")


@app.get("/query")
async def query_model(data: Model = Query()):
    return {"param": data.param}


@app.get("/header")
async def header_model(data: Model = Header()):
    return {"param": data.param}


@app.get("/cookie")
async def cookie_model(data: Model = Cookie()):
    return {"param": data.param}


def test_query_model_with_alias():
    client = TestClient(app)
    response = client.get("/query", params={"param_alias": "value"})
    assert response.status_code == 200, response.text
    assert response.json() == {"param": "value"}


def test_header_model_with_alias():
    client = TestClient(app)
    response = client.get("/header", headers={"param_alias": "value"})
    assert response.status_code == 200, response.text
    assert response.json() == {"param": "value"}


def test_cookie_model_with_alias():
    client = TestClient(app)
    client.cookies.set("param_alias", "value")
    response = client.get("/cookie")
    assert response.status_code == 200, response.text
    assert response.json() == {"param": "value"}


def test_query_model_with_alias_by_name():
    client = TestClient(app)
    response = client.get("/query", params={"param": "value"})
    assert response.status_code == 422, response.text
    details = response.json()
    assert details["detail"][0]["input"] == {"param": "value"}


def test_header_model_with_alias_by_name():
    client = TestClient(app)
    response = client.get("/header", headers={"param": "value"})
    assert response.status_code == 422, response.text
    details = response.json()
    assert details["detail"][0]["input"] == IsPartialDict({"param": "value"})


def test_cookie_model_with_alias_by_name():
    client = TestClient(app)
    client.cookies.set("param", "value")
    response = client.get("/cookie")
    assert response.status_code == 422, response.text
    details = response.json()
    assert details["detail"][0]["input"] == {"param": "value"}
