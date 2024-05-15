from typing import Optional

from fastapi import FastAPI
from fastapi.params import Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
def get(
    x: Optional[float] = Query(default=0, allow_inf_nan=False),
    y: Optional[float] = Query(default=0, allow_inf_nan=True),
    z: Optional[float] = Query(default=0),
) -> str:  # type: ignore
    return "OK"


client = TestClient(app)


def test_allow_inf_nan_false():
    response = client.get("/?x=inf")
    assert response.status_code == 422, response.text

    response = client.get("/?x=-inf")
    assert response.status_code == 422, response.text

    response = client.get("/?x=nan")
    assert response.status_code == 422, response.text

    response = client.get("/?x=0")
    assert response.status_code == 200, response.text


def test_allow_inf_nan_true():
    response = client.get("/?y=inf")
    assert response.status_code == 200, response.text

    response = client.get("/?y=-inf")
    assert response.status_code == 200, response.text

    response = client.get("/?y=nan")
    assert response.status_code == 200, response.text

    response = client.get("/?y=0")
    assert response.status_code == 200, response.text


def test_allow_inf_nan_not_specified():
    response = client.get("/?z=inf")
    assert response.status_code == 200, response.text

    response = client.get("/?z=-inf")
    assert response.status_code == 200, response.text

    response = client.get("/?z=nan")
    assert response.status_code == 200, response.text

    response = client.get("/?z=0")
    assert response.status_code == 200, response.text
