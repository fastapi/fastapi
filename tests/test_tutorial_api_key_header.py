from fastapi.testclient import TestClient

from docs_src.security.tutorial_api_key_header import app

client = TestClient(app)


def test_public_endpoint():
    """Test que l'endpoint public fonctionne sans authentification."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Ceci est un endpoint public"}


def test_protected_endpoint_with_valid_api_key():
    """Test de l'endpoint protégé avec une API key valide."""
    response = client.get("/protected", headers={"X-API-Key": "your-secret-api-key"})
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "john_doe" in data["message"]
    assert data["user_role"] == "admin"
    assert "protected_data" in data


def test_protected_endpoint_without_api_key():
    """Test de l'endpoint protégé sans API key."""
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json() == {"detail": "API Key manquante"}


def test_protected_endpoint_with_invalid_api_key():
    """Test de l'endpoint protégé avec une API key invalide."""
    response = client.get("/protected", headers={"X-API-Key": "wrong-key"})
    assert response.status_code == 401
    assert response.json() == {"detail": "API Key invalide"}


def test_users_me_endpoint_with_valid_api_key():
    """Test de l'endpoint /users/me avec une API key valide."""
    response = client.get("/users/me", headers={"X-API-Key": "your-secret-api-key"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "john_doe"
    assert data["role"] == "admin"


def test_users_me_endpoint_without_api_key():
    """Test de l'endpoint /users/me sans API key."""
    response = client.get("/users/me")
    assert response.status_code == 401


def test_openapi_schema():
    """Test que le schéma OpenAPI inclut bien la sécurité API Key."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    openapi_schema = response.json()

    # Vérifier que le composant de sécurité API Key est présent
    assert "components" in openapi_schema
    assert "securitySchemes" in openapi_schema["components"]

    security_schemes = openapi_schema["components"]["securitySchemes"]

    # Rechercher le scheme APIKeyHeader
    api_key_scheme = None
    for _scheme_name, scheme_data in security_schemes.items():
        if scheme_data.get("type") == "apiKey" and scheme_data.get("in") == "header":
            api_key_scheme = scheme_data
            break

    assert api_key_scheme is not None
    assert api_key_scheme["name"] == "X-API-Key"

    # Vérifier que les endpoints protégés ont bien la sécurité définie
    paths = openapi_schema["paths"]

    # L'endpoint /protected devrait avoir de la sécurité
    protected_endpoint = paths["/protected"]["get"]
    assert "security" in protected_endpoint

    # L'endpoint public ne devrait pas avoir de sécurité
    public_endpoint = paths["/"]["get"]
    assert "security" not in public_endpoint or public_endpoint.get("security") == []
