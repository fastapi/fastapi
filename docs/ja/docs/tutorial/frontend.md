# フロントエンド { #frontend }

`app.frontend()`（または `router.frontend()`）で静的なフロントエンドアプリを配信できます。

これは、Vite を使った React、TanStack Router、Astro、Vue、Svelte、Angular、Solid など、静的ファイルを生成するフロントエンドツールで役立ちます。

これらのツールでは、通常、次のようなコマンドでフロントエンドをビルドするステップがあります。

```bash
npm run build
```

これにより、フロントエンドファイルを含む `./dist/` のようなディレクトリが生成されます。

`app.frontend()` を使うと、これらのフロントエンドフレームワークが必要とする規約に従って、そのディレクトリを配信できます。

**FastAPI** は最初に *path operations* をチェックします。通常のルートに一致しなかった場合にのみフロントエンドファイルがチェックされるため、API には影響しません。

## フロントエンドの配信 { #serve-a-frontend }

たとえば `npm run build` でフロントエンドをビルドした後、生成されたファイルを `dist` などのディレクトリに配置します。

プロジェクト構成は次のようになります。

```text
.
├── pyproject.toml
├── app
│   ├── __init__.py
│   └── main.py
└── dist
    ├── index.html
    └── assets
        └── app.js
```

そして `app.frontend()` で配信します。

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

これにより、`/assets/app.js` へのリクエストで `dist/assets/app.js` を配信できます。

**FastAPI** の *path operation* もある場合は、*path operation* が優先されます。

## クライアントサイドルーティング { #client-side-routing }

**single-page apps**（SPA）を含む多くのフロントエンドアプリは、クライアントサイドルーティングを使います。`/dashboard/settings` のようなパスは実際のファイルではなく、フレームワークが処理するものかもしれません。

そのため、その URL に直接アクセスした場合（アプリ内で遷移するのではなく）、バックエンドは `index.html` からフロントエンドアプリを配信し、フロントエンドフレームワークがクライアントサイドルーティングを処理できるようにする必要があります。

そのためには、`fallback="index.html"` を使います。

{* ../../docs_src/frontend/tutorial002_py310.py hl[5] *}

**FastAPI** は、このフォールバックを、通常のブラウザナビゲーションリクエストのように `Accept: text/html` または `Accept: application/xhtml+xml` で明示的に HTML を受け付ける `GET` および `HEAD` リクエストにのみ使用します。JavaScript、CSS、画像などの存在しないファイルは引き続き `404` を返します。

`POST` や `PUT` など、他のメソッドのリクエストがフロントエンドのフォールバックにのみ一致するパスへ送られた場合も、`404` を返します。通常の **FastAPI** の *path operations* は、フロントエンドのルートよりも引き続き高い優先順位を持ちます。

/// tip | 豆知識

デフォルトでは、`fallback` の値は `fallback="auto"` です。ほとんどの場合、`fallback` を指定する必要はありません。詳細は以下を参照してください。

///

これは、TanStack Router を使った React、Vue、Angular、SvelteKit、Solid など、クライアントサイドルーティングを使う多くのフロントエンドアプリで望まれる動作です。

## カスタム 404 ページ { #custom-404-page }

存在しないフロントエンドパスに対して、静的な `404.html` ページを配信することもできます。

{* ../../docs_src/frontend/tutorial003_py310.py hl[5] *}

そのレスポンスはステータスコード `404` を保持します。

この場合、**FastAPI** は存在しないフロントエンドパスに対して `index.html` を配信しません。代わりに `404.html` ファイルを返します。

/// tip | 豆知識

デフォルトでは、`fallback` の値は `fallback="auto"` です。これにより、`404.html` ファイルが見つかった場合、自動的にフォールバックとして使われます。

そのため、通常は `fallback` 引数を省略できます。

///

これは、Astro のように各ページの静的 HTML ファイルを生成するフロントエンドツールで役立ちます。

## 自動フォールバック { #fallback-auto }

デフォルトでは、`app.frontend()` は `fallback="auto"` を使います。

フロントエンドディレクトリに `404.html` ファイルがある場合、存在しないフロントエンドパスはそのファイルをステータスコード `404` で配信します。

そうでない場合、`index.html` ファイルがあれば、存在しないブラウザナビゲーションのパスは `index.html` を配信します。これは、クライアントサイドルーティングを使う多くのフロントエンドアプリが期待する動作です。

そのため、ほとんどの場合、`fallback` 引数を指定せずに `app.frontend("/", directory="dist")` を使用できます。

{* ../../docs_src/frontend/tutorial001_py310.py hl[5] *}

## フォールバックの無効化 { #disable-fallback }

存在しないフロントエンドパスに対してフォールバックファイルを配信したくない場合は、`fallback=None` を使います。

{* ../../docs_src/frontend/tutorial005_py310.py hl[5] *}

すると、存在しないフロントエンドパスは通常の `404` を返します。

## ディレクトリのチェック { #check-directory }

デフォルトでは、`app.frontend()` は `check_dir="auto"` を使います。

`FASTAPI_ENV` 環境変数が `development` に設定されている場合、フロントエンドのビルド出力ディレクトリが存在しなくても、**FastAPI** は警告を表示するだけです。[`fastapi dev` コマンド](https://github.com/fastapi/fastapi-cli#fastapi-dev) は、この環境変数がまだ設定されていない場合に設定してくれます。これにより、開発中にフロントエンドをビルドまたは起動する前にバックエンドを起動できます。

それ以外の環境では、**FastAPI** はアプリ作成時にエラーを発生させます。これにより、フロントエンドファイルなしでアプリをデプロイする前に、設定エラーを早期に検出できます。

`check_dir=True` を設定して、アプリ作成時に常にディレクトリをチェックすることもできます。

フロントエンドファイルが後で作成される場合、たとえばアプリオブジェクトの作成後に別のビルドステップで作成される場合は、`check_dir=False` を設定します。

{* ../../docs_src/frontend/tutorial006_py310.py hl[5] *}

`check_dir=False` を指定すると、**FastAPI** はアプリ作成時にディレクトリをチェックしません。リクエストが処理される時点で設定されたディレクトリがまだ存在しない場合、**FastAPI** はその時点でエラーを発生させます。

## `APIRouter` での使用 { #use-it-with-apirouter }

フロントエンドファイルを `APIRouter` に追加し、prefix 付きで include することもできます。

{* ../../docs_src/frontend/tutorial004_py310.py hl[6,7] *}

この例では、フロントエンドのパスは `/app` 配下で配信されます。

他の router 内のものを含め、アプリ内の通常の *path operations* は引き続き優先されます。

## 依存関係とミドルウェア { #dependencies-and-middleware }

フロントエンドのレスポンスは通常の **FastAPI** アプリケーション内で実行されるため、HTTP ミドルウェアが適用されます。

アプリ、`APIRouter`、および `include_router()` からの依存関係もフロントエンドのレスポンスに適用されます。これは、cookie 認証などでフロントエンドを保護する場合に役立ちます。

依存関係は、通常の *path operations* と同様に、レスポンスヘッダーを変更したりバックグラウンドタスクを追加したりすることもできます。

## 静的ビルド出力のみ { #static-build-output-only }

`app.frontend()` は、フロントエンドのビルドで既に生成されたファイルを配信します。

server-side rendering は実行しません。これは静的ファイルを生成するフロントエンドフレームワーク向けであり、各リクエストごとにサーバー上で動的レンダリングを必要とするフレームワーク向けではありません。
