# カスタムドキュメント UI の静的アセット（セルフホスティング） { #custom-docs-ui-static-assets-self-hosting }

API ドキュメントは **Swagger UI** と **ReDoc** を使用しており、それぞれにいくつかの JavaScript と CSS ファイルが必要です。

既定では、これらのファイルは <abbr title="Content Delivery Network - コンテンツ配信ネットワーク: 通常は複数のサーバーで構成され、JavaScript や CSS などの静的ファイルを提供するサービス。クライアントに近いサーバーからそれらのファイルを配信することで、パフォーマンスを改善するためによく使われます。">CDN</abbr> から配信されます。

しかし、カスタマイズすることも可能で、特定の CDN を指定したり、自分でファイルを配信したりできます。

## JavaScript と CSS のカスタム CDN { #custom-cdn-for-javascript-and-css }

別の <abbr title="Content Delivery Network - コンテンツ配信ネットワーク">CDN</abbr> を使いたいとします。例えば `https://unpkg.com/` を使いたい場合です。

例えば、一部の URL が制限されている国に住んでいる場合に役立ちます。

### 自動ドキュメントの無効化 { #disable-the-automatic-docs }

最初の手順は自動ドキュメントを無効化することです。デフォルトではそれらは既定の CDN を使用します。

無効化するには、`FastAPI` アプリ作成時にそれらの URL を `None` に設定します:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[8] *}

### カスタムドキュメントの追加 { #include-the-custom-docs }

これで、カスタムドキュメント用の *path operations* を作成できます。

FastAPI の内部関数を再利用してドキュメント用の HTML ページを生成し、必要な引数を渡せます:

- `openapi_url`: ドキュメントの HTML ページが API の OpenAPI スキーマを取得する URL。ここでは属性 `app.openapi_url` を使用できます。
- `title`: API のタイトル。
- `oauth2_redirect_url`: 既定値を使うにはここで `app.swagger_ui_oauth2_redirect_url` を使用できます。
- `swagger_js_url`: Swagger UI ドキュメント用の HTML が取得する JavaScript ファイルの URL。これはカスタム CDN の URL です。
- `swagger_css_url`: Swagger UI ドキュメント用の HTML が取得する CSS ファイルの URL。これはカスタム CDN の URL です。

ReDoc についても同様です...

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[2:6,11:19,22:24,27:33] *}

/// tip | 豆知識

`swagger_ui_redirect` 用の *path operation* は、OAuth2 を使用する場合の補助です。

API を OAuth2 プロバイダと統合すると、認証を実行して取得したクレデンシャルを持った状態で API ドキュメントに戻れます。そして実際の OAuth2 認証を用いてドキュメント上から API と対話できます。

Swagger UI がこの処理を裏側で行いますが、そのためにこの「redirect」の補助が必要です。

///

### テスト用の *path operation* を作成 { #create-a-path-operation-to-test-it }

すべてが動作するかをテストできるように、*path operation* を作成します:

{* ../../docs_src/custom_docs_ui/tutorial001_py310.py hl[36:38] *}

### テスト { #test-it }

これで、<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> にアクセスしてページを再読み込みすると、新しい CDN からそれらのアセットが読み込まれるはずです。

## ドキュメント用 JavaScript と CSS のセルフホスティング { #self-hosting-javascript-and-css-for-docs }

オフライン（インターネット非接続）でも、あるいはローカルネットワークで、アプリを動作させたい場合などには、JavaScript と CSS をセルフホストするのが有用です。

ここでは、同じ FastAPI アプリ内でそれらのファイルを配信し、ドキュメントでそれらを使用するように設定する方法を示します。

### プロジェクトのファイル構成 { #project-file-structure }

プロジェクトのファイル構成が次のようになっているとします:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
```

これらの静的ファイルを保存するためのディレクトリを作成します。

新しいファイル構成は次のようになります:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static/
```

### ファイルのダウンロード { #download-the-files }

ドキュメントに必要な静的ファイルをダウンロードし、`static/` ディレクトリに配置します。

各リンクを右クリックして「リンク先を別名で保存...」のようなオプションを選べます。

**Swagger UI** では次のファイルを使用します:

- <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js" class="external-link" target="_blank">`swagger-ui-bundle.js`</a>
- <a href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css" class="external-link" target="_blank">`swagger-ui.css`</a>

そして **ReDoc** では次のファイルを使用します:

- <a href="https://cdn.jsdelivr.net/npm/redoc@2/bundles/redoc.standalone.js" class="external-link" target="_blank">`redoc.standalone.js`</a>

その後、ファイル構成は次のようになります:

```
.
├── app
│   ├── __init__.py
│   ├── main.py
└── static
    ├── redoc.standalone.js
    ├── swagger-ui-bundle.js
    └── swagger-ui.css
```

### 静的ファイルの配信 { #serve-the-static-files }

- `StaticFiles` をインポートします。
- 特定のパスに `StaticFiles()` インスタンスを「マウント」します。

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[7,11] *}

### 静的ファイルのテスト { #test-the-static-files }

アプリケーションを起動し、<a href="http://127.0.0.1:8000/static/redoc.standalone.js" class="external-link" target="_blank">http://127.0.0.1:8000/static/redoc.standalone.js</a> にアクセスします。

**ReDoc** 用の非常に長い JavaScript ファイルが表示されるはずです。

先頭は次のようになっているかもしれません:

```JavaScript
/*! For license information please see redoc.standalone.js.LICENSE.txt */
!function(e,t){"object"==typeof exports&&"object"==typeof module?module.exports=t(require("null")):
...
```

これで、アプリから静的ファイルを配信できていること、そしてドキュメント用の静的ファイルを正しい場所に配置できていることが確認できます。

次に、ドキュメントでそれらの静的ファイルを使用するようにアプリを設定します。

### 静的ファイル用に自動ドキュメントを無効化 { #disable-the-automatic-docs-for-static-files }

カスタム CDN を使う場合と同様、最初の手順は自動ドキュメントを無効化することです。既定では CDN を使用します。

無効化するには、`FastAPI` アプリ作成時にそれらの URL を `None` に設定します:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[9] *}

### 静的ファイル用のカスタムドキュメントを追加 { #include-the-custom-docs-for-static-files }

カスタム CDN と同様の方法で、カスタムドキュメント用の *path operations* を作成できます。

再び、FastAPI の内部関数を再利用してドキュメント用の HTML ページを生成し、必要な引数を渡します:

- `openapi_url`: ドキュメントの HTML ページが API の OpenAPI スキーマを取得する URL。ここでは属性 `app.openapi_url` を使用できます。
- `title`: API のタイトル。
- `oauth2_redirect_url`: 既定値を使うにはここで `app.swagger_ui_oauth2_redirect_url` を使用できます。
- `swagger_js_url`: Swagger UI ドキュメント用の HTML が取得する **JavaScript** ファイルの URL。**これはあなたのアプリ自身がいま配信しているものです**。
- `swagger_css_url`: Swagger UI ドキュメント用の HTML が取得する **CSS** ファイルの URL。**これはあなたのアプリ自身がいま配信しているものです**。

ReDoc についても同様です...

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[2:6,14:22,25:27,30:36] *}

/// tip | 豆知識

`swagger_ui_redirect` 用の *path operation* は、OAuth2 を使用する場合の補助です。

API を OAuth2 プロバイダと統合すると、認証を実行して取得したクレデンシャルを持った状態で API ドキュメントに戻れます。そして実際の OAuth2 認証を用いてドキュメント上から API と対話できます。

Swagger UI がこの処理を裏側で行いますが、そのためにこの「redirect」の補助が必要です。

///

### 静的ファイルをテストするための *path operation* を作成 { #create-a-path-operation-to-test-static-files }

すべてが動作するかをテストできるように、*path operation* を作成します:

{* ../../docs_src/custom_docs_ui/tutorial002_py310.py hl[39:41] *}

### 静的ファイル UI のテスト { #test-static-files-ui }

これで、WiFi を切断して <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> にアクセスし、ページを再読み込みできるはずです。

インターネットに接続していなくても、API のドキュメントを表示し、API と対話できます。
