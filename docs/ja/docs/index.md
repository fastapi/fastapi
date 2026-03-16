# FastAPI { #fastapi }

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
  <a href="https://fastapi.tiangolo.com/ja"><img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="FastAPI"></a>
</p>
<p align="center">
    <em>FastAPI フレームワーク、高パフォーマンス、学びやすい、素早くコーディングできる、本番運用に対応</em>
</p>
<p align="center">
<a href="https://github.com/fastapi/fastapi/actions?query=workflow%3ATest+event%3Apush+branch%3Amaster" target="_blank">
    <img src="https://github.com/fastapi/fastapi/actions/workflows/test.yml/badge.svg?event=push&branch=master" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/fastapi/fastapi" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/fastapi/fastapi.svg" alt="Coverage">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/fastapi" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

**ドキュメント**: <a href="https://fastapi.tiangolo.com/ja" target="_blank">https://fastapi.tiangolo.com</a>

**ソースコード**: <a href="https://github.com/fastapi/fastapi" target="_blank">https://github.com/fastapi/fastapi</a>

---

FastAPI は、Python の標準である型ヒントに基づいて Python で API を構築するための、モダンで、高速（高パフォーマンス）な Web フレームワークです。

主な特徴:

* **高速**: **NodeJS** や **Go** 並みのとても高いパフォーマンス（Starlette と Pydantic のおかげです）。 [利用可能な最も高速な Python フレームワークの一つです](#performance)。
* **高速なコーディング**: 開発速度を約 200%〜300% 向上させます。*
* **少ないバグ**: 開発者起因のヒューマンエラーを約 40% 削減します。*
* **直感的**: 素晴らしいエディタサポート。<dfn title="別名: auto-complete、autocompletion、IntelliSense">補完</dfn> があらゆる場所で使えます。デバッグ時間を削減します。
* **簡単**: 簡単に利用・習得できるようにデザインされています。ドキュメントを読む時間を削減します。
* **短い**: コードの重複を最小限にします。各パラメータ宣言から複数の機能を得られます。バグも減ります。
* **堅牢性**: 自動対話型ドキュメントにより、本番環境向けのコードが得られます。
* **Standards-based**: API のオープンスタンダードに基づいており（そして完全に互換性があります）、<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>（以前は Swagger として知られていました）や <a href="https://json-schema.org/" class="external-link" target="_blank">JSON Schema</a> をサポートします。

<small>* 本番アプリケーションを構築している社内開発チームのテストに基づく見積もりです。</small>

## Sponsors { #sponsors }

<!-- sponsors -->

### Keystone Sponsor { #keystone-sponsor }

{% for sponsor in sponsors.keystone -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}

### Gold and Silver Sponsors { #gold-and-silver-sponsors }

{% for sponsor in sponsors.gold -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor -%}
{%- for sponsor in sponsors.silver -%}
<a href="{{ sponsor.url }}" target="_blank" title="{{ sponsor.title }}"><img src="{{ sponsor.img }}" style="border-radius:15px"></a>
{% endfor %}

<!-- /sponsors -->

<a href="https://fastapi.tiangolo.com/ja/fastapi-people/#sponsors" class="external-link" target="_blank">その他のスポンサー</a>

## 評価 { #opinions }

"_[...] 最近 **FastAPI** を使っています。 [...] 実際に私のチームの全ての **Microsoft の機械学習サービス** で使用する予定です。 そのうちのいくつかのコアな **Windows** 製品と **Office** 製品に統合されつつあります。_"

<div style="text-align: right; margin-right: 10%;">Kabir Khan - <strong>Microsoft</strong> <a href="https://github.com/fastapi/fastapi/pull/26" target="_blank"><small>(ref)</small></a></div>

---

"_FastAPIライブラリを採用し、クエリで **予測値** を取得できる **REST** サーバを構築しました。 [for Ludwig]_"

<div style="text-align: right; margin-right: 10%;">Piero Molino, Yaroslav Dudin, and Sai Sumanth Miryala - <strong>Uber</strong> <a href="https://eng.uber.com/ludwig-v0-2/" target="_blank"><small>(ref)</small></a></div>

---

"_**Netflix** は、**危機管理**オーケストレーションフレームワーク、**Dispatch** のオープンソースリリースを発表できることをうれしく思います。 [built with **FastAPI**]_"

<div style="text-align: right; margin-right: 10%;">Kevin Glisson, Marc Vilanova, Forest Monsen - <strong>Netflix</strong> <a href="https://netflixtechblog.com/introducing-dispatch-da4b8a2a8072" target="_blank"><small>(ref)</small></a></div>

---

"_私は **FastAPI** にワクワクしています。 めちゃくちゃ楽しいです！_"

<div style="text-align: right; margin-right: 10%;">Brian Okken - <strong><a href="https://pythonbytes.fm/episodes/show/123/time-to-right-the-py-wrongs?time_in_sec=855" target="_blank">Python Bytes</a> podcast host</strong> <a href="https://x.com/brianokken/status/1112220079972728832" target="_blank"><small>(ref)</small></a></div>

---

"_正直、あなたが作ったものは超堅実で洗練されているように見えます。いろんな意味で、それは私が **Hug** にそうなってほしかったものです。誰かがそれを作るのを見るのは本当に刺激的です。_"

<div style="text-align: right; margin-right: 10%;">Timothy Crosley - <strong><a href="https://github.com/hugapi/hug" target="_blank">Hug</a> creator</strong> <a href="https://news.ycombinator.com/item?id=19455465" target="_blank"><small>(ref)</small></a></div>

---

"_REST API を構築するための **モダンなフレームワーク** を学びたい方は、**FastAPI** [...] をチェックしてみてください。 [...] 高速で、使用・習得が簡単です [...]_"

"_私たちの **API** は **FastAPI** に切り替えました [...] きっと気に入ると思います [...]_"

<div style="text-align: right; margin-right: 10%;">Ines Montani - Matthew Honnibal - <strong><a href="https://explosion.ai" target="_blank">Explosion AI</a> founders - <a href="https://spacy.io" target="_blank">spaCy</a> creators</strong> <a href="https://x.com/_inesmontani/status/1144173225322143744" target="_blank"><small>(ref)</small></a> - <a href="https://x.com/honnibal/status/1144031421859655680" target="_blank"><small>(ref)</small></a></div>

---

"_本番運用の Python API を構築したい方には、**FastAPI** を強くおすすめします。**美しく設計**されており、**使いやすく**、**高いスケーラビリティ**があります。私たちの API ファースト開発戦略の **主要コンポーネント** となり、Virtual TAC Engineer などの多くの自動化やサービスを推進しています。_"

<div style="text-align: right; margin-right: 10%;">Deon Pillsbury - <strong>Cisco</strong> <a href="https://www.linkedin.com/posts/deonpillsbury_cisco-cx-python-activity-6963242628536487936-trAp/" target="_blank"><small>(ref)</small></a></div>

---

## FastAPI ミニドキュメンタリー { #fastapi-mini-documentary }

2025 年末に公開された <a href="https://www.youtube.com/watch?v=mpR8ngthqiE" class="external-link" target="_blank">FastAPI ミニドキュメンタリー</a>があります。オンラインで視聴できます:

<a href="https://www.youtube.com/watch?v=mpR8ngthqiE" target="_blank"><img src="https://fastapi.tiangolo.com/img/fastapi-documentary.jpg" alt="FastAPI Mini Documentary"></a>

## **Typer**、CLI 版 FastAPI { #typer-the-fastapi-of-clis }

<a href="https://typer.tiangolo.com" target="_blank"><img src="https://typer.tiangolo.com/img/logo-margin/logo-margin-vector.svg" style="width: 20%;"></a>

Web API の代わりにターミナルで使用する <abbr title="Command Line Interface - コマンドラインインターフェイス">CLI</abbr> アプリを構築する場合は、<a href="https://typer.tiangolo.com/" class="external-link" target="_blank">**Typer**</a> を確認してください。

**Typer** は FastAPI の弟分です。そして、**CLI 版 FastAPI** を意図しています。 ⌨️ 🚀

## 必要条件 { #requirements }

FastAPI は巨人の肩の上に立っています。

* Web の部分は <a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>
* データの部分は <a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a>

## インストール { #installation }

<a href="https://fastapi.tiangolo.com/ja/virtual-environments/" class="external-link" target="_blank">virtual environment</a> を作成して有効化し、それから FastAPI をインストールします。

<div class="termy">

```console
$ pip install "fastapi[standard]"

---> 100%
```

</div>

**注**: すべてのターミナルで動作するように、`"fastapi[standard]"` は必ずクォートで囲んでください。

## アプリケーション例 { #example }

### 作成 { #create-it }

`main.py` ファイルを作成し、以下のコードを入力します。

```Python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

<details markdown="1">
<summary>または <code>async def</code> を使います...</summary>

コードで `async` / `await` を使用する場合は、`async def` を使います。

```Python hl_lines="7  12"
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

**注**:

わからない場合は、<a href="https://fastapi.tiangolo.com/ja/async/#in-a-hurry" target="_blank">ドキュメントの `async` と `await` の _"In a hurry?"_ セクション</a>を確認してください。

</details>

### 実行 { #run-it }

以下のコマンドでサーバーを起動します。

<div class="termy">

```console
$ fastapi dev main.py

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/home/user/code/awesomeapp']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2248755] using WatchFiles
INFO:     Started server process [2248757]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

</div>

<details markdown="1">
<summary><code>fastapi dev main.py</code> コマンドについて</summary>

`fastapi dev` コマンドは `main.py` ファイルを読み取り、その中の **FastAPI** アプリを検出し、<a href="https://www.uvicorn.dev" class="external-link" target="_blank">Uvicorn</a> を使用してサーバーを起動します。

デフォルトでは、`fastapi dev` はローカル開発向けに自動リロードを有効にして起動します。

詳しくは <a href="https://fastapi.tiangolo.com/ja/fastapi-cli/" target="_blank">FastAPI CLI docs</a> を参照してください。

</details>

### 動作確認 { #check-it }

ブラウザで <a href="http://127.0.0.1:8000/items/5?q=somequery" class="external-link" target="_blank">http://127.0.0.1:8000/items/5?q=somequery</a> を開きます。

以下の JSON のレスポンスが確認できます。

```JSON
{"item_id": 5, "q": "somequery"}
```

すでに以下の API が作成されています。

* _パス_ `/` と `/items/{item_id}` で HTTP リクエストを受け取ります。
* 両方の _パス_ は `GET` <em>操作</em>（HTTP _メソッド_ としても知られています）を取ります。
* _パス_ `/items/{item_id}` は `int` であるべき _パスパラメータ_ `item_id` を持ちます。
* _パス_ `/items/{item_id}` はオプションの `str` _クエリパラメータ_ `q` を持ちます。

### 自動対話型 API ドキュメント { #interactive-api-docs }

次に、<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> にアクセスします。

自動対話型 API ドキュメントが表示されます（<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a> が提供しています）。

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 代替 API ドキュメント { #alternative-api-docs }

次に、<a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> にアクセスします。

代替の自動ドキュメントが表示されます（<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a> が提供しています）。

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

## アップグレード例 { #example-upgrade }

次に、`PUT` リクエストからボディを受け取るために `main.py` ファイルを修正しましょう。

Pydantic によって、標準的な Python の型を使ってボディを宣言します。

```Python hl_lines="2  7-10 23-25"
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
```

`fastapi dev` サーバーは自動でリロードされるはずです。

### 自動対話型 API ドキュメントのアップグレード { #interactive-api-docs-upgrade }

次に、<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a> にアクセスします。

* 自動対話型 API ドキュメントは新しいボディも含めて自動でアップデートされます。

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-03-swagger-02.png)

* 「Try it out」ボタンをクリックします。パラメータを入力して API と直接やりとりできます。

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-04-swagger-03.png)

* 次に、「Execute」ボタンをクリックします。ユーザーインターフェースは API と通信し、パラメータを送信し、結果を取得して画面に表示します。

![Swagger UI interaction](https://fastapi.tiangolo.com/img/index/index-05-swagger-04.png)

### 代替 API ドキュメントのアップグレード { #alternative-api-docs-upgrade }

次に、<a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a> にアクセスします。

* 代替のドキュメントにも新しいクエリパラメータやボディが反映されます。

![ReDoc](https://fastapi.tiangolo.com/img/index/index-06-redoc-02.png)

### まとめ { #recap }

要約すると、関数のパラメータとして、パラメータやボディなどの型を **一度だけ** 宣言します。

標準的な最新の Python の型を使います。

新しい構文や特定のライブラリのメソッドやクラスなどを覚える必要はありません。

単なる標準的な **Python** です。

例えば、`int` の場合:

```Python
item_id: int
```

または、より複雑な `Item` モデルの場合:

```Python
item: Item
```

...そして、この一度の宣言で、以下のようになります。

* 以下を含むエディタサポート:
    * 補完。
    * 型チェック。
* データの検証:
    * データが無効な場合に自動で明確なエラーを返します。
    * 深い入れ子になった JSON オブジェクトでも検証が可能です。
* 入力データの <dfn title="別名: serialization、parsing、marshalling">変換</dfn>: ネットワークから Python のデータや型へ。以下から読み取ります:
    * JSON。
    * パスパラメータ。
    * クエリパラメータ。
    * Cookie。
    * ヘッダー。
    * フォーム。
    * ファイル。
* 出力データの <dfn title="別名: serialization、parsing、marshalling">変換</dfn>: Python のデータや型からネットワークデータへ（JSON として）変換します:
    * Python の型（`str`、`int`、`float`、`bool`、`list` など）の変換。
    * `datetime` オブジェクト。
    * `UUID` オブジェクト。
    * データベースモデル。
    * ...などなど。
* 2 つの代替ユーザーインターフェースを含む自動対話型 API ドキュメント:
    * Swagger UI。
    * ReDoc。

---

前のコード例に戻ると、**FastAPI** は次のように動作します。

* `GET` および `PUT` リクエストのパスに `item_id` があることを検証します。
* `GET` および `PUT` リクエストに対して `item_id` が `int` 型であることを検証します。
    * そうでない場合、クライアントは有用で明確なエラーを受け取ります。
* `GET` リクエストに対して、`q` という名前のオプションのクエリパラメータ（`http://127.0.0.1:8000/items/foo?q=somequery` のような）が存在するかどうかを調べます。
    * `q` パラメータは `= None` で宣言されているため、オプションです。
    * `None` がなければ必須になります（`PUT` の場合のボディと同様です）。
* `PUT` リクエストを `/items/{item_id}` に送信する場合、ボディを JSON として読み込みます:
    * 必須の属性 `name` があり、`str` であるべきことを確認します。
    * 必須の属性 `price` があり、`float` でなければならないことを確認します。
    * オプションの属性 `is_offer` があり、存在する場合は `bool` であるべきことを確認します。
    * これらはすべて、深くネストされた JSON オブジェクトに対しても動作します。
* JSON への/からの変換を自動的に行います。
* OpenAPI ですべてを文書化し、以下で利用できます:
    * 対話型ドキュメントシステム。
    * 多くの言語に対応した自動クライアントコード生成システム。
* 2 つの対話型ドキュメント Web インターフェースを直接提供します。

---

まだ表面的な部分に触れただけですが、仕組みはすでにイメージできているはずです。

以下の行を変更してみてください。

```Python
    return {"item_name": item.name, "item_id": item_id}
```

...以下の:

```Python
        ... "item_name": item.name ...
```

...を:

```Python
        ... "item_price": item.price ...
```

...に変更し、エディタが属性を自動補完し、その型を知ることを確認してください。

![editor support](https://fastapi.tiangolo.com/img/vscode-completion.png)

より多くの機能を含む、より完全な例については、<a href="https://fastapi.tiangolo.com/ja/tutorial/">Tutorial - User Guide</a> を参照してください。

**ネタバレ注意**: tutorial - user guide には以下が含まれます。

* **ヘッダー**、**Cookie**、**フォームフィールド**、**ファイル**など、他のさまざまな場所からの **パラメータ** 宣言。
* `maximum_length` や `regex` のような **検証制約** を設定する方法。
* 非常に強力で使いやすい **<dfn title="別名: components、resources、providers、services、injectables">依存性注入</dfn>** システム。
* **JWT トークン**を用いた **OAuth2** や **HTTP Basic** 認証のサポートを含む、セキュリティと認証。
* **深くネストされた JSON モデル**を宣言するための、より高度な（しかし同様に簡単な）手法（Pydantic のおかげです）。
* <a href="https://strawberry.rocks" class="external-link" target="_blank">Strawberry</a> および他のライブラリによる **GraphQL** 統合。
* 以下のようなたくさんのおまけ機能（Starlette のおかげです）:
    * **WebSockets**
    * HTTPX と `pytest` に基づく極めて簡単なテスト
    * **CORS**
    * **Cookie Sessions**
    * ...などなど。

### アプリをデプロイ（任意） { #deploy-your-app-optional }

必要に応じて FastAPI アプリを <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> にデプロイできます。まだの場合はウェイティングリストに参加してください。 🚀

すでに **FastAPI Cloud** アカウント（ウェイティングリストから招待されました 😉）がある場合は、1 コマンドでアプリケーションをデプロイできます。

デプロイ前に、ログインしていることを確認してください。

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

次に、アプリをデプロイします。

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

これで完了です！その URL でアプリにアクセスできます。 ✨

#### FastAPI Cloud について { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>** は **FastAPI** の作者と同じチームによって作られています。

最小限の労力で API を **構築**、**デプロイ**、**アクセス** するためのプロセスを効率化します。

FastAPI でアプリを構築するのと同じ **開発者体験** を、クラウドへの **デプロイ** にももたらします。 🎉

FastAPI Cloud は *FastAPI and friends* オープンソースプロジェクトの主要スポンサーであり、資金提供元です。 ✨

#### 他のクラウドプロバイダにデプロイ { #deploy-to-other-cloud-providers }

FastAPI はオープンソースであり、標準に基づいています。選択した任意のクラウドプロバイダに FastAPI アプリをデプロイできます。

各クラウドプロバイダのガイドに従って、FastAPI アプリをデプロイしてください。 🤓

## パフォーマンス { #performance }

独立した TechEmpower のベンチマークでは、Uvicorn で動作する **FastAPI** アプリケーションが、<a href="https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7" class="external-link" target="_blank">利用可能な最も高速な Python フレームワークの一つ</a>であり、Starlette と Uvicorn（FastAPI で内部的に使用されています）にのみ下回っていると示されています。（*）

詳細は <a href="https://fastapi.tiangolo.com/ja/benchmarks/" class="internal-link" target="_blank">Benchmarks</a> セクションをご覧ください。

## 依存関係 { #dependencies }

FastAPI は Pydantic と Starlette に依存しています。

### `standard` 依存関係 { #standard-dependencies }

FastAPI を `pip install "fastapi[standard]"` でインストールすると、`standard` グループのオプション依存関係が含まれます。

Pydantic によって使用されるもの:

* <a href="https://github.com/JoshData/python-email-validator" target="_blank"><code>email-validator</code></a> - メール検証のため。

Starlette によって使用されるもの:

* <a href="https://www.python-httpx.org" target="_blank"><code>httpx</code></a> - `TestClient` を使用したい場合に必要です。
* <a href="https://jinja.palletsprojects.com" target="_blank"><code>jinja2</code></a> - デフォルトのテンプレート設定を使用したい場合に必要です。
* <a href="https://github.com/Kludex/python-multipart" target="_blank"><code>python-multipart</code></a> - `request.form()` とともに、フォームの <dfn title="HTTP リクエストから届く文字列を Python データに変換すること">「parsing」</dfn> をサポートしたい場合に必要です。

FastAPI によって使用されるもの:

* <a href="https://www.uvicorn.dev" target="_blank"><code>uvicorn</code></a> - アプリケーションをロードして提供するサーバーのため。これには `uvicorn[standard]` も含まれ、高性能なサービングに必要な依存関係（例: `uvloop`）が含まれます。
* `fastapi-cli[standard]` - `fastapi` コマンドを提供します。
    * これには `fastapi-cloud-cli` が含まれ、FastAPI アプリケーションを <a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a> にデプロイできます。

### `standard` 依存関係なし { #without-standard-dependencies }

`standard` のオプション依存関係を含めたくない場合は、`pip install "fastapi[standard]"` の代わりに `pip install fastapi` でインストールできます。

### `fastapi-cloud-cli` なし { #without-fastapi-cloud-cli }

標準の依存関係を含めつつ `fastapi-cloud-cli` を除外して FastAPI をインストールしたい場合は、`pip install "fastapi[standard-no-fastapi-cloud-cli]"` でインストールできます。

### 追加のオプション依存関係 { #additional-optional-dependencies }

追加でインストールしたい依存関係があります。

追加のオプション Pydantic 依存関係:

* <a href="https://docs.pydantic.dev/latest/usage/pydantic_settings/" target="_blank"><code>pydantic-settings</code></a> - 設定管理のため。
* <a href="https://docs.pydantic.dev/latest/usage/types/extra_types/extra_types/" target="_blank"><code>pydantic-extra-types</code></a> - Pydantic で使用する追加の型のため。

追加のオプション FastAPI 依存関係:

* <a href="https://github.com/ijl/orjson" target="_blank"><code>orjson</code></a> - `ORJSONResponse` を使用したい場合に必要です。
* <a href="https://github.com/esnme/ultrajson" target="_blank"><code>ujson</code></a> - `UJSONResponse` を使用したい場合に必要です。

## ライセンス { #license }

このプロジェクトは MIT ライセンスの条項の下でライセンスされています。
