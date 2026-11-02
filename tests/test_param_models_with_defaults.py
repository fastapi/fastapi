from typing import Annotated

from fastapi import FastAPI, Form, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Filters(BaseModel):
    start: int
    limit: int = 10


class Prefs(BaseModel):
    theme: str
    items: list[str] = []


def test_query_model_with_default_instance_uses_default_when_omitted():
    app = FastAPI()

    @app.get("/")
    def read(filters: Annotated[Filters, Query()] = Filters(start=1)):
        return filters

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 1, "limit": 10}


def test_query_model_with_default_instance_uses_sent_data():
    app = FastAPI()

    @app.get("/")
    def read(filters: Annotated[Filters, Query()] = Filters(start=1)):
        return filters

    client = TestClient(app)
    response = client.get("/?start=5")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 5, "limit": 10}


def test_query_model_with_default_instance_partial_data_still_errors():
    app = FastAPI()

    @app.get("/")
    def read(filters: Annotated[Filters, Query()] = Filters(start=1)):
        return filters

    client = TestClient(app)
    response = client.get("/?limit=3")
    assert response.status_code == 422, response.text
    errors = response.json()["detail"]
    assert errors[0]["loc"] == ["query", "start"]
    assert errors[0]["type"] == "missing"


def test_required_query_model_without_default_still_errors():
    app = FastAPI()

    @app.get("/")
    def read(filters: Annotated[Filters, Query()]):
        return filters

    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 422, response.text
    errors = response.json()["detail"]
    assert errors[0]["loc"] == ["query", "start"]
    assert errors[0]["type"] == "missing"
    response = client.get("/?start=2")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 2, "limit": 10}


def test_form_model_with_default_instance_uses_default_when_omitted():
    app = FastAPI()

    @app.post("/prefs")
    def update_prefs(prefs: Annotated[Prefs, Form()] = Prefs(theme="dark")):
        return prefs

    client = TestClient(app)
    response = client.post("/prefs", data={})
    assert response.status_code == 200, response.text
    assert response.json() == {"theme": "dark", "items": []}
    response = client.post("/prefs", data={"theme": "light"})
    assert response.status_code == 200, response.text
    assert response.json() == {"theme": "light", "items": []}


def test_required_form_model_without_default_still_errors():
    app = FastAPI()

    class Creds(BaseModel):
        user: str
        pw: str

    @app.post("/login")
    def login(creds: Annotated[Creds, Form()]):
        return creds

    client = TestClient(app)
    response = client.post("/login", data={})
    assert response.status_code == 422, response.text
    errors = response.json()["detail"]
    assert [error["loc"] for error in errors] == [
        ["body", "user"],
        ["body", "pw"],
    ]


def test_openapi_default_instance_model_fields_are_not_required():
    app = FastAPI()

    @app.get("/")
    def read(filters: Annotated[Filters, Query()] = Filters(start=1)):
        return filters

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    parameters = schema["paths"]["/"]["get"]["parameters"]
    assert [(param["name"], param["required"]) for param in parameters] == [
        ("start", False),
        ("limit", False),
    ]


def test_openapi_required_model_fields_stay_required():
    app = FastAPI()

    @app.get("/")
    def read(filters: Annotated[Filters, Query()]):
        return filters

    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    schema = response.json()
    parameters = schema["paths"]["/"]["get"]["parameters"]
    assert [(param["name"], param["required"]) for param in parameters] == [
        ("start", True),
        ("limit", False),
    ]
