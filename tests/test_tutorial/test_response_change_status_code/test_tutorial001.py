from fastapi.testclient import TestClient

from response_change_status_code.tutorial001 import app

client = TestClient(app)


def test_path_operation():
    response = client.put("/get-or-create-task/foo")
    print(response.content)
    assert response.status_code == 200
    assert response.json() == "Listen to the Bar Fighters"
    response = client.put("/get-or-create-task/bar")
    assert response.status_code == 201
    assert response.json() == "This didn't exist before"
