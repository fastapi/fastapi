from fastapi.testclient import TestClient

from docs_src.extending_openapi.tutorial006 import app

client = TestClient(app)


def test_swagger_ui():
    response = client.get("/elements")
    assert response.status_code == 200, response.text
    assert 'router="history"' in response.text
    assert 'layout="sidebar"' in response.text
    assert 'tryItCredentialPolicy="omit"' in response.text
    

def test_get_users():
    response = client.get("/users/foo")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello foo"}


