import pytest
from fastapi.testclient import TestClient

from docs_src.cors.tutorial001 import app, origins


@pytest.fixture(name="client")
def get_test_client():
    return TestClient(app)


class TestCORS:
    allowed_origins = origins

    @pytest.mark.parametrize("allowed_origin_url", origins)
    def test_preflight_with_allowed_origin(self, client, allowed_origin_url):
        origin_url = allowed_origin_url
        headers = {
            "Origin": origin_url,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Example",
        }
        response = client.options("/", headers=headers)
        assert origin_url in self.allowed_origins
        # response
        assert response.status_code == 200
        # response headers: cors
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-credentials" in response.headers
        assert "access-control-max-age" in response.headers
        assert "access-control-allow-headers" in response.headers
        # response headers: cors: origin
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == origin_url

    def test_preflight_with_not_allowed_origin(self, client):
        origin_url = "https://www.example.com"
        headers = {
            "Origin": origin_url,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "X-Example",
        }
        response = client.options("/", headers=headers)
        assert origin_url not in self.allowed_origins
        # response
        assert response.status_code == 400
        # response headers: cors
        assert "access-control-allow-methods" in response.headers
        assert "access-control-allow-credentials" in response.headers
        assert "access-control-max-age" in response.headers
        assert "access-control-allow-headers" in response.headers
        # response headers: cors: origin
        assert "access-control-allow-origin" not in response.headers

    @pytest.mark.parametrize("allowed_origin_url", origins)
    def test_simple_response_with_allowed_origin(self, client, allowed_origin_url):
        origin_url = allowed_origin_url
        headers = {
            "Origin": origin_url,
        }
        response = client.get("/", headers=headers)
        assert origin_url in self.allowed_origins
        # response
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
        # response headers: cors
        assert "access-control-allow-methods" not in response.headers
        assert "access-control-allow-credentials" in response.headers
        assert "access-control-max-age" not in response.headers
        assert "access-control-allow-headers" not in response.headers
        # response headers: cors: origin
        assert "access-control-allow-origin" in response.headers
        assert response.headers["access-control-allow-origin"] == origin_url

    def test_simple_response_with_not_allowed_origin(self, client):
        origin_url = "https://example.com"
        headers = {
            "Origin": origin_url,
        }
        response = client.get("/", headers=headers)
        assert origin_url not in self.allowed_origins
        # response
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
        # response headers: cors
        assert "access-control-allow-methods" not in response.headers
        assert "access-control-allow-credentials" in response.headers
        assert "access-control-max-age" not in response.headers
        assert "access-control-allow-headers" not in response.headers
        # response headers: cors: origin
        assert "access-control-allow-origin" not in response.headers

    def test_non_cors_response(self, client):
        response = client.get("/")
        # response
        assert response.status_code == 200, response.text
        assert response.json() == {"message": "Hello World"}
        # response headers: cors
        assert "access-control-allow-methods" not in response.headers
        assert "access-control-allow-credentials" not in response.headers
        assert "access-control-max-age" not in response.headers
        assert "access-control-allow-headers" not in response.headers
        assert "access-control-allow-origin" not in response.headers
