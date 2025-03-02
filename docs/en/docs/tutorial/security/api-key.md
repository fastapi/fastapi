# API Key Authentication

API Key authentication is a simple and common way to authenticate API requests. In this approach, clients include a special key in their request headers to prove their identity.

## Import Dependencies

First, import the required FastAPI components:

```python
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
```

## Create the API Key Header

Define the header that will contain the API key. By convention, API key headers often start with `X-`:

```python
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")
```

## Create the Authentication Function

Create a function that will validate the API key and return the authenticated user's data:

```python
def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    """Verify the API key and return user data."""
    # In a real application, you would verify the API key against a database
    if api_key == "your-secure-api-key":
        return {
            "user_id": 123,
            "permissions": ["read", "write"]
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
        headers={"WWW-Authenticate": "ApiKey"},
    )
```

## Use the Authentication in Your Routes

Apply the authentication to your routes using FastAPI's dependency injection:

```python
app = FastAPI()

@app.get("/secure-endpoint/")
def secure_endpoint(user_data: dict = Depends(verify_api_key)):
    return {
        "message": "You have access!",
        "user_data": user_data
    }
```

## Making Authenticated Requests

To access the protected endpoint, include the API key in your request headers:

```bash
curl -H "X-API-Key: your-secure-api-key" http://localhost:8000/secure-endpoint/
```

## Complete Example

Here's a complete example that includes database integration:

```python
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from starlette import status
from typing import Optional
from pydantic import BaseModel

# Models
class User(BaseModel):
    id: int
    username: str
    permissions: list[str]

# Setup
app = FastAPI()
API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

# Simulated database (replace with your actual database logic)
api_keys_db = {
    "your-secure-api-key": User(
        id=123,
        username="admin",
        permissions=["read", "write"]
    )
}

def get_user_from_api_key(api_key: str) -> Optional[User]:
    """Get user data from database using API key."""
    return api_keys_db.get(api_key)

def verify_api_key(api_key: str = Depends(API_KEY_HEADER)) -> User:
    """Verify API key and return user data."""
    user = get_user_from_api_key(api_key)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return user

@app.get("/secure-endpoint/")
def secure_endpoint(user: User = Depends(verify_api_key)):
    return {
        "message": "You have access!",
        "user": user
    }

@app.get("/admin-endpoint/")
def admin_endpoint(user: User = Depends(verify_api_key)):
    if "write" not in user.permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return {
        "message": "You have admin access!",
        "user": user
    }
```

## Security Considerations

When implementing API key authentication:

1. Always use HTTPS in production to prevent key interception
2. Store API keys securely (hashed in the database)
3. Implement rate limiting to prevent abuse
4. Consider key expiration and rotation policies
5. Log authentication failures for security monitoring

## Alternative Header Names

While this example uses `X-API-Key`, you can use any header name that fits your needs:

```python
# Common alternatives
API_KEY_HEADER = APIKeyHeader(name="Authorization")  # Using "Bearer <api-key>"
API_KEY_HEADER = APIKeyHeader(name="Api-Key")
API_KEY_HEADER = APIKeyHeader(name="X-Auth-Token")
```

Just ensure you document the expected header name for your API consumers.
