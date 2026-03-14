# Security ٹولز

جب آپ کو OAuth2 scopes کے ساتھ dependencies declare کرنی ہوں تو آپ `Security()` استعمال کرتے ہیں۔

لیکن آپ کو پھر بھی یہ define کرنا ہوگا کہ dependable کیا ہے، یعنی وہ callable جو آپ `Depends()` یا `Security()` کو parameter کے طور پر دیتے ہیں۔

ایسے dependables بنانے کے لیے کئی ٹولز دستیاب ہیں، اور یہ OpenAPI میں ضم ہو جاتے ہیں تاکہ یہ خودکار docs UI میں دکھائے جائیں، خودکار طور پر بنائے گئے clients اور SDKs کے ذریعے استعمال ہو سکیں، وغیرہ۔

آپ انہیں `fastapi.security` سے import کر سکتے ہیں:

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

ان کے بارے میں مزید پڑھیں [FastAPI دستاویزات میں Security](https://fastapi.tiangolo.com/tutorial/security/)۔

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

## OAuth2 Security Scopes میں Dependencies

::: fastapi.security.SecurityScopes

## OpenID Connect

::: fastapi.security.OpenIdConnect
