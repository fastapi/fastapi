<p align="center">
  <a href="https://fastapi.tiangolo.com"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI framework, high performance, easy to learn, fast to code, ready for production</em>
</p>
<p align="center">
<a href="https://travis-ci.com/tiangolo/fastapi" target="_blank">
    <img src="https://travis-ci.com/tiangolo/fastapi.svg?branch=master" alt="Build Status">
</a>
<a href="https://codecov.io/gh/tiangolo/fastapi" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/tiangolo/fastapi" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://badge.fury.io/py/fastapi.svg" alt="Package version">
</a>
<a href="https://gitter.im/tiangolo/fastapi?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge" target="_blank">
    <img src="https://badges.gitter.im/tiangolo/fastapi.svg" alt="Join the chat at https://gitter.im/tiangolo/fastapi">
</a>
</p>

---

**ドキュメント**: <a href="https://fastapi.tiangolo.com" target="_blank">https://fastapi.tiangolo.com</a>

**ソースコード**: <a href="https://github.com/tiangolo/fastapi" target="_blank">https://github.com/tiangolo/fastapi</a>

---

FastAPI は、モダンで、速い(高いパフォーマンスな)、標準の Python 型ヒントに基づいて、Python 3.6 以降のバージョンで API をビルドするための Web フレームワークです。

主な特徴:

- **高速**: **NodeJS** や **Go** 並みのとても高いパフォーマンス (Starlette と Pydantic のおかげです)。 [最も高速な Python フレームワークの一つです](#performance).

- **高速なコーディング**: 開発速度を約 200%~300%向上させます。 \*
- **少ないバグ**: 開発者起因のヒューマンエラーを約 40％削減します。 \*
- **直感的**: 素晴らしいエディタのサポートや <abbr title="also known as auto-complete, autocompletion, IntelliSense">オートコンプリート。</abbr> デバッグ時間を削減します。
- **簡単**: 簡単に利用、習得できるようにデザインされています。ドキュメントを読む時間を削減します。
- **短い**: コードの重複を最小限にしています。各パラメータからの複数の機能。少ないバグ。
- **堅牢性**: 自動対話ドキュメントを使用して、本番環境で使用できるコードを取得します。
- **Standards-based**: API のオープンスタンダードに基づいており、完全に互換性があります: <a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a> (以前は Swagger として知られていました) や <a href="http://json-schema.org/" class="external-link" target="_blank">JSON スキーマ</a>.

<small>\* 社内開発チームでのテストに基づき見積もってから、本番アプリケーションの構築します。</small>

## 評価

"_[...] 最近 **FastAPI** を使っています。 [...] 実際に私のチームの全ての **Microsoft の機械学習サービス** で使用する予定です。 そのうちのいくつかのコアな**Windows**製品と**Office**製品に統合されつつあります。_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/tiangolo/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_FastAPI ライブラリを採用して**REST**サーバを構築し、それをクエリして**予測**を取得しています。 [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** Netflix は、**危機管理**オーケストレーションフレームワーク、**Dispatch**のオープンソースリリースを発表できることをうれしく思います。 [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_私は**FastAPI**にワクワクしています。 めちゃくちゃ楽しいです！_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://twitter.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_正直、超堅実で洗練されているように見えます。いろんな意味で、それは私がハグしたかったものです。_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="http://www.hug.rest/" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_REST API を構築するための**モダンなフレームワーク**を学びたい方は、\*\*FastAPI＊＊をチェックしてみてください。 [...] 高速で, 使用、習得が簡単です。[...]_"

"_私たちの**API**は**FastAPI**に切り替えました。[...] きっと気に入ると思います。 [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://twitter.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://twitter.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

## **Typer**, the FastAPI of CLIs

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

もし Web API の代わりにターミナルで使用する<abbr title="Command Line Interface">CLI</abbr>アプリを構築する場合は、<a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a>を確認してください。

**Typer**は FastAPI の兄弟です。そして、**CLI の FastAPI**を意図しています。

## 必要条件

Python 3.6+

FastAPI は巨人の肩の上に立っています。

- Web の部分のための<a href="https://www.starlette.io/" class="external-link" target="_blank">Starlette</a>
- データの部分のための<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>

## インストール

<div class="termy">

```console
$ pip install fastapi

---> 100%
```

</div>

<a href="http://www.uvicorn.org" class="external-link" target="_blank">Uvicorn</a> または、 <a href="https://gitlab.com/pgjones/hypercorn" class="external-link" target="_blank">Hypercorn</a>のように、本番環境では ASGI サーバーが必要になります。

<div class="termy">

```console
$ pip install uvicorn

---> 100%
```

</div>

## アプリケーション例

### アプリケーションの作成

- `main.py` を作成し、以下のコードを入力します:

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>または<code>async def</code>を使います...</summary>

`async` / `await`を使用するときは、 `async def`を使います:

```Python hl_lines="7 12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}
```

**注**:

<a href="https://fastapi.tiangolo.com/async/#in-a-hurry" target="_blank">ドキュメントの`async` と `await`</a>についてわからない場合は、"In a hurry?"セクションをチェックしてください。

</details>

### 実行

以下のコマンドでサーバーを起動します:

<div class="termy">

```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary><code>uvicorn main:app --reload</code>コマンドについて</summary>

`uvicorn main:app`コマンドは以下の項目を参照します:

- `main`: `main.py`ファイル (Python "モジュール")
- `app`: `main.py` の`app = FastAPI()`の行で生成されたオブジェクト
- `--reload`: コードを変更したらサーバーを再起動します。このオプションは開発環境でのみ使用します

</details>

### 動作確認

ブラウザから<a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a>を開きます。

以下の JSON のレスポンスが確認できます:

```JSON
{"item_id": 5, "q": "somequery"}
```

もうすでに以下の API が作成されています:

- Receives HTTP requests in the _paths_ `/` and `/items/{item_id}`.
- Both _paths_ take `GET` <em>operations</em> (also known as HTTP _methods_).
- The _path_ `/items/{item_id}` has a _path parameter_ `item_id` that should be an `int`.
- The _path_ `/items/{item_id}` has an optional `str` _query parameter_ `q`.

### Interactive API docs

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

You will see the automatic interactive API documentation (provided by <a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### Alternative API docs

And now, go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

You will see the alternative automatic documentation (provided by <a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## Example upgrade

Now modify the file `main.py` to receive a body from a `PUT` request.

Declare the body using standard Python types, thanks to Pydantic.

```Python hl_lines="2  7 8 9 10  23 24 25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

The server should reload automatically (because you added `--reload` to the `uvicorn` command above).

### Interactive API docs upgrade

Now go to <a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>.

- The interactive API documentation will be automatically updated, including the new body:

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

- Click on the button "Try it out", it allows you to fill the parameters and directly interact with the API:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

- Then click on the "Execute" button, the user interface will communicate with your API, send the parameters, get the results and show them on the screen:

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### Alternative API docs upgrade

And now, go to <a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>.

- The alternative documentation will also reflect the new query parameter and body:

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### Recap

In summary, you declare **once** the types of parameters, body, etc. as function parameters.

You do that with standard modern Python types.

You don't have to learn a new syntax, the methods or classes of a specific library, etc.

Just standard **Python 3.6+**.

For example, for an `int`:

```Python
item_id: int
```

or for a more complex `Item` model:

```Python
item: Item
```

...and with that single declaration you get:

- Editor support, including:
  - Completion.
  - Type checks.
- Validation of data:
  - Automatic and clear errors when the data is invalid.
  - Validation even for deeply nested JSON objects.
- <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> of input data: coming from the network to Python data and types. Reading from:
  - JSON.
  - Path parameters.
  - Query parameters.
  - Cookies.
  - Headers.
  - Forms.
  - Files.
- <abbr title="also known as: serialization, parsing, marshalling">Conversion</abbr> of output data: converting from Python data and types to network data (as JSON):
  - Convert Python types (`str`, `int`, `float`, `bool`, `list`, etc).
  - `datetime` objects.
  - `UUID` objects.
  - Database models.
  - ...and many more.
- Automatic interactive API documentation, including 2 alternative user interfaces:
  - Swagger UI.
  - ReDoc.

---

Coming back to the previous code example, **FastAPI** will:

- Validate that there is an `item_id` in the path for `GET` and `PUT` requests.
- Validate that the `item_id` is of type `int` for `GET` and `PUT` requests.
  - If it is not, the client will see a useful, clear error.
- Check if there is an optional query parameter named `q` (as in `http://127.0.0.1:8000/items/foo?q=somequery`) for `GET` requests.
  - As the `q` parameter is declared with `= None`, it is optional.
  - Without the `None` it would be required (as is the body in the case with `PUT`).
- For `PUT` requests to `/items/{item_id}`, Read the body as JSON:
  - Check that it has a required attribute `name` that should be a `str`.
  - Check that it has a required attribute `price` that has to be a `float`.
  - Check that it has an optional attribute `is_offer`, that should be a `bool`, if present.
  - All this would also work for deeply nested JSON objects.
- Convert from and to JSON automatically.
- Document everything with OpenAPI, that can be used by:
  - Interactive documentation systems.
  - Automatic client code generation systems, for many languages.
- Provide 2 interactive documentation web interfaces directly.

---

We just scratched the surface, but you already get the idea of how it all works.

Try changing the line with:

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...from:

```Python
        ... "item_name": item.name ...
```

...to:

```Python
        ... "item_price": item.price ...
```

...and see how your editor will auto-complete the attributes and know their types:

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

For a more complete example including more features, see the <a href="https://fastapi.tiangolo.com/tutorial/">Tutorial - User Guide</a>.

**Spoiler alert**: the tutorial - user guide includes:

- Declaration of **parameters** from other different places as: **headers**, **cookies**, **form fields** and **files**.
- How to set **validation constraints** as `maximum_length` or `regex`.
- A very powerful and easy to use **<abbr title="also known as components, resources, providers, services, injectables">Dependency Injection</abbr>** system.
- Security and authentication, including support for **OAuth2** with **JWT tokens** and **HTTP Basic** auth.
- More advanced (but equally easy) techniques for declaring **deeply nested JSON models** (thanks to Pydantic).
- Many extra features (thanks to Starlette) as:
  - **WebSockets**
  - **GraphQL**
  - extremely easy tests based on `requests` and `pytest`
  - **CORS**
  - **Cookie Sessions**
  - ...and more.

## Performance

Independent TechEmpower benchmarks show **FastAPI** applications running under Uvicorn as <a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">one of the fastest Python frameworks available</a>, only below Starlette and Uvicorn themselves (used internally by FastAPI). (\*)

To understand more about it, see the section <a href="https://fastapi.tiangolo.com/benchmarks/" class="internal-link" target="_blank">Benchmarks</a>.

## Optional Dependencies

Used by Pydantic:

- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - for faster JSON <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>.
- <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email_validator</code></a> - for email validation.

Used by Starlette:

- <a href="http://docs.python-requests.org" target="_blank"><code>requests</code></a> - Required if you want to use the `TestClient`.
- <a href="https://github.com/Tinche/aiofiles" target="_blank"><code>aiofiles</code></a> - Required if you want to use `FileResponse` or `StaticFiles`.
- <a href="http://jinja.pocoo.org" target="_blank"><code>jinja2</code></a> - Required if you want to use the default template configuration.
- <a href="https://andrew-d.github.io/python-multipart/" target="_blank"><code>python-multipart</code></a> - Required if you want to support form <abbr title="converting the string that comes from an HTTP request into Python data">"parsing"</abbr>, with `request.form()`.
- <a href="https://pythonhosted.org/itsdangerous/" target="_blank"><code>itsdangerous</code></a> - Required for `SessionMiddleware` support.
- <a href="https://pyyaml.org/wiki/PyYAMLDocumentation" target="_blank"><code>pyyaml</code></a> - Required for Starlette's `SchemaGenerator` support (you probably don't need it with FastAPI).
- <a href="https://graphene-python.org/" target="_blank"><code>graphene</code></a> - Required for `GraphQLApp` support.
- <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - Required if you want to use `UJSONResponse`.

Used by FastAPI / Starlette:

- <a href="http://www.uvicorn.org" target="_blank"><code>uvicorn</code></a> - for the server that loads and serves your application.
- <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - Required if you want to use `ORJSONResponse`.

You can install all of these with `pip install fastapi[all]`.

## License

This project is licensed under the terms of the MIT license.
