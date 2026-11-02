import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial006_py310", "tutorial006_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")
    return TestClient(mod.app)


@pytest.mark.parametrize(
    "form,expected",
    [
        ({}, None),
        ({"kind": "person", "name": "Rick"}, {"kind": "person", "name": "Rick"}),
        (
            {"kind": "company", "company_name": "Acme"},
            {"kind": "company", "company_name": "Acme"},
        ),
    ],
)
def test_contact(client: TestClient, form, expected):
    response = client.post("/contacts/", data=form)
    assert response.status_code == 200, response.text
    assert response.json() == expected


@pytest.mark.parametrize(
    "kind,field", [("person", "name"), ("company", "company_name")]
)
def test_incomplete_contact(client: TestClient, kind, field):
    response = client.post("/contacts/", data={"kind": kind})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", kind, field]


@pytest.mark.parametrize(
    "form,error_type",
    [
        ({"name": "Rick"}, "union_tag_not_found"),
        ({"kind": "unknown"}, "union_tag_invalid"),
    ],
)
def test_invalid_contact_kind(client: TestClient, form, error_type):
    response = client.post("/contacts/", data=form)
    assert response.status_code == 422
    assert response.json()["detail"][0]["type"] == error_type
