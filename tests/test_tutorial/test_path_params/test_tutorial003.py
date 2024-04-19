from fastapi.testclient import TestClient
from fastapi.routing import APIRoute

import docs_src.path_params.tutorial003 as t3

client = TestClient(t3.app)


def test_get_users():
    response = client.get("/users")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"user_id": "the current user"}


def test_routes_created():
    root1 = APIRoute(path='/users', endpoint=t3.read_user, methods=['GET'], name = "name='read_user")
    root2 = APIRoute(path='/users', endpoint=t3.read_user_me, methods=['GET'], name = "name='read_user_me'")
    assert (root1 in t3.app.router.routes) and (root2 in t3.app.router.routes)

