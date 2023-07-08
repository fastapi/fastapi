import pytest
from dirty_equals import IsDict
from fastapi.testclient import TestClient
from fastapi.utils import match_pydantic_error_url


@pytest.fixture(name="client")
def get_client():
    from docs_src.query_params.tutorial006 import app

    c = TestClient(app)
    return c


def test_foo_needy_very(client: TestClient):
    response = client.get("/items/foo?needy=very")
    assert response.status_code == 200
    assert response.json() == {
        "query": 1,
        "string_mapping": {
            "query": "1",
            "foo": "baz"
        },
        "mapping_query_int": {
            "query": 1
        },
        "sequence_mapping_queries": {
            "query": [
            "1"
            ],
            "foo": []
        }
    }