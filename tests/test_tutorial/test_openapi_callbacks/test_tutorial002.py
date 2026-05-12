from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from docs_src.openapi_callbacks.tutorial002_py310 import app

client = TestClient(app)


@patch("docs_src.openapi_callbacks.tutorial002_py310.httpx.AsyncClient.post")
def test_process_passage(mock_post):
    mock_post.return_value = AsyncMock()

    response = client.post(
        "/process-passage",
        json={
            "passage_topic": "FastAPI tutorial",
            "callback_url": "http://testserver/callback",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Passage processing started"}


def test_callback():
    response = client.post(
        "/callback",
        json={
            "processed_passage": "FastAPI tutorial",
            "status": "completed",
        },
    )

    assert response.status_code == 200
    assert response.json() == {"received": True}
