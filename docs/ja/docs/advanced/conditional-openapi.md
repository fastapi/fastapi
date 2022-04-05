# 条件付き OpenAPI

必要であれば、設定と環境変数を利用して、環境に応じて条件付きでOpenAPIを構成することが可能です。また、完全にOpenAPIを無効にすることもできます。

## セキュリティとAPI、およびドキュメントについて

本番環境においてドキュメントのUIを非表示にすることによって、APIを保護しようと *すべきではありません*。

それは、APIのセキュリティの強化にはならず、*path operations* は依然として利用可能です。

もしセキュリティ上の欠陥がソースコードにあるならば、それは存在したままです。

ドキュメンテーションを非表示にするのは、単にあなたのAPIへのアクセス方法を難解にするだけでなく、同時にあなた自身の本番環境でのAPIのデバッグを困難にしてしまう可能性があります。単純に、 <a href="https://en.wikipedia.org/wiki/Security_through_obscurity" class="external-link" target="_blank">Security through obscurity</a> の一つの形態として考えられるでしょう。

もしあなたのAPIのセキュリティを強化したいなら、いくつかのよりよい方法があります。例を示すと、

* リクエストボディとレスポンスのためのPydanticモデルの定義を見直す。
* 依存関係に基づきすべての必要なパーミッションとロールを設定する。
* パスワードを絶対に平文で保存しない。パスワードハッシュのみを保存する。
* PasslibやJWTトークンに代表される、よく知られた暗号化ツールを使って実装する。
* そして必要なところでは、もっと細かいパーミッション制御をOAuth2スコープを使って行う。
* など

それでも、例えば本番環境のような特定の環境のみで、あるいは環境変数の設定によってAPIドキュメントをどうしても無効にしたいという、非常に特殊なユースケースがあるかもしれません。

## 設定と環境変数による条件付き OpenAPI

生成するOpenAPIとドキュメントUIの構成は、共通のPydanticの設定を使用して簡単に切り替えられます。

例えば、

```Python hl_lines="6  11"
{!../../../docs_src/conditional_openapi/tutorial001.py!}
```

ここでは `openapi_url` の設定を、デフォルトの `"/openapi.json"` のまま宣言しています。

そして、これを `FastAPI` appを作る際に使います。

それから、以下のように `OPENAPI_URL` という環境変数を空文字列に設定することによってOpenAPI (UIドキュメントを含む) を無効化することができます。

<div class="termy">

```console
$ OPENAPI_URL= uvicorn main:app

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

すると、以下のように `/openapi.json`, `/docs`, `/redoc` のどのURLにアクセスしても、 `404 Not Found` エラーが返ってくるようになります。

```JSON
{
    "detail": "Not Found"
}
```
