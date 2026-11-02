import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client", params=["tutorial007_py310", "tutorial007_an_py310"])
def get_client(request: pytest.FixtureRequest):
    mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")
    return TestClient(mod.app)


@pytest.mark.parametrize(
    "contact",
    [
        {"contact_type": "person", "name": "Rick"},
        {"contact_type": "company", "company_name": "Acme"},
    ],
)
@pytest.mark.parametrize(
    "notification",
    [
        {},
        {"notification_type": "email", "email": "rick@example.com"},
        {"notification_type": "sms", "phone": "+123456789"},
    ],
)
def test_contact(client: TestClient, contact, notification):
    response = client.post(
        "/contacts/", data={**contact, **notification, "token": "secret"}
    )
    assert response.status_code == 200, response.text
    assert response.json() == {
        "contact": contact,
        "notification": notification or None,
        "token": "secret",
    }


@pytest.mark.parametrize(
    "fields,location",
    [
        ({"token": "secret"}, ["body"]),
        ({"token": "secret", "contact_type": "person"}, ["body", "person", "name"]),
        (
            {
                "token": "secret",
                "contact_type": "person",
                "name": "Rick",
                "notification_type": "sms",
            },
            ["body", "sms", "phone"],
        ),
    ],
)
def test_missing_fields(client: TestClient, fields, location):
    response = client.post("/contacts/", data=fields)
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == location
