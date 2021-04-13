from fastapi.testclient import TestClient

from docs_src.custom_request_and_route.tutorial004 import app

client = TestClient(app)


def test_router_class_get():
    response = client.get("/via-router-class")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}


def test_router_class_head():
    response = client.head("/via-router-class")
    assert response.status_code == 200
    assert not response.content


def test_included_router_get():
    response = client.get("/via-include")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to FastAPI!"}


def test_included_router_head():
    response = client.head("/via-include")
    assert response.status_code == 200
    assert not response.content
