import pytest
from fastapi import Cookie, Depends, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class Model(BaseModel):
    field1: int = Field(0)


class Model2(BaseModel):
    field2: int = Field(0)


for param in (Query, Header, Cookie):

    def dependency(field2: int = param(0)):
        return field2

    @app.get(f"/{param.__name__.lower()}-depends/")
    async def with_depends(model1: Model = param(), dependency=Depends(dependency)):
        return {"field1": model1.field1, "field2": dependency}

    @app.get(f"/{param.__name__.lower()}-argument/")
    async def with_model_and_argument(model1: Model = param(), field2: int = param(0)):
        return {"field1": model1.field1, "field2": field2}

    @app.get(f"/{param.__name__.lower()}-models/")
    async def with_models(model1: Model = param(), model2: Model2 = param()):
        return {"field1": model1.field1, "field2": model2.field2}

    @app.get(f"/{param.__name__.lower()}-arguments/")
    async def with_argument(field1: int = param(0), field2: int = param(0)):
        return {"field1": field1, "field2": field2}


client = TestClient(app)


@pytest.mark.parametrize(
    "path",
    ["/query-depends/", "/query-arguments/", "/query-argument/", "/query-models/"],
)
def test_query_depends(path):
    response = client.get(path, params={"field1": 0, "field2": 1})
    assert response.status_code == 200
    assert response.json() == {"field1": 0, "field2": 1}


@pytest.mark.parametrize(
    "path",
    ["/header-depends/", "/header-arguments/", "/header-argument/", "/header-models/"],
)
def test_header_depends(path):
    response = client.get(path, headers={"field1": "0", "field2": "1"})
    assert response.status_code == 200
    assert response.json() == {"field1": 0, "field2": 1}


@pytest.mark.parametrize(
    "path",
    ["/cookie-depends/", "/cookie-arguments/", "/cookie-argument/", "/cookie-models/"],
)
def test_cookie_depends(path):
    client.cookies = {"field1": "0", "field2": "1"}
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"field1": 0, "field2": 1}


@pytest.mark.parametrize(
    ("path", "in_"),
    [
        ("/query-depends/", "query"),
        ("/query-arguments/", "query"),
        ("/query-argument/", "query"),
        ("/query-models/", "query"),
        ("/header-depends/", "header"),
        ("/header-arguments/", "header"),
        ("/header-argument/", "header"),
        ("/header-models/", "header"),
        ("/cookie-depends/", "cookie"),
        ("/cookie-arguments/", "cookie"),
        ("/cookie-argument/", "cookie"),
        ("/cookie-models/", "cookie"),
    ],
)
def test_parameters_openapi_schema(path, in_):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"][path]["get"]["parameters"] == [
        {
            "name": "field1",
            "in": in_,
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field1"},
        },
        {
            "name": "field2",
            "in": in_,
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field2"},
        },
    ]
