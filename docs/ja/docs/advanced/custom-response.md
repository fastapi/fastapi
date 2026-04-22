# カスタムレスポンス - HTML、ストリーム、ファイル、その他 { #custom-response-html-stream-file-others }

デフォルトでは、**FastAPI** はJSONレスポンスを返します。

[レスポンスを直接返す](response-directly.md)で見たように、`Response` を直接返してこの挙動を上書きできます。

しかし、`Response`（または `JSONResponse` のような任意のサブクラス）を直接返す場合、（`response_model` を宣言していても）データは自動的に変換されず、ドキュメントも自動生成されません（例えば、生成されるOpenAPIの一部としてHTTPヘッダー `Content-Type` に特定の「メディアタイプ」を含めるなど）。

一方で、*path operation デコレータ* の `response_class` パラメータを使って、使用したい `Response`（`Response` の任意のサブクラス）を宣言することもできます。

*path operation 関数* から返したコンテンツは、その `Response` に格納されます。

/// note | 備考

メディアタイプを持たないレスポンスクラスを使用すると、FastAPIはレスポンスにコンテンツがないものと見なします。そのため、生成されるOpenAPIドキュメントにレスポンスフォーマットは記載されません。

///

## JSONレスポンス { #json-responses }

FastAPI はデフォルトでJSONレスポンスを返します。

[レスポンスモデル](../tutorial/response-model.md) を宣言すると、FastAPI は Pydantic を使ってデータをJSONにシリアライズします。

レスポンスモデルを宣言しない場合、FastAPI は [JSON Compatible Encoder](../tutorial/encoder.md) で説明した `jsonable_encoder` を使い、その結果を `JSONResponse` に入れます。

`JSONResponse` のようにJSONメディアタイプ（`application/json`）を持つ `response_class` を宣言した場合、*path operation デコレータ* に宣言した任意のPydanticの `response_model` に従って、返すデータは自動的に変換（およびフィルタ）されます。ただし、そのデータは Pydantic でJSONのバイト列にシリアライズされるわけではなく、まず `jsonable_encoder` で変換された後に `JSONResponse` クラスへ渡され、Pythonの標準JSONライブラリでバイト列にシリアライズされます。

### JSONのパフォーマンス { #json-performance }

結論として、最大のパフォーマンスを得たい場合は、[レスポンスモデル](../tutorial/response-model.md) を使い、*path operation デコレータ* で `response_class` は宣言しないでください。

{* ../../docs_src/response_model/tutorial001_01_py310.py ln[15:17] hl[16] *}

## HTMLレスポンス { #html-response }

**FastAPI** からHTMLを直接返すには、`HTMLResponse` を使います。

* `HTMLResponse` をインポートする
* *path operation デコレータ* のパラメータ `response_class` に `HTMLResponse` を渡す

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | 情報

パラメータ `response_class` は、レスポンスの「メディアタイプ」を定義するためにも使用されます。

この場合、HTTPヘッダー `Content-Type` には `text/html` が設定されます。

そして、OpenAPIにもそのようにドキュメント化されます。

///

### `Response` を返す { #return-a-response }

[レスポンスを直接返す](response-directly.md)で見たように、*path operation* の中でレスポンスを直接返して上書きすることもできます。

上記と同じ例で、`HTMLResponse` を返すと次のようになります:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | 注意

*path operation 関数* から直接返される `Response` は、OpenAPIにドキュメント化されず（例えば `Content-Type` がドキュメント化されない）、自動生成の対話的ドキュメントにも表示されません。

///

/// info | 情報

もちろん、実際の `Content-Type` ヘッダーやステータスコードなどは、返した `Response` オブジェクトに由来します。

///

### OpenAPIにドキュメント化しつつ `Response` を上書き { #document-in-openapi-and-override-response }

関数の中からレスポンスを上書きしつつ、同時にOpenAPIで「メディアタイプ」をドキュメント化したい場合は、`response_class` パラメータを使用し、かつ `Response` オブジェクトを返します。

この場合、`response_class` はOpenAPIの *path operation* をドキュメント化するためだけに使われ、実際には返した `Response` がそのまま使用されます。

#### `HTMLResponse` を直接返す { #return-an-htmlresponse-directly }

例えば、次のようになります:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

この例では、関数 `generate_html_response()` はHTMLの `str` を返すのではなく、すでに `Response` を生成して返しています。

`generate_html_response()` の呼び出し結果を返すことで、デフォルトの **FastAPI** の挙動を上書きする `Response` をすでに返しています。

しかし、`response_class` にも `HTMLResponse` を渡しているため、**FastAPI** はOpenAPIおよび対話的ドキュメントで、それが `text/html` のHTMLであると正しくドキュメント化できます:

<img src="/img/tutorial/custom-response/image01.png">

## 利用可能なレスポンス { #available-responses }

以下は利用可能なレスポンスの一部です。

`Response` を使って他のものを返したり、カスタムサブクラスを作成することもできます。

/// note | 技術詳細

`from starlette.responses import HTMLResponse` を使うこともできます。

**FastAPI** は開発者の利便性のために、`starlette.responses` と同じものを `fastapi.responses` として提供しています。ただし、利用可能なレスポンスの多くはStarletteから直接提供されています。

///

### `Response` { #response }

メインの `Response` クラスで、他のすべてのレスポンスはこれを継承しています。

直接返すことができます。

以下のパラメータを受け付けます。

* `content` - `str` または `bytes`
* `status_code` - `int` のHTTPステータスコード
* `headers` - 文字列の `dict`
* `media_type` - メディアタイプを示す `str`。例: `"text/html"`

FastAPI（実際にはStarlette）は自動的に Content-Length ヘッダーを含めます。また、`media_type` に基づいた Content-Type ヘッダーを含め、テキストタイプには charset を追加します。

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

上で読んだように、テキストやバイト列を受け取り、HTMLレスポンスを返します。

### `PlainTextResponse` { #plaintextresponse }

テキストやバイト列を受け取り、プレーンテキストのレスポンスを返します。

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

データを受け取り、`application/json` としてエンコードされたレスポンスを返します。

これは、上で述べたように **FastAPI** のデフォルトのレスポンスです。

/// note | 技術詳細

ただし、レスポンスモデルや返却型を宣言した場合は、それが直接データのJSONシリアライズに使われ、適切なJSONのメディアタイプを持つレスポンスが `JSONResponse` クラスを使わずに直接返されます。

これが最適なパフォーマンスを得る理想的な方法です。

///

### `RedirectResponse` { #redirectresponse }

HTTPリダイレクトを返します。デフォルトでは307ステータスコード（Temporary Redirect）を使用します。

`RedirectResponse` を直接返せます:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

または、`response_class` パラメータで使用できます:

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

その場合、*path operation* 関数からURLを直接返せます。

この場合に使用される `status_code` は、`RedirectResponse` のデフォルトである `307` になります。

---

さらに、`status_code` パラメータを `response_class` パラメータと組み合わせて使うこともできます:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

非同期ジェネレータ、または通常のジェネレータ/イテレータ（`yield` を持つ関数）を受け取り、レスポンスボディをストリームします。

{* ../../docs_src/custom_response/tutorial007_py310.py hl[3,16] *}

/// note | 技術詳細

`async` タスクは `await` に到達したときにのみキャンセルできます。`await` がない場合、ジェネレータ（`yield` を持つ関数）は適切にキャンセルできず、キャンセル要求後も実行が続く可能性があります。

この小さな例では `await` が不要なため、イベントループにキャンセルを処理する機会を与えるために `await anyio.sleep(0)` を追加しています。

これは大きなストリームや無限ストリームではさらに重要になります。

///

/// tip | 豆知識

`StreamingResponse` を直接返す代わりに、[データをストリームする](./stream-data.md) スタイルに従うことをおすすめします。こちらのほうがはるかに便利で、裏側でキャンセル処理も行ってくれます。

JSON Lines をストリームする場合は、[JSON Lines をストリームする](../tutorial/stream-json-lines.md) チュートリアルを参照してください。

///

### `FileResponse` { #fileresponse }

ファイルをレスポンスとして非同期にストリームします。

他のレスポンスタイプとは異なる引数セットでインスタンス化します:

* `path` - ストリームするファイルのファイルパス
* `headers` - 含めたい任意のカスタムヘッダー（辞書）
* `media_type` - メディアタイプを示す文字列。未設定の場合、ファイル名やパスから推測されます
* `filename` - 設定した場合、レスポンスの `Content-Disposition` に含まれます

ファイルレスポンスには、適切な `Content-Length`、`Last-Modified`、`ETag` ヘッダーが含まれます。

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

`response_class` パラメータを使うこともできます:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

この場合、*path operation* 関数からファイルパスを直接返せます。

## カスタムレスポンスクラス { #custom-response-class }

`Response` を継承して、独自のカスタムレスポンスクラスを作成し、使用できます。

例えば、[`orjson`](https://github.com/ijl/orjson) を特定の設定で使いたいとします。

インデントされた整形済みJSONを返したいので、orjson のオプション `orjson.OPT_INDENT_2` を使いたいとします。

`CustomORJSONResponse` を作成できます。主に必要なのは、`bytes` を返す `Response.render(content)` メソッドを作ることです:

{* ../../docs_src/custom_response/tutorial009c_py310.py hl[9:14,17] *}

これまでは次のように返していたものが:

```json
{"message": "Hello World"}
```

...このレスポンスでは次のように返されます:

```json
{
  "message": "Hello World"
}
```

もちろん、JSONの整形以外にも、これを活用するもっと良い方法が見つかるはずです。 😉

### `orjson` か レスポンスモデルか { #orjson-or-response-model }

もし求めているのがパフォーマンスであれば、`orjson` レスポンスを使うより、[レスポンスモデル](../tutorial/response-model.md) を使うほうが良い場合が多いです。

レスポンスモデルがあると、FastAPI は中間ステップ（他の場合に行われる `jsonable_encoder` による変換など）を介さずに、Pydantic を使ってデータをJSONにシリアライズします。

内部的には、Pydantic はJSONシリアライズに `orjson` と同じRust由来の仕組みを用いているため、レスポンスモデルを使うだけで最良のパフォーマンスが得られます。

## デフォルトレスポンスクラス { #default-response-class }

**FastAPI** クラスのインスタンスや `APIRouter` を作成する際に、デフォルトで使用するレスポンスクラスを指定できます。

これを定義するパラメータは `default_response_class` です。

以下の例では、**FastAPI** はすべての *path operation* で、JSONの代わりにデフォルトで `HTMLResponse` を使用します。

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | 豆知識

これまでと同様に、*path operation* ごとに `response_class` をオーバーライドできます。

///

## その他のドキュメント { #additional-documentation }

OpenAPIでは `responses` を使ってメディアタイプやその他の詳細を宣言することもできます: [OpenAPI の追加レスポンス](additional-responses.md)。
