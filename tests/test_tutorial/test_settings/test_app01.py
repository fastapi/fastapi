import importlib
import sys

import pytest
from dirty_equals import IsAnyStr
from fastapi.testclient import TestClient
from pydantic import ValidationError
from pytest import MonkeyPatch


@pytest.fixture(
    name="mod_name",
    params=[
        pytest.param("app01_py39"),
    ],
)
def get_mod_name(request: pytest.FixtureRequest):
    return f"docs_src.settings.{request.param}.main"


@pytest.fixture(name="client")
def get_test_client(mod_name: str, monkeypatch: MonkeyPatch) -> TestClient:
    if mod_name in sys.modules:
        del sys.modules[mod_name]
    monkeypatch.setenv("ADMIN_EMAIL", "admin@example.com")
    main_mod = importlib.import_module(mod_name)
    return TestClient(main_mod.app)


def test_settings_validation_error(mod_name: str, monkeypatch: MonkeyPatch):
    monkeypatch.delenv("ADMIN_EMAIL", raising=False)
    if mod_name in sys.modules:
        del sys.modules[mod_name]  # pragma: no cover

    with pytest.raises(ValidationError) as exc_info:
        importlib.import_module(mod_name)
    assert exc_info.value.errors() == [
        {
            "loc": ("admin_email",),
            "msg": "Field required",
            "type": "missing",
            "input": {},
            "url": IsAnyStr,
        }
    ]


def test_app(client: TestClient):
    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "admin@example.com",
        "items_per_user": 50,
    }


def test_openapi_schema(client: TestClient):
    response = client.get("/openapi.json")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "openapi": "3.1.0",
        "info": {"title": "FastAPI", "version": "0.1.0"},
        "paths": {
            "/info": {
                "get": {
                    "operationId": "info_info_get",
                    "responses": {
                        "200": {
                            "description": "Successful Response",
                            "content": {"application/json": {"schema": {}}},
                        }
                    },
                    "summary": "Info",
                }
            }
        },
    }
