from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader

app = FastAPI()

API_KEY = "your-secret-api-key"

api_key_header = APIKeyHeader(name="X-API-Key")


def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key"
        )
    return api_key


@app.get("/protected")
def read_protected_data(api_key: str = Depends(verify_api_key)):
    return {"message": "This is protected data", "api_key": api_key}
