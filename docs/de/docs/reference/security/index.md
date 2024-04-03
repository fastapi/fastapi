# Sicherheitstools

Wenn Sie Abhängigkeiten mit OAuth2-Scopes deklarieren müssen, verwenden Sie `Security()`.

Aber Sie müssen immer noch definieren, was das <abbr title="Das von dem abhängt, die zu verwendende Abhängigkeit">Dependable</abbr>, das Callable ist, welches Sie als Parameter an `Depends()` oder `Security()` übergeben.

Es gibt mehrere Tools, mit denen Sie diese Dependables erstellen können, und sie werden in OpenAPI integriert, sodass sie in der Oberfläche der automatischen Dokumentation angezeigt werden und von automatisch generierten Clients und SDKs, usw., verwendet werden können.

Sie können sie von `fastapi.security` importieren:

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

## API-Schlüssel-Sicherheitsschemas

::: fastapi.security.APIKeyCookie

::: fastapi.security.APIKeyHeader

::: fastapi.security.APIKeyQuery

## HTTP-Authentifizierungsschemas

::: fastapi.security.HTTPBasic

::: fastapi.security.HTTPBearer

::: fastapi.security.HTTPDigest

## HTTP-Anmeldeinformationen

::: fastapi.security.HTTPAuthorizationCredentials

::: fastapi.security.HTTPBasicCredentials

## OAuth2-Authentifizierung

::: fastapi.security.OAuth2

::: fastapi.security.OAuth2AuthorizationCodeBearer

::: fastapi.security.OAuth2PasswordBearer

## OAuth2-Passwortformulare

::: fastapi.security.OAuth2PasswordRequestForm

::: fastapi.security.OAuth2PasswordRequestFormStrict

## OAuth2-Sicherheitsscopes in Abhängigkeiten

::: fastapi.security.SecurityScopes

## OpenID Connect

::: fastapi.security.OpenIdConnect
