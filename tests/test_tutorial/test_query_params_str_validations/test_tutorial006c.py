import importlib

import pytest
from fastapi.testclient import TestClient

from tests.utils import needs_pydanticv2

from ...utils import needs_py39, needs_py310


@pytest.fixture(
    name="client",
    params=[
        "tutorial006c_an",
        pytest.param("tutorial006c_an_py310", marks=needs_py310),
        pytest.param("tutorial006c_an_py39", marks=needs_py39),
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(
        f"docs_src.query_params_str_validations.{request.param}"
    )
    yield TestClient(mod.app)


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
