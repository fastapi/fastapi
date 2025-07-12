import pytest
from fastapi import Cookie, Depends, FastAPI, Header, Query
from fastapi._compat import PYDANTIC_V2
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


class Model(BaseModel):
    field1: int = Field(0)


class Model2(BaseModel):
    field2: int = Field(0)


class ModelNoExtra(BaseModel):
    field1: int = Field(0)
    if PYDANTIC_V2:
        model_config = ConfigDict(extra="forbid")
    else:

        class Config:
            extra = "forbid"


for param in (Query, Header, Cookie):
    # Generates 4 views for all three Query, Header, and Cookie params:
    # i.e. /query-depends/, /query-arguments/, /query-argument/, /query-models/ for query

    def dependency(field2: int = param(0)):
        return field2

    @app.get(f"/{param.__name__.lower()}-depends/")
    async def with_depends(model1: Model = param(), dependency=Depends(dependency)):
        """Model1 is specified via Query()/Header()/Cookie() and Model2 through Depends"""
        return {"field1": model1.field1, "field2": dependency}

    @app.get(f"/{param.__name__.lower()}-argument/")
    async def with_model_and_argument(model1: Model = param(), field2: int = param(0)):
        """Model1 is specified via Query()/Header()/Cookie() and Model2 as direct argument"""
        return {"field1": model1.field1, "field2": field2}

    @app.get(f"/{param.__name__.lower()}-models/")
    async def with_models(model1: Model = param(), model2: Model2 = param()):
        """Model1 and Model2 are specified via Query()/Header()/Cookie()"""
        return {"field1": model1.field1, "field2": model2.field2}

    @app.get(f"/{param.__name__.lower()}-arguments/")
    async def with_argument(field1: int = param(0), field2: int = param(0)):
        """Model1 and Model2 are specified as direct arguments (sanity check)"""
        return {"field1": field1, "field2": field2}


@app.get("/mixed/")
async def mixed_model_sources(model1: Model = Query(), model2: Model2 = Header()):
    """Model1 is specified as Query(), Model2 as Header()"""
    return {"field1": model1.field1, "field2": model2.field2}


@app.get("/duplicate/")
async def duplicate_name(model: Model = Query(), same_model: Model = Query()):
    """Model1 is specified twice in Query()"""
    return {"field1": model.field1, "duplicate": same_model.field1}


@app.get("/duplicate2/")
async def duplicate_name2(model: Model = Query(), same_model: Model = Header()):
    """Model1 is specified twice, once in Query(), once in Header()"""
    return {"field1": model.field1, "duplicate": same_model.field1}


@app.get("/duplicate-no-extra/")
async def duplicate_name_no_extra(
    model: Model = Query(), same_model: ModelNoExtra = Query()
):
    """Uses Model and ModelNoExtra, but they have overlapping names"""
    return {"field1": model.field1, "duplicate": same_model.field1}


@app.get("/no-extra/")
async def no_extra(model1: ModelNoExtra = Query(), model2: Model2 = Query()):
    """Uses Model2 and ModelNoExtra, but they don't have overlapping names"""
    pass  # pragma: nocover


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


def test_mixed():
    response = client.get("/mixed/", params={"field1": 0}, headers={"field2": "1"})
    assert response.status_code == 200
    assert response.json() == {"field1": 0, "field2": 1}


@pytest.mark.parametrize(
    "path",
    ["/duplicate/", "/duplicate2/", "/duplicate-no-extra/"],
)
def test_duplicate_name(path):
    response = client.get(path, params={"field1": 0})
    assert response.status_code == 200
    assert response.json() == {"field1": 0, "duplicate": 0}


def test_no_extra():
    response = client.get("/no-extra/", params={"field1": 0, "field2": 1})
    assert response.status_code == 422
    if PYDANTIC_V2:
        assert response.json() == {
            "detail": [
                {
                    "input": "1",
                    "loc": ["query", "field2"],
                    "msg": "Extra inputs are not permitted",
                    "type": "extra_forbidden",
                }
            ]
        }
    else:
        assert response.json() == {
            "detail": [
                {
                    "loc": ["query", "field2"],
                    "msg": "extra fields not permitted",
                    "type": "value_error.extra",
                }
            ]
        }


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


def test_parameters_openapi_mixed():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/mixed/"]["get"]["parameters"] == [
        {
            "name": "field1",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field1"},
        },
        {
            "name": "field2",
            "in": "header",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field2"},
        },
    ]


def test_parameters_openapi_duplicate_name():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/duplicate/"]["get"]["parameters"] == [
        {
            "name": "field1",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field1"},
        },
    ]


def test_parameters_openapi_duplicate_name2():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/duplicate2/"]["get"]["parameters"] == [
        {
            "name": "field1",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field1"},
        },
        {
            "name": "field1",
            "in": "header",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field1"},
        },
    ]
