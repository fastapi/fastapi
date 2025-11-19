from typing import Optional

from fastapi import FastAPI, HTTPException, Security, status
from fastapi.security import APIKeyHeader

app = FastAPI()

API_KEY = "supersecret"
API_KEY_NAME = "X-API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


async def get_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authenticated",
        )
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )
    return api_key


@app.get("/protected-route")
async def protected_route(api_key: str = Security(get_api_key)):
    return {"message": "You are authorized"}
