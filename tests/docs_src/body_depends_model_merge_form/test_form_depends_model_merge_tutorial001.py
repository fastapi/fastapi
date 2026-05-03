import pytest
from fastapi import status

from tests.docs_src._loader import docs_src_test_client


@pytest.fixture(scope="module")
def client():
    return docs_src_test_client(
        "docs_src_body_depends_model_merge_form_tutorial001",
        "body_depends_model_merge_form",
        "tutorial001_an_py310.py",
    )


@pytest.mark.parametrize(
    ("path", "form_data"),
    [
        pytest.param(
            "/auth/session/password/",
            {"username": "alice", "password": "secret"},
            id="password",
        ),
        pytest.param(
            "/auth/session/token/",
            {"username": "bob", "token": "tok-123"},
            id="token",
        ),
    ],
)
def test_form_depends_model_merge(client, path, form_data):
    response = client.post(path, data=form_data)
    assert response.status_code == status.HTTP_200_OK, response.text
    assert response.json() == form_data
