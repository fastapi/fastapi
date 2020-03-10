from fastapi.testclient import TestClient

from custom_request_and_route.tutorial002 import app

client = TestClient(app)


def test_endpoint_works():
    response = client.post("/", json=[1, 2, 3])
    assert response.json() == 6


def test_exception_handler_body_access():
    response = client.post("/", json={"numbers": [1, 2, 3]})

    assert response.json() == {
        "detail": {
            "body": '{"numbers": [1, 2, 3]}',
            "errors": [
                {
                    "loc": ["body", "numbers"],
                    "msg": "value is not a valid list",
                    "type": "type_error.list",
                }
            ],
        }
    }
