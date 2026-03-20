# 使用舊的 403 身分驗證錯誤狀態碼 { #use-old-403-authentication-error-status-codes }

在 FastAPI 版本 `0.122.0` 之前，當內建的安全工具在身分驗證失敗後回傳錯誤給用戶端時，會使用 HTTP 狀態碼 `403 Forbidden`。

從 FastAPI 版本 `0.122.0` 起，改為使用更合適的 HTTP 狀態碼 `401 Unauthorized`，並在回應中依據 HTTP 規範加上合理的 `WWW-Authenticate` 標頭，參考 <a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>、<a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>。

但如果你的用戶端因某些原因依賴於舊行為，你可以在你的 security 類別中覆寫 `make_not_authenticated_error` 方法以恢復舊的行為。

例如，你可以建立 `HTTPBearer` 的子類別，讓它回傳 `403 Forbidden` 錯誤，而不是預設的 `401 Unauthorized` 錯誤：

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip
注意這個函式回傳的是例外物件本身，而不是直接拋出它。拋出的動作會在其餘的內部程式碼中處理。
///
