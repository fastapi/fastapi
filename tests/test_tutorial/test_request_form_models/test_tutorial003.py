import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        "tutorial003_py310",
        "tutorial003_an_py310",
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")

    client = TestClient(mod.app)
    return client


def test_get_form(client: TestClient):
    """The form has a checkbox that is by default checked"""
    response = client.get("/form")
    response.raise_for_status()
    assert '<input type="checkbox" name="checkbox"' in response.text
    assert 'checked="checked"' in response.text


def test_post_form_checked(client: TestClient):
    """When the checkbox is checked, the value is (correctly) True"""
    response = client.post("/form", data={"checkbox": "on"})
    response.raise_for_status()
    assert response.json() == {"checkbox": True}


@pytest.mark.parametrize("data", [{}, {"checkbox": ""}])
def test_post_form_unchecked(client: TestClient, data: dict):
    """
    When the checkbox is not checked,
    the value is (maybe correctly but undesirably) still True
    """
    response = client.post("/form", data=data)
    response.raise_for_status()
    assert response.json() == {"checkbox": True}
