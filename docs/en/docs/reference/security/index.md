# Security Tools

When you need to declare dependencies with OAuth2 scopes you use `Security()`.

But you still need to define what is the dependable, the callable that you pass as a parameter to `Depends()` or `Security()`.

There are multiple tools that you can use to create those dependables, and they get integrated into OpenAPI so they are shown in the automatic docs UI, they can be used by automatically generated clients and SDKs, etc.

You can import them from `fastapi.security`:

```python
from fastapi.security import (
    APIKeyCookie,
    APIKeyHeader,
    APIKeyQuery,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPDigest,
    OAuth2,
    OAuth2AuthorizationCodeBearer,
    OAuth2PasswordBearer,
    OAuth2PasswordRequestForm,
    OAuth2PasswordRequestFormStrict,
    OpenIdConnect,
    SecurityScopes,
)
```

Read more about them in the [FastAPI docs about Security](https://fastapi.tiangolo.com/tutorial/security/).

## API Key Security Schemes

::: fastapi.security.APIKeyCookie

::: fastapi.security.APIKeyHeader

### Using APIKeyHeader

`APIKeyHeader` is a security tool for extracting API keys from HTTP headers.

Here’s a simple example of how to use it in FastAPI:

```python
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

app = FastAPI()

API_KEY = "mysecretapikey"
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

@app.get("/secure-data")
async def secure_data(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return {"message": "Secure data accessed"}
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate API key"
        )




::: fastapi.security.APIKeyQuery

## HTTP Authentication Schemes

::: fastapi.security.HTTPBasic

::: fastapi.security.HTTPBearer

::: fastapi.security.HTTPDigest

## HTTP Credentials

::: fastapi.security.HTTPAuthorizationCredentials

::: fastapi.security.HTTPBasicCredentials

## OAuth2 Authentication

::: fastapi.security.OAuth2

::: fastapi.security.OAuth2AuthorizationCodeBearer

::: fastapi.security.OAuth2PasswordBearer

## OAuth2 Password Form

::: fastapi.security.OAuth2PasswordRequestForm

::: fastapi.security.OAuth2PasswordRequestFormStrict

## OAuth2 Security Scopes in Dependencies

::: fastapi.security.SecurityScopes

## OpenID Connect

::: fastapi.security.OpenIdConnect
