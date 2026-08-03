import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

from .main import app, items


@pytest.mark.anyio
async def test_root():
    assert items == {}

    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}
    assert items == {}
