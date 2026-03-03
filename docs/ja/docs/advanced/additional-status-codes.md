# 追加のステータスコード { #additional-status-codes }

デフォルトでは、 **FastAPI** は `JSONResponse` を使ってレスポンスを返し、*path operation* から返した内容をその `JSONResponse` の中に入れます。

デフォルトのステータスコード、または *path operation* で設定したステータスコードが使用されます。

## 追加のステータスコード { #additional-status-codes_1 }

メインのステータスコードとは別に追加のステータスコードを返したい場合は、`JSONResponse` のような `Response` を直接返し、追加のステータスコードを直接設定できます。

たとえば、item を更新でき、成功時に HTTP ステータスコード 200 "OK" を返す *path operation* を作りたいとします。

しかし、新しい item も受け付けたいとします。そして、item が以前存在しなかった場合には作成し、HTTP ステータスコード 201「Created」を返します。

これを実現するには、`JSONResponse` をインポートし、望む `status_code` を設定して、そこで内容を直接返します。

{* ../../docs_src/additional_status_codes/tutorial001_an_py310.py hl[4,25] *}

/// warning

上の例のように `Response` を直接返すと、それはそのまま返されます。

モデルなどによってシリアライズされません。

必要なデータが含まれていること、そして（`JSONResponse` を使用している場合）値が有効な JSON であることを確認してください。

///

/// note | 技術詳細

`from starlette.responses import JSONResponse` を使うこともできます。

**FastAPI** は開発者の利便性のために、`fastapi.responses` と同じ `starlette.responses` を提供しています。しかし、利用可能なレスポンスのほとんどは Starlette から直接提供されています。`status` も同様です。

///

## OpenAPI と API ドキュメント { #openapi-and-api-docs }

追加のステータスコードとレスポンスを直接返す場合、それらは OpenAPI スキーマ（API ドキュメント）には含まれません。FastAPI には、事前に何が返されるかを知る方法がないからです。

しかし、[追加のレスポンス](additional-responses.md){.internal-link target=_blank} を使ってコード内にドキュメント化できます。
