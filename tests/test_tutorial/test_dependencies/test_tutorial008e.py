from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial008e import app

client = TestClient(app)


def test_get_no_item():
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found"}
    assert "X-Username" not in response.headers


def test_get():
    response = client.get("/items/plumbus")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "description": "Freshly pickled plumbus",
        "owner": "Morty",
    }
    assert response.headers["X-Username"] == "Morty"
