import pytest
from fastapi.testclient import TestClient


@pytest.fixture(name="client")
def get_client():
    from docs_src.dependencies.tutorial008d_an import app

    client = TestClient(app)
    return client


def test_get_no_item(client: TestClient):
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found, there's only a plumbus here"}


def test_get(client: TestClient):
    response = client.get("/items/plumbus")
    assert response.status_code == 200, response.text
    assert response.json() == "plumbus"


def test_internal_error(client: TestClient):
    from docs_src.dependencies.tutorial008d_an import InternalError

    with pytest.raises(InternalError) as exc_info:
        client.get("/items/portal-gun")
    assert (
        exc_info.value.args[0] == "The portal gun is too dangerous to be owned by Rick"
    )


def test_internal_server_error():
    from docs_src.dependencies.tutorial008d_an import app

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/items/portal-gun")
    assert response.status_code == 500, response.text
    assert response.text == "Internal Server Error"
