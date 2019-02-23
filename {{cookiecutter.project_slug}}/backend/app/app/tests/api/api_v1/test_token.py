import requests

from app.core import config
from app.tests.utils.utils import get_server_api


def test_get_access_token():
    server_api = get_server_api()
    login_data = {
        "username": config.FIRST_SUPERUSER,
        "password": config.FIRST_SUPERUSER_PASSWORD,
    }
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_use_access_token(superuser_token_headers):
    server_api = get_server_api()
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/login/test-token",
        headers=superuser_token_headers,
    )
    result = r.json()
    assert r.status_code == 200
    assert "email" in result
