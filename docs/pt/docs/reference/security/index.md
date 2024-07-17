# Ferramentas de Segurança

Quando você precisa declarar dependências com escopos OAuth2, você usa `Security()`.

Mas você ainda precisa definir qual é a dependência, a função que você passa como parâmetro para `Depends()` ou `Security()`.

Existem várias ferramentas que você pode usar para criar essas dependências, e elas se integram ao OpenAPI para serem exibidas na UI de documentação automática. Elas podem ser usadas por clientes e SDKs gerados automaticamente, etc.

Você pode importá-las de `fastapi.security`:

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

::: fastapi.security.APIKeyHeader

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
