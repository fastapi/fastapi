import requests

from app.core import config
from app.tests.utils.utils import get_server_api


def test_celery_worker_test(superuser_token_headers):
    server_api = get_server_api()
    data = {"msg": "test"}
    r = requests.post(
        f"{server_api}{config.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
