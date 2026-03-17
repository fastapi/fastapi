from fastapi import FastAPI
from fastapi.testclient import TestClient


from docs_src.path_params.tutorial006_py310 import app

client = TestClient(app)


def test_valid_item_id():
    response = client.get("/items/100")
    assert response.status_code == 200
    assert response.json() == {"item_id": 100}


def test_item_id_below_range():
    response = client.get("/items/0")
    assert response.status_code == 422  # validation error


def test_item_id_above_range():
    response = client.get("/items/1001")
    assert response.status_code == 422  # validation error


def test_invalid_type():
    response = client.get("/items/abc")
    assert response.status_code == 422  # type validation error
