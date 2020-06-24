import pytest

from httpx import AsyncClient

import main


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=main.app, base_url='http://test') as ac:
        response = await ac.get('/')
    assert response.status_code == 200
    assert response.json() == {'message': 'tomato'}
