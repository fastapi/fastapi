# APIKey Header

FastAPI supports using **API keys** as an alternative to OAuth2/JWT.

This is useful when you want to quickly secure an endpoint with a simple key check.

---

## 📘 Example

```python
from fastapi import FastAPI, Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

API_KEY = "supersecretapikey"
api_key_header = APIKeyHeader(name="X-API-Key")

def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate API KEY")
    return api_key

@app.get("/secure-data/")
def secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "You have access to secure data!"}
```
