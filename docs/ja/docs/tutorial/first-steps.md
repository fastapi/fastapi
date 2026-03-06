# 最初のステップ { #first-steps }

最もシンプルなFastAPIファイルは以下のようになります:

{* ../../docs_src/first_steps/tutorial001_py310.py *}

これを`main.py`にコピーします。

ライブサーバーを実行します:

<div class="termy">

```console
$ <font color="#4E9A06">fastapi</font> dev <u style="text-decoration-style:solid">main.py</u>

  <span style="background-color:#009485"><font color="#D3D7CF"> FastAPI </font></span>  Starting development server 🚀

             Searching for package file structure from directories
             with <font color="#3465A4">__init__.py</font> files
             Importing from <font color="#75507B">/home/user/code/</font><font color="#AD7FA8">awesomeapp</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> module </font></span>  🐍 main.py

     <span style="background-color:#007166"><font color="#D3D7CF"> code </font></span>  Importing the FastAPI app object from the module with
             the following code:

             <u style="text-decoration-style:solid">from </u><u style="text-decoration-style:solid"><b>main</b></u><u style="text-decoration-style:solid"> import </u><u style="text-decoration-style:solid"><b>app</b></u>

      <span style="background-color:#007166"><font color="#D3D7CF"> app </font></span>  Using import string: <font color="#3465A4">main:app</font>

   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Server started at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font>
   <span style="background-color:#007166"><font color="#D3D7CF"> server </font></span>  Documentation at <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000/docs</u></font>

      <span style="background-color:#007166"><font color="#D3D7CF"> tip </font></span>  Running in development mode, for production use:
             <b>fastapi run</b>

             Logs:

     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Will watch for changes in these directories:
             <b>[</b><font color="#4E9A06">&apos;/home/user/code/awesomeapp&apos;</font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Uvicorn running on <font color="#729FCF"><u style="text-decoration-style:solid">http://127.0.0.1:8000</u></font> <b>(</b>Press CTRL+C
             to quit<b>)</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started reloader process <b>[</b><font color="#34E2E2"><b>383138</b></font><b>]</b> using WatchFiles
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Started server process <b>[</b><font color="#34E2E2"><b>383153</b></font><b>]</b>
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Waiting for application startup.
     <span style="background-color:#007166"><font color="#D3D7CF"> INFO </font></span>  Application startup complete.
```

</div>

出力には次のような行があります:

```hl_lines="4"
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

この行はローカルマシンでアプリが提供されているURLを示しています。

### チェック { #check-it }

ブラウザで<a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a>を開きます。

次のようなJSONレスポンスが表示されます:

```JSON
{"message": "Hello World"}
```

### 対話的APIドキュメント { #interactive-api-docs }

次に、<a href="http://127.0.0.1:8000/docs" class="external-link" target="_blank">http://127.0.0.1:8000/docs</a>にアクセスします。

自動生成された対話的APIドキュメントが表示されます (<a href="https://github.com/swagger-api/swagger-ui" class="external-link" target="_blank">Swagger UI</a>で提供):

![Swagger UI](https://fastapi.tiangolo.com/img/index/index-01-swagger-ui-simple.png)

### 代替APIドキュメント { #alternative-api-docs }

次に、<a href="http://127.0.0.1:8000/redoc" class="external-link" target="_blank">http://127.0.0.1:8000/redoc</a>にアクセスします。

先ほどとは異なる、自動生成された対話的APIドキュメントが表示されます (<a href="https://github.com/Rebilly/ReDoc" class="external-link" target="_blank">ReDoc</a>によって提供):

![ReDoc](https://fastapi.tiangolo.com/img/index/index-02-redoc-simple.png)

### OpenAPI { #openapi }

**FastAPI**は、APIを定義するための**OpenAPI**標準規格を使用して、すべてのAPIの「スキーマ」を生成します。

#### 「スキーマ」 { #schema }

「スキーマ」は定義または説明です。実装コードではなく、単なる抽象的な説明です。

#### API「スキーマ」 { #api-schema }

ここでは、<a href="https://github.com/OAI/OpenAPI-Specification" class="external-link" target="_blank">OpenAPI</a>はAPIのスキーマ定義の方法を規定する仕様です。

このスキーマ定義はAPIパス、受け取り可能なパラメータなどが含まれます。

#### データ「スキーマ」 { #data-schema }

「スキーマ」という用語は、JSONコンテンツなどの一部のデータの形状を指す場合もあります。

そのような場合、スキーマはJSON属性とそれらが持つデータ型などを意味します。

#### OpenAPIおよびJSONスキーマ { #openapi-and-json-schema }

OpenAPIはAPIのためのAPIスキーマを定義します。そして、そのスキーマは**JSONデータスキーマ**の標準規格である**JSON Schema**を利用するAPIによって送受されるデータの定義（または「スキーマ」）を含んでいます。

#### `openapi.json`を確認 { #check-the-openapi-json }

素のOpenAPIスキーマがどのようなものか興味がある場合、FastAPIはすべてのAPIの説明を含むJSON（スキーマ）を自動的に生成します。

次の場所で直接確認できます: <a href="http://127.0.0.1:8000/openapi.json" class="external-link" target="_blank">http://127.0.0.1:8000/openapi.json</a>.

次のようなJSONが表示されます。

```JSON
{
    "openapi": "3.1.0",
    "info": {
        "title": "FastAPI",
        "version": "0.1.0"
    },
    "paths": {
        "/items/": {
            "get": {
                "responses": {
                    "200": {
                        "description": "Successful Response",
                        "content": {
                            "application/json": {



...
```

#### OpenAPIの目的 { #what-is-openapi-for }

OpenAPIスキーマは、FastAPIに含まれている2つのインタラクティブなドキュメントシステムの動力源です。

そして、OpenAPIに基づいた代替案が数十通りあります。 **FastAPI**で構築されたアプリケーションに、これらの選択肢を簡単に追加できます。

また、APIと通信するクライアント用のコードを自動的に生成するために使用することもできます。たとえば、フロントエンド、モバイル、またはIoTアプリケーションです。

### アプリをデプロイ（任意） { #deploy-your-app-optional }

任意でFastAPIアプリを<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>にデプロイできます。まだなら、待機リストに登録してください。 🚀

すでに**FastAPI Cloud**アカウントがある場合（待機リストから招待済みの場合😉）、1コマンドでアプリケーションをデプロイできます。

デプロイする前に、ログインしていることを確認してください:

<div class="termy">

```console
$ fastapi login

You are logged in to FastAPI Cloud 🚀
```

</div>

その後、アプリをデプロイします:

<div class="termy">

```console
$ fastapi deploy

Deploying to FastAPI Cloud...

✅ Deployment successful!

🐔 Ready the chicken! Your app is ready at https://myapp.fastapicloud.dev
```

</div>

以上です！これで、そのURLでアプリにアクセスできます。 ✨

## ステップ毎の要約 { #recap-step-by-step }

### Step 1: `FastAPI`をインポート { #step-1-import-fastapi }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[1] *}

`FastAPI`は、APIのすべての機能を提供するPythonクラスです。

/// note | 技術詳細

`FastAPI`は`Starlette`を直接継承するクラスです。

`FastAPI`でも<a href="https://www.starlette.dev/" class="external-link" target="_blank">Starlette</a>のすべての機能を利用可能です。

///

### Step 2: `FastAPI`の「インスタンス」を生成 { #step-2-create-a-fastapi-instance }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[3] *}
ここで、`app`変数が`FastAPI`クラスの「インスタンス」になります。

これが、すべてのAPIを作成するための主要なポイントになります。

### Step 3: *path operation*を作成 { #step-3-create-a-path-operation }

#### パス { #path }

ここでの「パス」とは、最初の`/`から始まるURLの最後の部分を指します。

したがって、次のようなURLでは:

```
https://example.com/items/foo
```

...パスは次のようになります:

```
/items/foo
```

/// info | 情報

「パス」は一般に「エンドポイント」または「ルート」とも呼ばれます。

///

APIを構築する際、「パス」は「関心事」と「リソース」を分離するための主要な方法です。

#### Operation { #operation }

ここでの「オペレーション」とは、HTTPの「メソッド」の1つを指します。

以下のようなものの1つ:

* `POST`
* `GET`
* `PUT`
* `DELETE`

...さらによりエキゾチックなもの:

* `OPTIONS`
* `HEAD`
* `PATCH`
* `TRACE`

HTTPプロトコルでは、これらの「メソッド」の1つ（または複数）を使用して各パスにアクセスできます。

---

APIを構築するときは、通常、これらの特定のHTTPメソッドを使用して特定のアクションを実行します。

通常は次を使用します:

* `POST`: データの作成
* `GET`: データの読み取り
* `PUT`: データの更新
* `DELETE`: データの削除

したがって、OpenAPIでは、各HTTPメソッドは「オペレーション」と呼ばれます。

「**オペレーションズ**」とも呼ぶことにします。

#### *path operation デコレータ*を定義 { #define-a-path-operation-decorator }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[6] *}

`@app.get("/")`は直下の関数が下記のリクエストの処理を担当することを**FastAPI**に伝えます:

* パス `/`
* <dfn title="HTTP GET メソッド"><code>get</code> オペレーション</dfn>

/// info | `@decorator` Info

Pythonにおける`@something`シンタックスはデコレータと呼ばれます。

「デコレータ」は関数の上に置きます。かわいらしい装飾的な帽子のようです（この用語の由来はそこにあると思います）。

「デコレータ」は直下の関数を受け取り、それを使って何かを行います。

私たちの場合、このデコレーターは直下の関数が**オペレーション** `get`を使用した**パス** `/`に対応することを**FastAPI** に通知します。

これが「*path operation デコレータ*」です。

///

他のオペレーションも使用できます:

* `@app.post()`
* `@app.put()`
* `@app.delete()`

また、よりエキゾチックなものも使用できます:

* `@app.options()`
* `@app.head()`
* `@app.patch()`
* `@app.trace()`

/// tip | 豆知識

各オペレーション (HTTPメソッド)は自由に使用できます。

**FastAPI**は特定の意味づけを強制しません。

ここでの情報は、要件ではなくガイドラインとして提示されます。

例えば、GraphQLを使用する場合、通常は`POST`オペレーションのみを使用してすべてのアクションを実行します。

///

### Step 4: **path operation 関数**を定義 { #step-4-define-the-path-operation-function }

以下は「**path operation 関数**」です:

* **パス**: は`/`です。
* **オペレーション**: は`get`です。
* **関数**: 「デコレータ」の直下にある関数 (`@app.get("/")`の直下) です。

{* ../../docs_src/first_steps/tutorial001_py310.py hl[7] *}

これは、Pythonの関数です。

この関数は、`GET`オペレーションを使ったURL「`/`」へのリクエストを受け取るたびに**FastAPI**によって呼び出されます。

この場合、この関数は`async`関数です。

---

`async def`の代わりに通常の関数として定義することもできます:

{* ../../docs_src/first_steps/tutorial003_py310.py hl[7] *}

/// note | 備考

違いが分からない場合は、[Async: *"急いでいますか？"*](../async.md#in-a-hurry){.internal-link target=_blank}を確認してください。

///

### Step 5: コンテンツの返信 { #step-5-return-the-content }

{* ../../docs_src/first_steps/tutorial001_py310.py hl[8] *}

`dict`、`list`、`str`、`int`などの単一の値を返すことができます。

Pydanticモデルを返すこともできます（後で詳しく説明します）。

JSONに自動的に変換されるオブジェクトやモデルは他にもたくさんあります（ORMなど）。 お気に入りのものを使ってみてください。すでにサポートされている可能性が高いです。

### Step 6: デプロイする { #step-6-deploy-it }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**に1コマンドでアプリをデプロイします: `fastapi deploy`. 🎉

#### FastAPI Cloudについて { #about-fastapi-cloud }

**<a href="https://fastapicloud.com" class="external-link" target="_blank">FastAPI Cloud</a>**は、**FastAPI**の作者とそのチームによって開発されています。

最小限の労力でAPIの**構築**、**デプロイ**、**アクセス**を行うプロセスを合理化します。

FastAPIでアプリを構築するのと同じ**開発体験**を、クラウドへの**デプロイ**にもたらします。 🎉

FastAPI Cloudは、*FastAPI and friends*のオープンソースプロジェクトに対する主要スポンサーであり、資金提供元です。 ✨

#### 他のクラウドプロバイダにデプロイする { #deploy-to-other-cloud-providers }

FastAPIはオープンソースで、標準に基づいています。選択した任意のクラウドプロバイダにFastAPIアプリをデプロイできます。

クラウドプロバイダのガイドに従って、FastAPIアプリをデプロイしてください。 🤓

## まとめ { #recap }

* `FastAPI`をインポートします。
* `app`インスタンスを生成します。
* `@app.get("/")`のようなデコレータを使用して、**path operation デコレータ**を記述します。
* **path operation 関数**を定義します。例: `def root(): ...`。
* `fastapi dev`コマンドで開発サーバーを起動します。
* 任意で`fastapi deploy`を使ってアプリをデプロイします。
