import random
import string

import requests

from app.core.config import settings


def random_lower_string():
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email():
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_server_api():
    server_name = f"http://{settings.SERVER_NAME}"
    return server_name


def get_superuser_token_headers():
    server_api = get_server_api()
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = requests.post(
        f"{server_api}{settings.API_V1_STR}/login/access-token", data=login_data
    )
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    # superuser_token_headers = headers
    return headers
