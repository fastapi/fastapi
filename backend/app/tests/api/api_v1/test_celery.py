from fastapi.testclient import TestClient

from app.core.config import settings


def test_celery_worker_test(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"message": "test"}
    r = client.post(
        f"{settings.API_V1_STR}/utils/test-celery/",
        json=data,
        headers=superuser_token_headers,
    )
    response = r.json()
    assert response["message"] == "Word received"
