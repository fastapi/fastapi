# Request を直接使う { #using-the-request-directly }

これまで、必要なリクエストの各部分を、その型とともに宣言してきました。

次の場所からデータを取得します:

- パスのパラメータ
- ヘッダー
- クッキー
- など

こうすることで、**FastAPI** はそのデータを検証し、変換し、API のドキュメントを自動生成します。

しかし、`Request` オブジェクトに直接アクセスする必要がある場面もあります。

## `Request` オブジェクトの詳細 { #details-about-the-request-object }

**FastAPI** は内部的には **Starlette** の上にいくつかのツール層を載せたものなので、必要に応じて Starlette の <a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">`Request`</a> オブジェクトを直接使えます。

また、`Request` オブジェクトから直接データ（例: ボディ）を取得する場合、そのデータは FastAPI によって検証・変換・ドキュメント化（OpenAPI による自動 API ユーザーインターフェース向け）されません。

ただし、通常どおりに宣言された他のパラメータ（例: Pydantic モデルのボディ）は引き続き検証・変換・注釈付けなどが行われます。

それでも、`Request` オブジェクトを取得するのが有用な特定のケースがあります。

## `Request` オブジェクトを直接使う { #use-the-request-object-directly }

たとえば、path operation 関数内でクライアントの IP アドレス／ホストを取得したいとします。

そのためには、リクエストに直接アクセスする必要があります。

{* ../../docs_src/using_request_directly/tutorial001_py310.py hl[1,7:8] *}

path operation 関数の引数として `Request` 型のパラメータを宣言すると、**FastAPI** はその引数に `Request` を渡します。

/// tip | 豆知識

この例では、`Request` 型の引数に加えて、パスパラメータも宣言しています。

そのため、パスパラメータは取り出され、検証され、指定した型に変換され、OpenAPI で注釈（ドキュメント化）されます。

同様に、通常どおり任意の他のパラメータを宣言しつつ、追加で `Request` も受け取れます。

///

## `Request` のドキュメント { #request-documentation }

より詳しくは、<a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">公式 Starlette ドキュメントサイトの `Request` オブジェクト</a>を参照してください。

/// note | 技術詳細

`from starlette.requests import Request` を使うこともできます。

**FastAPI** は開発者である皆さんの便宜のために直接提供していますが、これは Starlette からそのまま提供されているものです。

///
