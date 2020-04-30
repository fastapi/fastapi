from dependency_testing.tutorial001 import (
    app,
    client,
    test_override_in_items,
    test_override_in_items_with_params,
    test_override_in_items_with_q,
)


def test_override_in_items_run():
    test_override_in_items()


def test_override_in_items_with_q_run():
    test_override_in_items_with_q()


def test_override_in_items_with_params_run():
    test_override_in_items_with_params()


def test_override_in_users():
    response = client.get("/users/")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": None, "skip": 5, "limit": 10},
    }


def test_override_in_users_with_q():
    response = client.get("/users/?q=foo")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_override_in_users_with_params():
    response = client.get("/users/?q=foo&skip=100&limit=200")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Users!",
        "params": {"q": "foo", "skip": 5, "limit": 10},
    }


def test_normal_app():
    app.dependency_overrides = None
    response = client.get("/items/?q=foo&skip=100&limit=200")
    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Hello Items!",
        "params": {"q": "foo", "skip": 100, "limit": 200},
    }
