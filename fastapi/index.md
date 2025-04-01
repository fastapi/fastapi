## Authentication with API Key in Header

FastAPI makes it easy to authenticate users by passing an API key through HTTP headers.

### Example: API Key Authentication

The following is a simple example where an API key is passed through the request header for authentication:

```python
from fastapi import FastAPI, Header, HTTPException, Depends

app = FastAPI()

# Dependency to check API key in header
def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != "mysecretapikey123":
        raise HTTPException(status_code=400, detail="Invalid API Key")
    return x_api_key

@app.get("/secure-data")
async def get_secure_data(api_key: str = Depends(get_api_key)):
    return {"message": "This is secure data."}

curl -X 'GET' \
  'http://127.0.0.1:8000/secure-data' \
  -H 'x-api-key: mysecretapikey123'
