# ミドルウェア { #middleware }

**FastAPI** アプリケーションにミドルウェアを追加できます。

「ミドルウェア」は、すべての**リクエスト**に対して、それがあらゆる特定の*path operation*によって処理される前に機能する関数です。また、すべての**レスポンス**に対して、それを返す前に機能します。

* ミドルウェアはアプリケーションに届いたそれぞれの**リクエスト**を受け取ります。
* その後、その**リクエスト**に対して何かを実行したり、必要なコードを実行したりできます。
* 次に、アプリケーションの残りの部分に**リクエスト**を渡して (*path operation* によって) 処理させます。
* 次に、ミドルウェアはアプリケーション (の *path operation*) によって生成された**レスポンス**を受け取ります。
* その**レスポンス**に対して何かを実行したり、必要なコードを実行したりできます。
* そして、**レスポンス**を返します。

/// note | 技術詳細

`yield` を使った依存関係をもつ場合は、終了コードはミドルウェアの *後に* 実行されます。

バックグラウンドタスク ([バックグラウンドタスク](background-tasks.md){.internal-link target=_blank} セクションで説明します。後で確認できます) がある場合は、それらは全てのミドルウェアの *後に* 実行されます。

///

## ミドルウェアの作成 { #create-a-middleware }

ミドルウェアを作成するには、関数の上部でデコレータ `@app.middleware("http")` を使用します。

ミドルウェア関数は以下を受け取ります:

* `request`。
* パラメータとして `request` を受け取る関数 `call_next`。
    * この関数は、対応する*path operation*に `request` を渡します。
    * 次に、対応する*path operation*によって生成された `response` を返します。
* その後、`response` を返す前にさらに `response` を変更することもできます。

{* ../../docs_src/middleware/tutorial001_py310.py hl[8:9,11,14] *}

/// tip | 豆知識

カスタムの独自ヘッダーは <a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers" class="external-link" target="_blank">`X-` プレフィックスを使用</a>して追加できる点に注意してください。

ただし、ブラウザのクライアントに表示させたいカスタムヘッダーがある場合は、<a href="https://www.starlette.dev/middleware/#corsmiddleware" class="external-link" target="_blank">StarletteのCORSドキュメント</a>に記載されているパラメータ `expose_headers` を使用して、それらをCORS設定に追加する必要があります ([CORS (Cross-Origin Resource Sharing)](cors.md){.internal-link target=_blank})。

///

/// note | 技術詳細

`from starlette.requests import Request` を使用することもできます。

**FastAPI**は、開発者の便利のためにこれを提供していますが、Starletteから直接きています。

///

### `response` の前後 { #before-and-after-the-response }

*path operation* が `request` を受け取る前に、 `request` とともに実行されるコードを追加できます。

また `response` が生成された後、それを返す前にも追加できます。

例えば、リクエストの処理とレスポンスの生成にかかった秒数を含むカスタムヘッダー `X-Process-Time` を追加できます:

{* ../../docs_src/middleware/tutorial001_py310.py hl[10,12:13] *}

/// tip | 豆知識

ここでは、これらのユースケースに対してより正確になり得るため、`time.time()` の代わりに <a href="https://docs.python.org/3/library/time.html#time.perf_counter" class="external-link" target="_blank">`time.perf_counter()`</a> を使用しています。 🤓

///

## 複数ミドルウェアの実行順序 { #multiple-middleware-execution-order }

`@app.middleware()` デコレータまたは `app.add_middleware()` メソッドのいずれかを使って複数のミドルウェアを追加すると、新しく追加された各ミドルウェアがアプリケーションをラップし、スタックを形成します。最後に追加されたミドルウェアが *最も外側*、最初に追加されたミドルウェアが *最も内側* になります。

リクエスト経路では、*最も外側* のミドルウェアが最初に実行されます。

レスポンス経路では、最後に実行されます。

例:

```Python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

これにより、実行順序は次のようになります:

* **リクエスト**: MiddlewareB → MiddlewareA → route

* **レスポンス**: route → MiddlewareA → MiddlewareB

このスタック動作により、ミドルウェアが予測可能で制御しやすい順序で実行されることが保証されます。

## その他のミドルウェア { #other-middlewares }

他のミドルウェアの詳細については、[高度なユーザーガイド: 高度なミドルウェア](../advanced/middleware.md){.internal-link target=_blank}を参照してください。

次のセクションでは、ミドルウェアを使用して <abbr title="Cross-Origin Resource Sharing - クロスオリジンリソース共有">CORS</abbr> を処理する方法について説明します。
