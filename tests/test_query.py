import pytest
from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

response_missing = {
    "detail": [
        {
            "loc": ["query", "query"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
}

response_not_valid_int = {
    "detail": [
        {
            "loc": ["query", "query"],
            "msg": "value is not a valid integer",
            "type": "type_error.integer",
        }
    ]
}


@pytest.mark.parametrize(
    "path,expected_status,expected_response",
    [
        ("/query", 422, response_missing),
        ("/query?query=baz", 200, "foo bar baz"),
        ("/query?not_declared=baz", 422, response_missing),
        ("/query/optional", 200, "foo bar"),
        ("/query/optional?query=baz", 200, "foo bar baz"),
        ("/query/optional?not_declared=baz", 200, "foo bar"),
        ("/query/int", 422, response_missing),
        ("/query/int?query=42", 200, "foo bar 42"),
        ("/query/int?query=42.5", 422, response_not_valid_int),
        ("/query/int?query=baz", 422, response_not_valid_int),
        ("/query/int?not_declared=baz", 422, response_missing),
        ("/query/int/optional", 200, "foo bar"),
        ("/query/int/optional?query=50", 200, "foo bar 50"),
        ("/query/int/optional?query=foo", 422, response_not_valid_int),
        ("/query/int/default", 200, "foo bar 10"),
        ("/query/int/default?query=50", 200, "foo bar 50"),
        ("/query/int/default?query=foo", 422, response_not_valid_int),
        ("/query/param", 200, "foo bar"),
        ("/query/param?query=50", 200, "foo bar 50"),
        ("/query/param-required", 422, response_missing),
        ("/query/param-required?query=50", 200, "foo bar 50"),
        ("/query/param-required/int", 422, response_missing),
        ("/query/param-required/int?query=50", 200, "foo bar 50"),
        ("/query/param-required/int?query=foo", 422, response_not_valid_int),
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
