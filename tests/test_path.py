import pytest
from starlette.testclient import TestClient

from .main import app

client = TestClient(app)


def test_text_get():
    response = client.get("/text")
    assert response.status_code == 200
    assert response.json() == "Hello World"


def test_nonexistent():
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


response_not_valid_int = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}

response_not_valid_float = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "value is not a valid float",
            "type": "type_error.float",
        }
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/path/foobar", 200, "foobar"),
        ("/path/str/foobar", 200, "foobar"),
        ("/path/str/42", 200, "42"),
        ("/path/str/True", 200, "True"),
        ("/path/int/foobar", 422, response_not_valid_int),
        ("/path/int/True", 422, response_not_valid_int),
        ("/path/int/42", 200, 42),
        ("/path/int/42.5", 422, response_not_valid_int),
        ("/path/float/foobar", 422, response_not_valid_float),
        ("/path/float/True", 422, response_not_valid_float),
        ("/path/float/42", 200, 42),
        ("/path/float/42.5", 200, 42.5),
        ("/path/bool/foobar", 200, False),
        ("/path/bool/True", 200, True),
        ("/path/bool/42", 200, False),
        ("/path/bool/42.5", 200, False),
        ("/path/bool/1", 200, True),
        ("/path/bool/0", 200, False),
        ("/path/bool/true", 200, True),
        ("/path/bool/False", 200, False),
        ("/path/bool/false", 200, False),
        ("/path/param/foo", 200, "foo"),
        ("/path/param-required/foo", 200, "foo"),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
