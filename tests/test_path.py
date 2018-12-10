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

response_at_least_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value has at least 3 characters",
            "type": "value_error.any_str.min_length",
            "ctx": {"limit_value": 3},
        }
    ]
}


response_at_least_2 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value has at least 2 characters",
            "type": "value_error.any_str.min_length",
            "ctx": {"limit_value": 2},
        }
    ]
}


response_maximum_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value has at most 3 characters",
            "type": "value_error.any_str.max_length",
            "ctx": {"limit_value": 3},
        }
    ]
}


response_greater_than_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is greater than 3",
            "type": "value_error.number.not_gt",
            "ctx": {"limit_value": 3},
        }
    ]
}


response_greater_than_0 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is greater than 0",
            "type": "value_error.number.not_gt",
            "ctx": {"limit_value": 0},
        }
    ]
}


response_greater_than_1 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is greater than 1",
            "type": "value_error.number.not_gt",
            "ctx": {"limit_value": 1},
        }
    ]
}


response_greater_than_equal_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is greater than or equal to 3",
            "type": "value_error.number.not_ge",
            "ctx": {"limit_value": 3},
        }
    ]
}


response_less_than_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is less than 3",
            "type": "value_error.number.not_lt",
            "ctx": {"limit_value": 3},
        }
    ]
}


response_less_than_0 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is less than 0",
            "type": "value_error.number.not_lt",
            "ctx": {"limit_value": 0},
        }
    ]
}


response_less_than_equal_3 = {
    "detail": [
        {
            "loc": ["path", "item_id"],
            "msg": "ensure this value is less than or equal to 3",
            "type": "value_error.number.not_le",
            "ctx": {"limit_value": 3},
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
        ("/path/param-minlength/foo", 200, "foo"),
        ("/path/param-minlength/fo", 422, response_at_least_3),
        ("/path/param-maxlength/foo", 200, "foo"),
        ("/path/param-maxlength/foobar", 422, response_maximum_3),
        ("/path/param-min_maxlength/foo", 200, "foo"),
        ("/path/param-min_maxlength/foobar", 422, response_maximum_3),
        ("/path/param-min_maxlength/f", 422, response_at_least_2),
        ("/path/param-gt/42", 200, 42),
        ("/path/param-gt/2", 422, response_greater_than_3),
        ("/path/param-gt0/0.05", 200, 0.05),
        ("/path/param-gt0/0", 422, response_greater_than_0),
        ("/path/param-ge/42", 200, 42),
        ("/path/param-ge/3", 200, 3),
        ("/path/param-ge/2", 422, response_greater_than_equal_3),
        ("/path/param-lt/42", 422, response_less_than_3),
        ("/path/param-lt/2", 200, 2),
        ("/path/param-lt0/-1", 200, -1),
        ("/path/param-lt0/0", 422, response_less_than_0),
        ("/path/param-le/42", 422, response_less_than_equal_3),
        ("/path/param-le/3", 200, 3),
        ("/path/param-le/2", 200, 2),
        ("/path/param-lt-gt/2", 200, 2),
        ("/path/param-lt-gt/4", 422, response_less_than_3),
        ("/path/param-lt-gt/0", 422, response_greater_than_1),
        ("/path/param-le-ge/2", 200, 2),
        ("/path/param-le-ge/1", 200, 1),
        ("/path/param-le-ge/3", 200, 3),
        ("/path/param-le-ge/4", 422, response_less_than_equal_3),
        ("/path/param-lt-int/2", 200, 2),
        ("/path/param-lt-int/42", 422, response_less_than_3),
        ("/path/param-lt-int/2.7", 422, response_not_valid_int),
        ("/path/param-gt-int/42", 200, 42),
        ("/path/param-gt-int/2", 422, response_greater_than_3),
        ("/path/param-gt-int/2.7", 422, response_not_valid_int),
        ("/path/param-le-int/42", 422, response_less_than_equal_3),
        ("/path/param-le-int/3", 200, 3),
        ("/path/param-le-int/2", 200, 2),
        ("/path/param-le-int/2.7", 422, response_not_valid_int),
        ("/path/param-ge-int/42", 200, 42),
        ("/path/param-ge-int/3", 200, 3),
        ("/path/param-ge-int/2", 422, response_greater_than_equal_3),
        ("/path/param-ge-int/2.7", 422, response_not_valid_int),
        ("/path/param-lt-gt-int/2", 200, 2),
        ("/path/param-lt-gt-int/4", 422, response_less_than_3),
        ("/path/param-lt-gt-int/0", 422, response_greater_than_1),
        ("/path/param-lt-gt-int/2.7", 422, response_not_valid_int),
        ("/path/param-le-ge-int/2", 200, 2),
        ("/path/param-le-ge-int/1", 200, 1),
        ("/path/param-le-ge-int/3", 200, 3),
        ("/path/param-le-ge-int/4", 422, response_less_than_equal_3),
        ("/path/param-le-ge-int/2.7", 422, response_not_valid_int),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
