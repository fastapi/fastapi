# 古い 403 認証エラーのステータスコードを使う { #use-old-403-authentication-error-status-codes }

FastAPI バージョン `0.122.0` より前は、統合されたセキュリティユーティリティが認証に失敗してクライアントへエラーを返す際、HTTP ステータスコード `403 Forbidden` を使用していました。

FastAPI バージョン `0.122.0` 以降では、より適切な HTTP ステータスコード `401 Unauthorized` を使用し、HTTP 仕様に従ってレスポンスに妥当な `WWW-Authenticate` ヘッダーを含めます。<a href="https://datatracker.ietf.org/doc/html/rfc7235#section-3.1" class="external-link" target="_blank">RFC 7235</a>、<a href="https://datatracker.ietf.org/doc/html/rfc9110#name-401-unauthorized" class="external-link" target="_blank">RFC 9110</a>。

しかし、何らかの理由でクライアントが従来の挙動に依存している場合は、セキュリティクラスでメソッド `make_not_authenticated_error` をオーバーライドすることで、その挙動に戻せます。

たとえば、既定の `401 Unauthorized` エラーの代わりに `403 Forbidden` エラーを返す `HTTPBearer` のサブクラスを作成できます:

{* ../../docs_src/authentication_error_status_code/tutorial001_an_py310.py hl[9:13] *}

/// tip | 豆知識

この関数は例外インスタンスを返す点に注意してください。ここでは例外を送出しません。送出は内部の他のコードで行われます。

///
