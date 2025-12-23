import importlib
import warnings

import pytest
from fastapi.testclient import TestClient

from ...utils import needs_pydanticv1


@pytest.fixture(
    name="client",
    params=[
        "tutorial002_pv1_py39",
        "tutorial002_pv1_an_py39",
    ],
)
def get_client(request: pytest.FixtureRequest):
    with warnings.catch_warnings(record=True):
        warnings.filterwarnings(
            "ignore",
            message=r"pydantic\.v1 is deprecated and will soon stop being supported by FastAPI\..*",
            category=DeprecationWarning,
        )
        mod = importlib.import_module(f"docs_src.request_form_models.{request.param}")

    client = TestClient(mod.app)
    return client


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_post_body_form(client: TestClient):
    response = client.post("/login/", data={"username": "Foo", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"username": "Foo", "password": "secret"}


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_post_body_extra_form(client: TestClient):
    response = client.post(
        "/login/", data={"username": "Foo", "password": "secret", "extra": "extra"}
    )
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error.extra",
                "loc": ["body", "extra"],
                "msg": "extra fields not permitted",
            }
        ]
    }


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_post_body_form_no_password(client: TestClient):
    response = client.post("/login/", data={"username": "Foo"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error.missing",
                "loc": ["body", "password"],
                "msg": "field required",
            }
        ]
    }


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_post_body_form_no_username(client: TestClient):
    response = client.post("/login/", data={"password": "secret"})
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error.missing",
                "loc": ["body", "username"],
                "msg": "field required",
            }
        ]
    }


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_post_body_form_no_data(client: TestClient):
    response = client.post("/login/")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "type": "value_error.missing",
                "loc": ["body", "username"],
                "msg": "field required",
            },
            {
                "type": "value_error.missing",
                "loc": ["body", "password"],
                "msg": "field required",
            },
        ]
    }


# TODO: remove when deprecating Pydantic v1
@needs_pydanticv1
def test_post_body_json(client: TestClient):
    response = client.post("/login/", json={"username": "Foo", "password": "secret"})
    assert response.status_code == 422, response.text
    assert response.json() == {
        "detail": [
            {
                "type": "value_error.missing",
                "loc": ["body", "username"],
                "msg": "field required",
            },
            {
                "type": "value_error.missing",
                "loc": ["body", "password"],
                "msg": "field required",
            },
        ]
    }
