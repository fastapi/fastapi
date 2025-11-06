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
        "string_mapping": {"foo": "baz"},
        "mapping_query_int": {},
        "sequence_mapping_queries": {},
    }
