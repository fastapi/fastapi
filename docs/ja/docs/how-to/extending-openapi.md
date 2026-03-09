# OpenAPI の拡張 { #extending-openapi }

生成された OpenAPI スキーマを変更する必要がある場合があります。

このセクションではその方法を説明します。

## 通常のプロセス { #the-normal-process }

通常（デフォルト）のプロセスは次のとおりです。

`FastAPI` アプリケーション（インスタンス）には、OpenAPI スキーマを返すことが期待される `.openapi()` メソッドがあります。

アプリケーションオブジェクトの作成時に、`/openapi.json`（または `openapi_url` に設定したパス）への path operation が登録されます。

これは単に、アプリケーションの `.openapi()` メソッドの結果を含む JSON レスポンスを返します。

デフォルトでは、`.openapi()` メソッドはプロパティ `.openapi_schema` に内容があるかを確認し、あればそれを返します。

なければ、`fastapi.openapi.utils.get_openapi` にあるユーティリティ関数を使って生成します。

この関数 `get_openapi()` は次の引数を受け取ります:

- `title`: ドキュメントに表示される OpenAPI のタイトル。
- `version`: API のバージョン。例: `2.5.0`。
- `openapi_version`: 使用する OpenAPI 仕様のバージョン。デフォルトは最新の `3.1.0`。
- `summary`: API の短い概要。
- `description`: API の説明。Markdown を含めることができ、ドキュメントに表示されます。
- `routes`: ルートのリスト。登録済みの各 path operation です。`app.routes` から取得されます。

/// info | 情報

パラメータ `summary` は OpenAPI 3.1.0 以降で利用可能で、FastAPI 0.99.0 以降が対応しています。

///

## デフォルトの上書き { #overriding-the-defaults }

上記の情報を使って、同じユーティリティ関数で OpenAPI スキーマを生成し、必要な部分を上書きできます。

たとえば、<a href="https://github.com/Rebilly/ReDoc/blob/master/docs/redoc-vendor-extensions.md#x-logo" class="external-link" target="_blank">カスタムロゴを含めるための ReDoc の OpenAPI 拡張</a>を追加してみましょう。

### 通常の **FastAPI** { #normal-fastapi }

まず、通常どおりに **FastAPI** アプリケーションを実装します:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[1,4,7:9] *}

### OpenAPI スキーマの生成 { #generate-the-openapi-schema }

次に、`custom_openapi()` 関数内で同じユーティリティ関数を使って OpenAPI スキーマを生成します:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[2,15:21] *}

### OpenAPI スキーマの変更 { #modify-the-openapi-schema }

OpenAPI スキーマの `info`「オブジェクト」にカスタムの `x-logo` を追加して、ReDoc 拡張を加えます:

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[22:24] *}

### OpenAPI スキーマのキャッシュ { #cache-the-openapi-schema }

生成したスキーマを保持する「キャッシュ」として `.openapi_schema` プロパティを利用できます。

こうすることで、ユーザーが API ドキュメントを開くたびにスキーマを生成する必要がなくなります。

最初の1回だけ生成され、その後は同じキャッシュ済みスキーマが以降のリクエストで使われます。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[13:14,25:26] *}

### メソッドの上書き { #override-the-method }

これで、`.openapi()` メソッドを新しい関数に置き換えられます。

{* ../../docs_src/extending_openapi/tutorial001_py310.py hl[29] *}

### 確認 { #check-it }

<a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> にアクセスすると、カスタムロゴ（この例では **FastAPI** のロゴ）が使われていることが確認できます:

<img src="/img/tutorial/extending-openapi/image01.png">
