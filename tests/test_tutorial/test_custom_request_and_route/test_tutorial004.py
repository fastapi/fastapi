from fastapi.testclient import TestClient

from docs_src.custom_api_router.tutorial001 import app

client = TestClient(app)


def test_get_timed():
    response = client.get("/healthz")
    assert response.text == "OK"
    assert "X-Response-Time" in response.headers
    assert float(response.headers["X-Response-Time"]) >= 0


def test_route_class():
    response = client.post(
        "/model/create", json={"name": "test", "description": "test"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["route_name"] == "Global.Model.create-model"
    assert response_json["route_class"] == "TimedRoute"
    assert response_json["router_class"] == "AppRouter"


def test_route_name():
    response = client.post(
        "/model/Model001/item/create", json={"name": "test", "description": "test"}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["route_name"] == "Global.Model.Item.create-item"
    assert response_json["router_class"] == "AppRouter"
