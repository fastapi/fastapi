from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel

app = FastAPI()

# Configuration de l'API Key - normalement vous stockeriez cela de manière sécurisée
API_KEY = "your-secret-api-key"
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


class User(BaseModel):
    username: str
    role: str


def verify_api_key(api_key: str = Security(api_key_header)):
    """
    Vérifie si l'API key fournie est valide.

    Args:
        api_key: L'API key extraite de l'en-tête HTTP

    Returns:
        L'API key si elle est valide

    Raises:
        HTTPException: Si l'API key est manquante ou invalide
    """
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key manquante",
            headers={"WWW-Authenticate": "API-Key"},
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key invalide",
            headers={"WWW-Authenticate": "API-Key"},
        )
    return api_key


def get_current_user(api_key: str = Depends(verify_api_key)):
    """
    Retourne l'utilisateur actuel basé sur l'API key valide.

    Dans un vrai système, vous feriez une requête à votre base de données
    pour récupérer l'utilisateur associé à l'API key.
    """
    # Simulation d'une recherche d'utilisateur en base
    return User(username="john_doe", role="admin")


@app.get("/")
async def public_endpoint():
    """Point d'accès public - aucune authentification requise."""
    return {"message": "Ceci est un endpoint public"}


@app.get("/protected")
async def protected_endpoint(current_user: User = Depends(get_current_user)):
    """
    Point d'accès protégé - nécessite une API key valide.

    Pour tester cet endpoint:
    curl -H "X-API-Key: your-secret-api-key" http://localhost:8000/protected
    """
    return {
        "message": f"Bonjour {current_user.username}!",
        "user_role": current_user.role,
        "protected_data": "Données sensibles accessibles uniquement avec une API key valide",
    }


@app.get("/users/me")
async def read_current_user(current_user: User = Depends(get_current_user)):
    """Récupère les informations de l'utilisateur actuel."""
    return current_user
