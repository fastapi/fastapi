import pytest
from starlette.testclient import TestClient

from .main import app

client = TestClient(app)

response_missing = {
    "detail": [
        {"loc": ["query"], "msg": "field required", "type": "value_error.missing"}
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
    ],
)
def test_get_path(path, expected_status, expected_response):
    response = client.get(path)
    assert response.status_code == expected_status
    assert response.json() == expected_response
