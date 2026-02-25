# 使用旧的 403 认证错误状态码 { #use-old-403-authentication-error-status-codes }

在 FastAPI `0.122.0` 版本之前，当内置的安全工具在认证失败后向客户端返回错误时，会使用 HTTP 状态码 `403 Forbidden`。

从 FastAPI `0.122.0` 版本开始，它们改用更合适的 HTTP 状态码 `401 Unauthorized`，并在响应中返回合理的 `WWW-Authenticate` 头，遵循 HTTP 规范，<a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>、<a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>。

但如果由于某些原因你的客户端依赖旧行为，你可以在你的安全类中重写方法 `make_not_authenticated_error` 来回退到旧行为。

例如，你可以创建一个 `HTTPBearer` 的子类，使其返回 `403 Forbidden` 错误，而不是默认的 `401 Unauthorized` 错误：

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | 提示

注意该函数返回的是异常实例，而不是直接抛出它。抛出操作由其余的内部代码完成。

///
