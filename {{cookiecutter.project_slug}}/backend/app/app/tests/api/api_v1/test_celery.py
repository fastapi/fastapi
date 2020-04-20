from typing import Dict

import requests

from app.core.config import settings
from app.tests.utils.utils import get_server_api


def test_celery_worker_test(superuser_token_headers: Dict[str, str]) -> None:
    server_api = get_server_api()
    data = {"msg": "test"}
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["msg"] == "Word received"
