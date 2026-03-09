# カスタム Request と APIRoute クラス { #custom-request-and-apiroute-class }

場合によっては、`Request` や `APIRoute` クラスで使われるロジックを上書きしたいことがあります。

特に、ミドルウェアでのロジックの代替として有効な場合があります。

たとえば、アプリケーションで処理される前にリクエストボディを読み取ったり操作したりしたい場合です。

/// danger | 警告

これは「上級」機能です。

FastAPI を始めたばかりの場合は、このセクションは読み飛ばしてもよいでしょう。

///

## ユースケース { #use-cases }

ユースケースの例:

* JSON ではないリクエストボディを JSON に変換する（例: <a href="https://msgpack.org/index.html" class="external-link" target="_blank">`msgpack`</a>）。
* gzip 圧縮されたリクエストボディの解凍。
* すべてのリクエストボディの自動ロギング。

## カスタムリクエストボディのエンコーディングの処理 { #handling-custom-request-body-encodings }

gzip のリクエストを解凍するために、カスタムの `Request` サブクラスを使う方法を見ていきます。

そして、そのカスタムリクエストクラスを使うための `APIRoute` サブクラスを用意します。

### カスタム `GzipRequest` クラスの作成 { #create-a-custom-gziprequest-class }

/// tip | 豆知識

これは仕組みを示すためのサンプルです。Gzip 対応が必要な場合は、用意されている [`GzipMiddleware`](../advanced/middleware.md#gzipmiddleware){.internal-link target=_blank} を使用できます。

///

まず、`GzipRequest` クラスを作成します。これは適切なヘッダーがある場合に本体を解凍するよう、`Request.body()` メソッドを上書きします。

ヘッダーに `gzip` がなければ、解凍は試みません。

この方法により、同じルートクラスで gzip 圧縮済み／未圧縮のリクエストの両方を扱えます。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[9:16] *}

### カスタム `GzipRoute` クラスの作成 { #create-a-custom-gziproute-class }

次に、`GzipRequest` を利用する `fastapi.routing.APIRoute` のカスタムサブクラスを作成します。

ここでは `APIRoute.get_route_handler()` メソッドを上書きします。

このメソッドは関数を返します。そしてその関数がリクエストを受け取り、レスポンスを返します。

ここでは、元のリクエストから `GzipRequest` を作成するために利用します。

{* ../../docs_src/custom_request_and_route/tutorial001_an_py310.py hl[19:27] *}

/// note | 技術詳細

`Request` には `request.scope` 属性があり、これはリクエストに関するメタデータを含む Python の `dict` です。

`Request` には `request.receive` もあり、これはリクエストの本体を「受信」するための関数です。

`scope` の `dict` と `receive` 関数はいずれも ASGI 仕様の一部です。

そしてこの 2 つ（`scope` と `receive`）が、新しい `Request` インスタンスを作成するために必要なものです。

`Request` について詳しくは、<a href="https://www.starlette.dev/requests/" class="external-link" target="_blank">Starlette の Requests に関するドキュメント</a> を参照してください。

///

`GzipRequest.get_route_handler` が返す関数が異なるのは、`Request` を `GzipRequest` に変換する点だけです。

これにより、`GzipRequest` は必要に応じてデータを解凍してから *path operations* に渡します。

それ以降の処理ロジックはすべて同じです。

ただし、`GzipRequest.body` を変更しているため、必要に応じて **FastAPI** によって読み込まれる際にリクエストボディが自動的に解凍されます。

## 例外ハンドラでのリクエストボディへのアクセス { #accessing-the-request-body-in-an-exception-handler }

/// tip | 豆知識

同じ問題を解決するには、`RequestValidationError` 用のカスタムハンドラで `body` を使う方がずっと簡単でしょう（[エラー処理](../tutorial/handling-errors.md#use-the-requestvalidationerror-body){.internal-link target=_blank}）。

ただし、この例も有効で、内部コンポーネントとどのようにやり取りするかを示しています。

///

同じアプローチを使って、例外ハンドラ内でリクエストボディにアクセスすることもできます。

やることは、`try`/`except` ブロックの中でリクエストを処理するだけです：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[14,16] *}

例外が発生しても、`Request` インスタンスはスコープ内に残るため、エラー処理時にリクエストボディを読み取り、活用できます：

{* ../../docs_src/custom_request_and_route/tutorial002_an_py310.py hl[17:19] *}

## ルーターでのカスタム `APIRoute` クラス { #custom-apiroute-class-in-a-router }

`APIRouter` の `route_class` パラメータを設定することもできます：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[26] *}

この例では、`router` 配下の *path operations* はカスタムの `TimedRoute` クラスを使用し、レスポンスの生成にかかった時間を示す追加の `X-Response-Time` ヘッダーがレスポンスに含まれます：

{* ../../docs_src/custom_request_and_route/tutorial003_py310.py hl[13:20] *}
