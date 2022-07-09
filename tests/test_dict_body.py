from typing import Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.post("/query")
def read_query(q: Dict):
    return q


client = TestClient(app)


def test_empty_list_invalid():
    response = client.post("/query", json=[])
    assert response.status_code == 422


def test_empty_list():
    response = client.post("/query", json=[])
    assert response.json() == []


def test_empty_list_does_not_mutate_to_dict():
    response = client.post("/query", json=[])
    assert response.json() != {}
