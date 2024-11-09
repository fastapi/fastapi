from fastapi.testclient import TestClient

from docs_src.dependencies.tutorial008b_an import app

client = TestClient(app)


def test_get_no_item():
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found"}


def test_owner_error():
    response = client.get("/items/plumbus")
    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Owner error: Rick"}


def test_get_item():
    response = client.get("/items/portal-gun")
    assert response.status_code == 200, response.text
    assert response.json() == {"description": "Gun to create portals", "owner": "Rick"}
