# カスタムレスポンス - HTML、ストリーム、ファイル、その他のレスポンス { #custom-response-html-stream-file-others }

デフォルトでは、**FastAPI** は `JSONResponse` を使ってレスポンスを返します。

[レスポンスを直接返す](response-directly.md){.internal-link target=_blank}で見たように、 `Response` を直接返すことでこの挙動をオーバーライドできます。

しかし、`Response` を直接返すと（または `JSONResponse` のような任意のサブクラスを返すと）、データは自動的に変換されず（`response_model` を宣言していても）、ドキュメントも自動生成されません（例えば、生成されるOpenAPIの一部としてHTTPヘッダー `Content-Type` に特定の「メディアタイプ」を含めるなど）。

`response_class` パラメータを使用して、*path operation デコレータ* で使用したい `Response`（任意の `Response` サブクラス）を宣言することもできます。

*path operation 関数* から返されるコンテンツは、その `Response` に含まれます。

そしてその `Response` が、`JSONResponse` や `UJSONResponse` の場合のようにJSONメディアタイプ（`application/json`）なら、関数の返り値は *path operationデコレータ* に宣言した任意のPydantic `response_model` により自動的に変換（およびフィルタ）されます。

/// note | 備考

メディアタイプを指定せずにレスポンスクラスを利用すると、FastAPIはレスポンスにコンテンツがないことを期待します。そのため、生成されるOpenAPIドキュメントにレスポンスフォーマットが記載されません。

///

## `ORJSONResponse` を使う { #use-orjsonresponse }

例えば、パフォーマンスを絞り出したい場合は、<a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>をインストールし、レスポンスとして `ORJSONResponse` をセットできます。

使いたい `Response` クラス（サブクラス）をインポートし、*path operationデコレータ* に宣言します。

大きなレスポンスの場合、`Response` を直接返すほうが、辞書を返すよりもはるかに高速です。

これは、デフォルトではFastAPIがチュートリアルで説明した同じ[JSON Compatible Encoder](../tutorial/encoder.md){.internal-link target=_blank}を使って、内部の各アイテムを検査し、JSONとしてシリアライズ可能であることを確認するためです。これにより、例えばデータベースモデルのような**任意のオブジェクト**を返せます。

しかし、返そうとしているコンテンツが **JSONでシリアライズ可能**であることが確実なら、それを直接レスポンスクラスに渡して、FastAPIがレスポンスクラスへ渡す前に返却コンテンツを `jsonable_encoder` に通すことで発生する追加のオーバーヘッドを回避できます。

{* ../../docs_src/custom_response/tutorial001b_py310.py hl[2,7] *}

/// info | 情報

パラメータ `response_class` は、レスポンスの「メディアタイプ」を定義するためにも利用されます。

この場合、HTTPヘッダー `Content-Type` には `application/json` がセットされます。

そして、OpenAPIにはそのようにドキュメントされます。

///

/// tip | 豆知識

`ORJSONResponse` はFastAPIでのみ利用可能で、Starletteでは利用できません。

///

## HTMLレスポンス { #html-response }

**FastAPI** からHTMLを直接返す場合は、`HTMLResponse` を使います。

* `HTMLResponse` をインポートする。
* *path operation デコレータ* のパラメータ `response_class` に `HTMLResponse` を渡す。

{* ../../docs_src/custom_response/tutorial002_py310.py hl[2,7] *}

/// info | 情報

パラメータ `response_class` は、レスポンスの「メディアタイプ」を定義するためにも利用されます。

この場合、HTTPヘッダー `Content-Type` には `text/html` がセットされます。

そして、OpenAPIにはそのようにドキュメントされます。

///

### `Response` を返す { #return-a-response }

[レスポンスを直接返す](response-directly.md){.internal-link target=_blank}で見たように、レスポンスを返すことで、*path operation* の中でレスポンスを直接オーバーライドすることもできます。

上記と同じ例において、 `HTMLResponse` を返すと、このようになります:

{* ../../docs_src/custom_response/tutorial003_py310.py hl[2,7,19] *}

/// warning | 注意

*path operation関数* から直接返される `Response` は、OpenAPIにドキュメントされず（例えば、`Content-Type` がドキュメントされない）、自動的な対話的ドキュメントでも表示されません。

///

/// info | 情報

もちろん、実際の `Content-Type` ヘッダーやステータスコードなどは、返された `Response` オブジェクトに由来します。

///

### OpenAPIドキュメントと `Response` のオーバーライド { #document-in-openapi-and-override-response }

関数の中でレスポンスをオーバーライドしつつも、OpenAPI に「メディアタイプ」をドキュメント化したいなら、`response_class` パラメータを使用し、かつ `Response` オブジェクトを返します。

`response_class` はOpenAPIの*path operation*のドキュメント化のためにのみ使用され、`Response` はそのまま使用されます。

#### `HTMLResponse` を直接返す { #return-an-htmlresponse-directly }

例えば、このようになります:

{* ../../docs_src/custom_response/tutorial004_py310.py hl[7,21,23] *}

この例では、関数 `generate_html_response()` は、`str` のHTMLを返すのではなく、`Response` を生成して返しています。

`generate_html_response()` を呼び出した結果を返すことにより、デフォルトの **FastAPI** の挙動をオーバーライドする `Response` をすでに返しています。

しかし、`response_class` にも `HTMLResponse` を渡しているため、**FastAPI** はOpenAPIと対話的ドキュメントで、`text/html` のHTMLとしてどのようにドキュメント化すればよいかを理解できます:

<img src="/img/tutorial/custom-response/image01.png">

## 利用可能なレスポンス { #available-responses }

以下が利用可能なレスポンスの一部です。

`Response` を使って他の何かを返せますし、カスタムのサブクラスも作れることを覚えておいてください。

/// note | 技術詳細

`from starlette.responses import HTMLResponse` も利用できます。

**FastAPI** は開発者の利便性のために、`starlette.responses` と同じものを `fastapi.responses` として提供しています。しかし、利用可能なレスポンスのほとんどはStarletteから直接提供されます。

///

### `Response` { #response }

メインの `Response` クラスで、他の全てのレスポンスはこれを継承しています。

直接返すことができます。

以下のパラメータを受け付けます。

* `content` - `str` か `bytes`。
* `status_code` - `int` のHTTPステータスコード。
* `headers` - 文字列の `dict` 。
* `media_type` - メディアタイプを示す `str` 。例えば `"text/html"` 。

FastAPI（実際にはStarlette）は自動的にContent-Lengthヘッダーを含みます。また、`media_type` に基づいたContent-Typeヘッダーを含み、テキストタイプのためにcharsetを追加します。

{* ../../docs_src/response_directly/tutorial002_py310.py hl[1,18] *}

### `HTMLResponse` { #htmlresponse }

上で読んだように、テキストやバイトを受け取り、HTMLレスポンスを返します。

### `PlainTextResponse` { #plaintextresponse }

テキストやバイトを受け取り、プレーンテキストのレスポンスを返します。

{* ../../docs_src/custom_response/tutorial005_py310.py hl[2,7,9] *}

### `JSONResponse` { #jsonresponse }

データを受け取り、`application/json` としてエンコードされたレスポンスを返します。

上で読んだように、**FastAPI** のデフォルトのレスポンスとして利用されます。

### `ORJSONResponse` { #orjsonresponse }

上で読んだように、<a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>を使った、高速な代替のJSONレスポンスです。

/// info | 情報

これは、例えば `pip install orjson` で `orjson` をインストールする必要があります。

///

### `UJSONResponse` { #ujsonresponse }

<a href="https://github.com/ultrajson/ultrajson" class="external-link" target="_blank">`ujson`</a>を使った、代替のJSONレスポンスです。

/// info | 情報

これは、例えば `pip install ujson` で `ujson` をインストールする必要があります。

///

/// warning | 注意

`ujson` は、いくつかのエッジケースの取り扱いについて、Pythonにビルトインされた実装ほど注意深くありません。

///

{* ../../docs_src/custom_response/tutorial001_py310.py hl[2,7] *}

/// tip | 豆知識

`ORJSONResponse` のほうが高速な代替かもしれません。

///

### `RedirectResponse` { #redirectresponse }

HTTPリダイレクトを返します。デフォルトでは307ステータスコード（Temporary Redirect）となります。

`RedirectResponse` を直接返せます:

{* ../../docs_src/custom_response/tutorial006_py310.py hl[2,9] *}

---

または、`response_class` パラメータで使用できます:

{* ../../docs_src/custom_response/tutorial006b_py310.py hl[2,7,9] *}

その場合、*path operation*関数からURLを直接返せます。

この場合に使用される `status_code` は `RedirectResponse` のデフォルトである `307` になります。

---

また、`status_code` パラメータを `response_class` パラメータと組み合わせて使うこともできます:

{* ../../docs_src/custom_response/tutorial006c_py310.py hl[2,7,9] *}

### `StreamingResponse` { #streamingresponse }

非同期ジェネレータ、または通常のジェネレータ/イテレータを受け取り、レスポンスボディをストリームします。

{* ../../docs_src/custom_response/tutorial007_py310.py hl[2,14] *}

#### ファイルライクオブジェクトで `StreamingResponse` を使う { #using-streamingresponse-with-file-like-objects }

<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> オブジェクト（例: `open()` で返されるオブジェクト）がある場合、そのfile-likeオブジェクトを反復処理するジェネレータ関数を作れます。

そうすれば、最初にすべてをメモリへ読み込む必要はなく、そのジェネレータ関数を `StreamingResponse` に渡して返せます。

これにはクラウドストレージとの連携、映像処理など、多くのライブラリが含まれます。

{* ../../docs_src/custom_response/tutorial008_py310.py hl[2,10:12,14] *}

1. これはジェネレータ関数です。内部に `yield` 文を含むため「ジェネレータ関数」です。
2. `with` ブロックを使うことで、ジェネレータ関数が終わった後（つまりレスポンスの送信が完了した後）にfile-likeオブジェクトが確実にクローズされるようにします。
3. この `yield from` は、`file_like` という名前のものを反復処理するように関数へ指示します。そして反復された各パートについて、そのパートをこのジェネレータ関数（`iterfile`）から来たものとして `yield` します。

    つまり、内部的に「生成」の作業を別のものへ移譲するジェネレータ関数です。

    このようにすることで `with` ブロックに入れられ、完了後にfile-likeオブジェクトが確実にクローズされます。

/// tip | 豆知識

ここでは `async` と `await` をサポートしていない標準の `open()` を使っているため、通常の `def` でpath operationを宣言している点に注意してください。

///

### `FileResponse` { #fileresponse }

レスポンスとしてファイルを非同期的にストリームします。

他のレスポンスタイプとは異なる引数のセットを受け取りインスタンス化します。

* `path` - ストリームするファイルのファイルパス。
* `headers` - 含めたい任意のカスタムヘッダーの辞書。
* `media_type` - メディアタイプを示す文字列。未設定の場合、ファイル名やパスからメディアタイプが推測されます。
* `filename` - 設定した場合、レスポンスの `Content-Disposition` に含まれます。

ファイルレスポンスには、適切な `Content-Length`、`Last-Modified`、`ETag` ヘッダーが含まれます。

{* ../../docs_src/custom_response/tutorial009_py310.py hl[2,10] *}

`response_class` パラメータを使うこともできます:

{* ../../docs_src/custom_response/tutorial009b_py310.py hl[2,8,10] *}

この場合、*path operation*関数からファイルパスを直接返せます。

## カスタムレスポンスクラス { #custom-response-class }

`Response` を継承した独自のカスタムレスポンスクラスを作成して利用できます。

例えば、<a href="https://github.com/ijl/orjson" class="external-link" target="_blank">`orjson`</a>を使いたいが、同梱の `ORJSONResponse` クラスで使われていないカスタム設定も使いたいとします。

例えば、インデントされ整形されたJSONを返したいので、orjsonオプション `orjson.OPT_INDENT_2` を使いたいとします。

`CustomORJSONResponse` を作れます。主に必要なのは、コンテンツを `bytes` として返す `Response.render(content)` メソッドを作ることです:

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

もちろん、JSONの整形よりも、これを活用するもっと良い方法が見つかるはずです。 😉

## デフォルトレスポンスクラス { #default-response-class }

**FastAPI** クラスのインスタンス、または `APIRouter` を作成する際に、デフォルトで使用するレスポンスクラスを指定できます。

これを定義するパラメータは `default_response_class` です。

以下の例では、**FastAPI** はすべての*path operation*で、`JSONResponse` の代わりに `ORJSONResponse` をデフォルトとして使います。

{* ../../docs_src/custom_response/tutorial010_py310.py hl[2,4] *}

/// tip | 豆知識

これまでと同様に、*path operation*で `response_class` をオーバーライドできます。

///

## その他のドキュメント { #additional-documentation }

OpenAPIでは `responses` を使ってメディアタイプやその他の詳細を宣言することもできます: [Additional Responses in OpenAPI](additional-responses.md){.internal-link target=_blank}。
