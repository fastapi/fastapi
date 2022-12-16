# WebSocket

**FastAPI**で<a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSocket</a>が使用できます。

## `WebSockets`のインストール

まず `WebSockets`のインストールが必要です。

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSocket クライアント

### 本番環境

本番環境では、React、Vue.js、Angularなどの最新のフレームワークで作成されたフロントエンドを使用しているでしょう。

そして、バックエンドとWebSocketを使用して通信するために、おそらくフロントエンドのユーティリティを使用することになるでしょう。

または、ネイティブコードでWebSocketバックエンドと直接通信するネイティブモバイルアプリケーションがあるかもしれません。

他にも、WebSocketのエンドポイントと通信する方法があるかもしれません。

---

ただし、この例では非常にシンプルなHTML文書といくつかのJavaScriptを、すべてソースコードの中に入れて使用することにします。

もちろん、これは最適な方法ではありませんし、本番環境で使うことはないでしょう。

本番環境では、上記の方法のいずれかの選択肢を採用することになるでしょう。

しかし、これはWebSocketのサーバーサイドに焦点を当て、実用的な例を示す最も簡単な方法です。

```Python hl_lines="2  6-38  41-43"
{!../../../docs_src/websockets/tutorial001.py!}
```

## `websocket` を作成する

**FastAPI** アプリケーションで、`websocket` を作成します。

```Python hl_lines="1  46-47"
{!../../../docs_src/websockets/tutorial001.py!}
```

!!! note "技術詳細"
    `from starlette.websockets import WebSocket` を使用しても構いません.

    **FastAPI** は開発者の利便性のために、同じ `WebSocket` を提供します。しかし、こちらはStarletteから直接提供されるものです。

## メッセージの送受信

WebSocketルートでは、 `await` を使ってメッセージの送受信ができます。

```Python hl_lines="48-52"
{!../../../docs_src/websockets/tutorial001.py!}
```

バイナリやテキストデータ、JSONデータを送受信できます。

## 試してみる

ファイル名が `main.py` である場合、以下の方法でアプリケーションを実行します。

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

ブラウザで <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> を開きます。

次のようなシンプルなページが表示されます。

<img src="/img/tutorial/websockets/image01.png">

入力ボックスにメッセージを入力して送信できます。

<img src="/img/tutorial/websockets/image02.png">

そして、 WebSocketを使用した**FastAPI**アプリケーションが応答します。

<img src="/img/tutorial/websockets/image03.png">

複数のメッセージを送信（および受信）できます。

<img src="/img/tutorial/websockets/image04.png">

そして、これらの通信はすべて同じWebSocket接続を使用します。

## 依存関係

WebSocketエンドポイントでは、`fastapi` から以下をインポートして使用できます。

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

これらは、他のFastAPI エンドポイント/*path operation* の場合と同じように機能します。

```Python hl_lines="58-65  68-83"
{!../../../docs_src/websockets/tutorial002.py!}
```

!!! info "情報"
    WebSocket で `HTTPException` を発生させることはあまり意味がありません。したがって、WebSocketの接続を直接閉じる方がよいでしょう。

    クロージングコードは、<a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">仕様で定義された有効なコード</a>の中から使用することができます。

    将来的には、どこからでも `raise` できる `WebSocketException` が用意され、専用の例外ハンドラを追加できるようになる予定です。これは、Starlette の <a href="https://github.com/encode/starlette/pull/527" class="external-link" target="_blank">PR #527</a> に依存するものです。

### 依存関係を用いてWebSocketsを試してみる

ファイル名が `main.py` である場合、以下の方法でアプリケーションを実行します。

<div class="termy">

```console
$ uvicorn main:app --reload

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

ブラウザで <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> を開きます。

クライアントが設定できる項目は以下の通りです。

* パスで使用される「Item ID」
* クエリパラメータとして使用される「Token」

!!! tip "豆知識"
    クエリ `token` は依存パッケージによって処理されることに注意してください。

これにより、WebSocketに接続してメッセージを送受信できます。

<img src="/img/tutorial/websockets/image05.png">

## 切断や複数クライアントへの対応

WebSocket接続が閉じられると、 `await websocket.receive_text()` は例外 `WebSocketDisconnect` を発生させ、この例のようにキャッチして処理することができます。

```Python hl_lines="81-83"
{!../../../docs_src/websockets/tutorial003.py!}
```

試してみるには、

* いくつかのブラウザタブでアプリを開きます。
* それらのタブでメッセージを記入してください。
* そして、タブのうち1つを閉じてください。

これにより例外 `WebSocketDisconnect` が発生し、他のすべてのクライアントは次のようなメッセージを受信します。

```
Client #1596980209979 left the chat
```

!!! tip "豆知識"
    上記のアプリは、複数の WebSocket 接続に対してメッセージを処理し、ブロードキャストする方法を示すための最小限のシンプルな例です。

    しかし、すべての接続がメモリ内の単一のリストで処理されるため、プロセスの実行中にのみ機能し、単一のプロセスでのみ機能することに注意してください。

    もしFastAPIと簡単に統合できて、RedisやPostgreSQLなどでサポートされている、より堅牢なものが必要なら、<a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a> を確認してください。

## その他のドキュメント

オプションの詳細については、Starletteのドキュメントを確認してください。

* <a href="https://www.starlette.io/websockets/" class="external-link" target="_blank"> `WebSocket` クラス</a>
* <a href="https://www.starlette.io/endpoints/#websocketendpoint" class="external-link" target="_blank">クラスベースのWebSocket処理</a>
