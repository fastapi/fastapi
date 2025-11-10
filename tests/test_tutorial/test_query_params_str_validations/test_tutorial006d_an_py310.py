import pytest
from fastapi.testclient import TestClient
from tests.utils import needs_pydanticv2

@pytest.fixture
def client():
    from docs_src.query_params_str_validations.tutorial006d_an_py310 import app
    yield TestClient(app)


@needs_pydanticv2
@pytest.mark.parametrize(
    "q_value,expected",
    [
        ("None", None),
        ("", None),
        ("null", None),
        ("hello", "hello"),
    ],
)
def test_read_items(q_value, expected, client: TestClient):
    response = client.get("/items/", params={"q": q_value})
    assert response.status_code == 200
    assert response.json() == {"q": expected}
