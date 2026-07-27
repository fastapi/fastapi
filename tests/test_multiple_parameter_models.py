import pytest
from fastapi import Cookie, Depends, FastAPI, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, ConfigDict, Field

app = FastAPI()


class Model(BaseModel):
    field_1: int = Field(0)


class Model2(BaseModel):
    field_2: int = Field(0)


class ModelNoExtra(BaseModel):
    field_1: int = Field(0)
    model_config = ConfigDict(extra="forbid")


def HeaderU(*args, **kwargs):
    """Header callable that ensures that convert_underscores is False."""
    return Header(*args, convert_underscores=False, **kwargs)


for param in (Query, Header, HeaderU, Cookie):
    # Generates 4 views for all three Query, Header, and Cookie params:
    # i.e. /query-depends/, /query-arguments/, /query-argument/, /query-models/ for query

    def dependency(field_2: int = param(0, title="Field 2")):
        return field_2

    @app.get(f"/{param.__name__.lower()}-depends/")
    async def with_depends(model1: Model = param(), dependency=Depends(dependency)):
        """Model1 is specified via Query()/Header()/Cookie() and Model2 through Depends"""
        return {"field_1": model1.field_1, "field_2": dependency}

    @app.get(f"/{param.__name__.lower()}-arguments/")
    async def with_argument(
        field_1: int = param(0, title="Field 1"),
        field_2: int = param(0, title="Field 2"),
    ):
        """Model1 and Model2 are specified as direct arguments (sanity check)"""
        return {"field_1": field_1, "field_2": field_2}

    @app.get(f"/{param.__name__.lower()}-argument/")
    async def with_model_and_argument(
        model1: Model = param(), field_2: int = param(0, title="Field 2")
    ):
        """Model1 is specified via Query()/Header()/Cookie() and Model2 as direct argument"""
        return {"field_1": model1.field_1, "field_2": field_2}

    @app.get(f"/{param.__name__.lower()}-models/")
    async def with_models(model1: Model = param(), model2: Model2 = param()):
        """Model1 and Model2 are specified via Query()/Header()/Cookie()"""
        return {"field_1": model1.field_1, "field_2": model2.field_2}


@app.get("/mixed/")
async def mixed_model_sources(model1: Model = Query(), model2: Model2 = Header()):
    """Model1 is specified as Query(), Model2 as Header()"""
    return {"field_1": model1.field_1, "field_2": model2.field_2}


@app.get("/duplicate/")
async def duplicate_name(model: Model = Query(), same_model: Model = Query()):
    """Model1 is specified twice in Query()"""
    return {"field_1": model.field_1, "duplicate": same_model.field_1}


@app.get("/duplicate2/")
async def duplicate_name2(model: Model = Query(), same_model: Model = Header()):
    """Model1 is specified twice, once in Query(), once in Header()"""
    return {"field_1": model.field_1, "duplicate": same_model.field_1}


@app.get("/duplicate-no-extra/")
async def duplicate_name_no_extra(
    model: Model = Query(), same_model: ModelNoExtra = Query()
):
    """Uses Model and ModelNoExtra, but they have overlapping names"""
    return {"field_1": model.field_1, "duplicate": same_model.field_1}


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
    response = client.get(path, params={"field_1": 0, "field_2": 1})
    assert response.status_code == 200
    assert response.json() == {"field_1": 0, "field_2": 1}


@pytest.mark.parametrize(
    "path",
    ["/header-depends/", "/header-arguments/", "/header-argument/", "/header-models/"],
)
def test_header_depends(path):
    response = client.get(path, headers={"field-1": "0", "field-2": "1"})
    assert response.status_code == 200
    assert response.json() == {"field_1": 0, "field_2": 1}


@pytest.mark.parametrize(
    "path",
    [
        "/headeru-depends/",
        "/headeru-arguments/",
        "/headeru-argument/",
        "/headeru-models/",
    ],
)
def test_headeru_depends(path):
    response = client.get(path, headers={"field_1": "0", "field_2": "1"})
    assert response.status_code == 200
    assert response.json() == {"field_1": 0, "field_2": 1}


@pytest.mark.parametrize(
    "path",
    ["/cookie-depends/", "/cookie-arguments/", "/cookie-argument/", "/cookie-models/"],
)
def test_cookie_depends(path):
    client.cookies = {"field_1": "0", "field_2": "1"}
    response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {"field_1": 0, "field_2": 1}


def test_mixed():
    response = client.get("/mixed/", params={"field_1": 0}, headers={"field-2": "1"})
    assert response.status_code == 200
    assert response.json() == {"field_1": 0, "field_2": 1}


@pytest.mark.parametrize(
    "path",
    ["/duplicate/", "/duplicate2/", "/duplicate-no-extra/"],
)
def test_duplicate_name(path):
    response = client.get(path, params={"field_1": 0})
    assert response.status_code == 200
    assert response.json() == {"field_1": 0, "duplicate": 0}


def test_no_extra():
    response = client.get("/no-extra/", params={"field_1": 0, "field_2": 1})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "input": "1",
                "loc": ["query", "field_2"],
                "msg": "Extra inputs are not permitted",
                "type": "extra_forbidden",
            }
        ]
    }


@pytest.mark.parametrize(
    ("path", "in_", "convert_underscores"),
    [
        ("/query-depends/", "query", False),
        ("/query-arguments/", "query", False),
        ("/query-argument/", "query", False),
        ("/query-models/", "query", False),
        ("/header-depends/", "header", True),
        ("/header-arguments/", "header", True),
        ("/header-argument/", "header", True),
        ("/header-models/", "header", True),
        ("/headeru-depends/", "header", False),
        ("/headeru-arguments/", "header", False),
        ("/headeru-argument/", "header", False),
        ("/headeru-models/", "header", False),
        ("/cookie-depends/", "cookie", False),
        ("/cookie-arguments/", "cookie", False),
        ("/cookie-argument/", "cookie", False),
        ("/cookie-models/", "cookie", False),
    ],
)
def test_parameters_openapi_schema(path, in_, convert_underscores):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"][path]["get"]["parameters"] == [
        {
            "name": "field-1" if convert_underscores else "field_1",
            "in": in_,
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 1"},
        },
        {
            "name": "field-2" if convert_underscores else "field_2",
            "in": in_,
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 2"},
        },
    ]


def test_parameters_openapi_mixed():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/mixed/"]["get"]["parameters"] == [
        {
            "name": "field_1",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 1"},
        },
        {
            "name": "field-2",
            "in": "header",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 2"},
        },
    ]


def test_parameters_openapi_duplicate_name():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/duplicate/"]["get"]["parameters"] == [
        {
            "name": "field_1",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 1"},
        },
    ]


def test_parameters_openapi_duplicate_name2():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json()["paths"]["/duplicate2/"]["get"]["parameters"] == [
        {
            "name": "field_1",
            "in": "query",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 1"},
        },
        {
            "name": "field-1",
            "in": "header",
            "required": False,
            "schema": {"type": "integer", "default": 0, "title": "Field 1"},
        },
    ]
