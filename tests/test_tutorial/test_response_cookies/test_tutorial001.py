from starlette.testclient import TestClient

from response_cookies.tutorial001 import app

client = TestClient(app)


def test_path_operation():
    response = client.post("/cookie/")
    assert response.status_code == 200
    assert response.json() == {"message": "Come to the dark side, we have cookies"}
    assert response.cookies["fakesession"] == "fake-cookie-session-value"
