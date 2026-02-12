import importlib
from types import ModuleType

import pytest

from ...utils import needs_py310


@pytest.fixture(
    name="test_module",
    params=[
        pytest.param("tutorial001_py39"),
        pytest.param("tutorial001_py310", marks=needs_py310),
        pytest.param("tutorial001_an_py39"),
        pytest.param("tutorial001_an_py310", marks=needs_py310),
    ],
)
def get_test_module(request: pytest.FixtureRequest) -> ModuleType:
    mod: ModuleType = importlib.import_module(
        f"docs_src.dependency_testing.{request.param}"
    )
    return mod


def test_override_in_items_run(test_module: ModuleType):
    test_override_in_items = test_module.test_override_in_items

    test_override_in_items()


def test_override_in_items_with_q_run(test_module: ModuleType):
    test_override_in_items_with_q = test_module.test_override_in_items_with_q

    test_override_in_items_with_q()


def test_override_in_items_with_params_run(test_module: ModuleType):
    test_override_in_items_with_params = test_module.test_override_in_items_with_params

    test_override_in_items_with_params()


def test_override_in_users(test_module: ModuleType):
    client = test_module.client
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_users_with_q(test_module: ModuleType):
    client = test_module.client
    response = client.get("/users/?q=foo")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_users_with_params(test_module: ModuleType):
    client = test_module.client
    response = client.get("/users/?q=foo&skip=100&limit=200")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_normal_app(test_module: ModuleType):
    app = test_module.app
    client = test_module.client
    app.dependency_overrides = None
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 100, "limit": 200},
    }
