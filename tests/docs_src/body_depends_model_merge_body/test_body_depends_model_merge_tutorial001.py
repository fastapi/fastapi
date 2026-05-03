import pytest
from fastapi import status

from tests.docs_src._loader import docs_src_test_client


@pytest.fixture(scope="module")
def client():
    return docs_src_test_client(
        "docs_src_body_depends_model_merge_body_tutorial001",
        "body_depends_model_merge_body",
        "tutorial001_an_py310.py",
    )


@pytest.mark.parametrize(
    ("path", "payload"),
    [
        pytest.param(
            "/items/objects/gadgets/",
            {"name": "G1", "description": "d1"},
            id="gadget",
        ),
        pytest.param(
            "/items/objects/parts/",
            {"name": "P1", "sku": "S1"},
            id="part",
        ),
    ],
)
def test_json_body_depends_model_merge(client, path, payload):
    response = client.post(path, json=payload)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == payload
