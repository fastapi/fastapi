# Security Tools

When you need to declare dependencies with OAuth2 scopes you use `Security()`.

But you still need to define what is the dependable, the callable that you pass as
a parameter to `Depends()` or `Security()`.

There are multiple tools that you can use to create those dependables, and they get
integrated into OpenAPI so they are shown in the automatic docs UI, they can be used
by automatically generated clients and SDKs, etc.

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

## API Key Security Schemes

::: fastapi.security.APIKeyCookie
    options:
        members:

::: fastapi.security.APIKeyHeader
    options:
        members:

::: fastapi.security.APIKeyQuery
    options:
        members:

## HTTP Authentication Schemes

::: fastapi.security.HTTPBasic
    options:
        members:

::: fastapi.security.HTTPBearer
    options:
        members:

::: fastapi.security.HTTPDigest
    options:
        members:

## HTTP Credentials

::: fastapi.security.HTTPAuthorizationCredentials
    options:
        members:

::: fastapi.security.HTTPBasicCredentials
    options:
        members:

## OAuth2 Authentication

::: fastapi.security.OAuth2
    options:
        members:

::: fastapi.security.OAuth2AuthorizationCodeBearer
    options:
        members:

::: fastapi.security.OAuth2PasswordBearer
    options:
        members:

## OAuth2 Password Form

::: fastapi.security.OAuth2PasswordRequestForm
    options:
        members:

::: fastapi.security.OAuth2PasswordRequestFormStrict
    options:
        members:

## OAuth2 Security Scopes in Dependencies

::: fastapi.security.SecurityScopes
    options:
        members:

## OpenID Connect

::: fastapi.security.OpenIdConnect
    options:
        members:
