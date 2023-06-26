from typing import Union

from fastapi import Body, FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/query")
def read_query(q: Union[str, None]):
    return q


@app.get("/explicit-query")
def read_explicit_query(q: Union[str, None] = Query()):
    return q


@app.post("/body-embed")
def send_body_embed(b: Union[str, None] = Body(embed=True)):
    return b


client = TestClient(app)


def test_required_nonable_query_invalid():
    response = client.get("/query")
    assert response.status_code == 422


def test_required_noneable_query_value():
    response = client.get("/query", params={"q": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_required_nonable_explicit_query_invalid():
    response = client.get("/explicit-query")
    assert response.status_code == 422


def test_required_nonable_explicit_query_value():
    response = client.get("/explicit-query", params={"q": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"


def test_required_nonable_body_embed_no_content():
    response = client.post("/body-embed")
    assert response.status_code == 422


def test_required_nonable_body_embed_invalid():
    response = client.post("/body-embed", json={"invalid": "invalid"})
    assert response.status_code == 422


def test_required_noneable_body_embed_value():
    response = client.post("/body-embed", json={"b": "foo"})
    assert response.status_code == 200
    assert response.json() == "foo"
