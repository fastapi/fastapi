import pytest
from httpx import ASGITransport, AsyncClient

from .main import app, lifespan


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        async with lifespan(app=app):
            # Send a GET request to the root endpoint
            response = await client.get("/")
            # Verify that the response is successful
            assert response.status_code == 200
            # Verify that the app's state is initialized
            assert response.json() == {"message": "some_state_open"}

    # Verify that the app's state is cleaned up
    assert app.state.some_state == "some_state_close"
