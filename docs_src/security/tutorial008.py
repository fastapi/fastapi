import secrets

from fastapi import FastAPI, Security, status
from fastapi.exceptions import HTTPException
from fastapi.security.api_key import APIKeyHeader

api_key_header_auth = APIKeyHeader(
    name="X-API-KEY",
    description="Mandatory API Token, required for all endpoints",
    auto_error=True,
)


async def get_api_key(api_key_header: str = Security(api_key_header_auth)):
    correct_api_key = secrets.compare_digest(api_key_header, "randomized-string-1234")
    if not correct_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key",
        )


app = FastAPI(dependencies=[Security(get_api_key)])


@app.get("/health")
async def endpoint():
    return {"Hello": "World"}
