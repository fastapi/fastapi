# 安全工具

当您需要使用 OAuth2 作用域声明依赖关系时，可以使用 `Security()`。

但您仍然需要定义什么是依赖项，即作为参数传递给`Depends()`或`Security()`的可调用项。

您可以使用多种工具来创建这些依赖项，并将它们集成到 OpenAPI 中，这样它们就会显示在自动文档用户界面中，自动生成的客户端和 SDK 等也可以使用它们。

您可以从 `fastapi.security` 中导入它们：

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

## API 密钥安全机制

::: fastapi.security.APIKeyCookie

::: fastapi.security.APIKeyHeader

::: fastapi.security.APIKeyQuery

## HTTP 认证方案

::: fastapi.security.HTTPBasic

::: fastapi.security.HTTPBearer

::: fastapi.security.HTTPDigest

## HTTP 凭据

::: fastapi.security.HTTPAuthorizationCredentials

::: fastapi.security.HTTPBasicCredentials

## OAuth 2.0 认证

::: fastapi.security.OAuth2

::: fastapi.security.OAuth2AuthorizationCodeBearer

::: fastapi.security.OAuth2PasswordBearer

## OAuth 2.0 密码表单模式

::: fastapi.security.OAuth2PasswordRequestForm

::: fastapi.security.OAuth2PasswordRequestFormStrict

## 依赖项中的 OAuth2 安全范围

::: fastapi.security.SecurityScopes

## OpenID 连接

::: fastapi.security.OpenIdConnect
