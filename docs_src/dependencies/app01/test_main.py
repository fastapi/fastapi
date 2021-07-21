from fastapi.testclient import TestClient

from . import config, main

client = TestClient(main.app)


def get_settings_override():
    return config.Settings(admin_email="testing_admin@example.com")


main.app.dependency_overrides[main.get_settings] = get_settings_override


def test_app():

    response = client.get("/info")
    data = response.json()
    assert data == {
        "app_name": "Awesome API",
        "admin_email": "testing_admin@example.com",
        "items_per_user": 50,
    }
