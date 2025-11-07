import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client")
def get_client():
    from docs_src.query_params.tutorial007_py310 import app

    c = TestClient(app)
    return c


def test_foo_needy_very(client: TestClient):
    response = client.get("/query/mixed-type-params?query=1&query=2&foo=bar&foo=baz")
    assert response.status_code == 200
    assert response.json() == {
        "query": 2,
        "mapping_query_str_or_int": {"foo": "baz"},
        "mapping_query_int": None,
        "sequence_mapping_int": None,
    }


def test_just_string_not_scalar_mapping(client: TestClient):
    response = client.get("/query/mixed-type-params?&query=2&foo=1&bar=3&foo=2&foo=baz")
    assert response.status_code == 200
    assert response.json() == {
        "query": 2,
        "mapping_query_str_or_int": {"bar": "3", "foo": "baz"},
        "mapping_query_int": {"bar": 3},
        "sequence_mapping_int": {"bar": [3], "foo": [1, 2]},
    }
