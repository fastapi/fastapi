import requests

from app.core import config
from app.tests.utils.item import create_random_item
from app.tests.utils.utils import get_server_api


def test_create_item(superuser_token_headers):
    server_api = get_server_api()
    data = {"title": "Foo", "description": "Fighters"}
    response = requests.post(
        f"{server_api}{config.API_V1_STR}/items/",
        headers=superuser_token_headers,
        json=data,
    )
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "owner_id" in content


def test_read_item(superuser_token_headers):
    item = create_random_item()
    server_api = get_server_api()
    response = requests.get(
        f"{server_api}{config.API_V1_STR}/items/{item.id}",
        headers=superuser_token_headers,
    )
    content = response.json()
    assert content["title"] == item.title
    assert content["description"] == item.description
    assert content["id"] == item.id
    assert content["owner_id"] == item.owner_id
