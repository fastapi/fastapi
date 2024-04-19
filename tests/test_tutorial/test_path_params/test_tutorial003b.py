from fastapi.routing import APIRoute
from fastapi.testclient import TestClient

import docs_src.path_params.tutorial003b as t3

client = TestClient(t3.app)


def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == ["Rick", "Morty"]


def test_routes_created():
    root1 = APIRoute(
        path="/users", endpoint=t3.read_users, methods=["GET"], name="read_users"
    )
    root2 = APIRoute(
        path="/users",
        endpoint=t3.read_users2,
        methods=["GET"],
        name="read_users2",
    )
    assert (root1 in t3.app.router.routes) and (root2 in t3.app.router.routes)
