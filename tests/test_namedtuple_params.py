from typing import NamedTuple

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


class Point(NamedTuple):
    x: int
    y: int


@app.post("/namedtuple-body/")
def post_namedtuple_body(point: Point):
    return point


client = TestClient(app)


def test_namedtuple_body_is_json():
    response = client.post("/namedtuple-body/", json=[1, 2])
    assert response.status_code == 200, response.text
    assert response.json() == [1, 2]


def test_namedtuple_body_in_openapi_as_json():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    content = response.json()["paths"]["/namedtuple-body/"]["post"]["requestBody"][
        "content"
    ]
    assert "multipart/form-data" not in content
    assert "application/json" in content
