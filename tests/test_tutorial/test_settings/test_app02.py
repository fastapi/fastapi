from fastapi.testclient import TestClient

from docs_src.settings.app02.main import app


def test_settings():
    client = TestClient(app)
    response = client.get("/info")
    assert response.json() == {
        "app_name": "Awesome API",
        "admin_email": "admin@example.com",
        "items_per_user": 50,
    }


def test_override_settings():
    from docs_src.settings.app02.test_main import test_app

    test_app()
