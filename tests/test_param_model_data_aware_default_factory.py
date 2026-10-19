from typing import Annotated

from fastapi import Cookie, FastAPI, Form, Header, Query
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class Filter(BaseModel):
    start: int = 5
    end: int = Field(default_factory=lambda data: data["start"] + 10)


@app.get("/query")
def get_query(filter_: Annotated[Filter, Query()]):
    return filter_


@app.get("/header")
def get_header(filter_: Annotated[Filter, Header()]):
    return filter_


@app.get("/cookie")
def get_cookie(filter_: Annotated[Filter, Cookie()]):
    return filter_


@app.post("/form")
def post_form(filter_: Annotated[Filter, Form()]):
    return filter_


@app.get("/standalone")
def get_standalone(q: int = Query(default_factory=lambda data: 42)):
    return {"q": q}


client = TestClient(app)


def test_query_param_model_data_aware_default():
    # When no query params are provided, default_factory uses default start=5 -> end=15
    response = client.get("/query")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 5, "end": 15}

    # When start is provided, default_factory uses provided start=20 -> end=30
    response = client.get("/query?start=20")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 20, "end": 30}

    # When both are provided, default_factory is not called
    response = client.get("/query?start=20&end=99")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 20, "end": 99}


def test_header_param_model_data_aware_default():
    response = client.get("/header")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 5, "end": 15}

    response = client.get("/header", headers={"start": "25"})
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 25, "end": 35}

    response = client.get("/header", headers={"start": "25", "end": "70"})
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 25, "end": 70}


def test_cookie_param_model_data_aware_default():
    response = client.get("/cookie")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 5, "end": 15}

    client_with_start = TestClient(app, cookies={"start": "30"})
    response = client_with_start.get("/cookie")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 30, "end": 40}

    client_with_both = TestClient(app, cookies={"start": "30", "end": "80"})
    response = client_with_both.get("/cookie")
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 30, "end": 80}


def test_form_param_model_data_aware_default():
    response = client.post("/form", data={})
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 5, "end": 15}

    response = client.post("/form", data={"start": "40"})
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 40, "end": 50}

    response = client.post("/form", data={"start": "40", "end": "100"})
    assert response.status_code == 200, response.text
    assert response.json() == {"start": 40, "end": 100}


def test_standalone_param_data_aware_default():
    response = client.get("/standalone")
    assert response.status_code == 200, response.text
    assert response.json() == {"q": 42}


def test_param_model_data_aware_default_validation_error():
    response = client.get("/query?start=invalid")
    assert response.status_code == 422, response.text
    errors = response.json()["detail"]
    assert any(err["loc"] == ["query", "start"] for err in errors)
