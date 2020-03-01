from fastapi.testclient import TestClient

from path_operation_advanced_configuration.tutorial003 import app

client = TestClient(app)

openapi_schema = {
    "openapi": "3.0.2",
    "info": {"title": "FastAPI", "version": "0.1.0"},
    "paths": {},
}


def test_openapi_schema():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.json() == openapi_schema


def test_get():
    response = client.get("/items/")
    assert response.status_code == 200
    assert response.json() == [{"item_id": "Foo"}]
