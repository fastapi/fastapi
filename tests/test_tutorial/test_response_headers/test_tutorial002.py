from fastapi.testclient import TestClient

from docs_src.response_headers.tutorial002 import app

client = TestClient(app)


def test_path_operation():
    response = client.get("/headers-and-object/")
    assert response.status_code == 200, response.text
    assert response.json() == {"message": "Hello World"}
    assert response.headers["X-Cat-Dog"] == "alone in the world"
