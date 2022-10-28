"""Test case for possible tag duplication at OpenAPI object level"""

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI(
    openapi_tags=[
        {"name": "items", "description": "items1"},
        {"name": "items", "description": "items2"},
    ]
)

client = TestClient(app)


def test_openapi_for_duplicates():
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    tag_list = response.json()["tags"]
    assert len(tag_list) == 1
    assert tag_list[0]["name"] == "items"
    assert tag_list[0]["description"] == "items1"
