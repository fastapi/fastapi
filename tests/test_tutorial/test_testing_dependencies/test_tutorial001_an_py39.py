from ...utils import needs_py39


@needs_py39
def test_override_in_items_run():
    from docs_src.dependency_testing.tutorial001_an_py39 import test_override_in_items

    test_override_in_items()


@needs_py39
def test_override_in_items_with_q_run():
    from docs_src.dependency_testing.tutorial001_an_py39 import (
        test_override_in_items_with_q,
    )

    test_override_in_items_with_q()


@needs_py39
def test_override_in_items_with_params_run():
    from docs_src.dependency_testing.tutorial001_an_py39 import (
        test_override_in_items_with_params,
    )

    test_override_in_items_with_params()


@needs_py39
def test_override_in_users():
    from docs_src.dependency_testing.tutorial001_an_py39 import client

    response = client.get("/users/")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


@needs_py39
def test_override_in_users_with_q():
    from docs_src.dependency_testing.tutorial001_an_py39 import client

    response = client.get("/users/?q=foo")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


@needs_py39
def test_override_in_users_with_params():
    from docs_src.dependency_testing.tutorial001_an_py39 import client

    response = client.get("/users/?q=foo&skip=100&limit=200")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


@needs_py39
def test_normal_app():
    from docs_src.dependency_testing.tutorial001_an_py39 import app, client

    app.dependency_overrides = None
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 100, "limit": 200},
    }
