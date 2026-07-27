import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(
    name="client",
    params=[
        "tutorial001_py310",
    ],
)
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.strict_content_type.{request.param}")
    client = TestClient(mod.app)
    return client


def test_lax_post_without_content_type_is_parsed_as_json(client: TestClient):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo", "price": 50.5}


def test_lax_post_with_json_content_type(client: TestClient):
    response = client.post(
        "/items/",
        json={"name": "Foo", "price": 50.5},
    )
    assert response.status_code == 200, response.text
    assert response.json() == {"name": "Foo", "price": 50.5}


def test_lax_post_with_text_plain_is_still_rejected(client: TestClient):
    response = client.post(
        "/items/",
        content='{"name": "Foo", "price": 50.5}',
        headers={"Content-Type": "text/plain"},
    )
    assert response.status_code == 422, response.text
