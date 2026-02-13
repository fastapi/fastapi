# WebSockets { #websockets }

**FastAPI**で<a href="https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API" class="external-link" target="_blank">WebSockets</a>が使用できます。

## `websockets`のインストール { #install-websockets }

[仮想環境](../virtual-environments.md){.internal-link target=_blank}を作成し、それを有効化してから、「WebSocket」プロトコルを簡単に使えるようにするPythonライブラリの`websockets`をインストールしてください。

<div class="termy">

```console
$ pip install websockets

---> 100%
```

</div>

## WebSockets クライアント { #websockets-client }

### 本番環境 { #in-production }

本番環境では、React、Vue.js、Angularなどの最新のフレームワークで作成されたフロントエンドを使用しているでしょう。

そして、バックエンドとWebSocketsを使用して通信するために、おそらくフロントエンドのユーティリティを使用することになるでしょう。

または、ネイティブコードでWebSocketバックエンドと直接通信するネイティブモバイルアプリケーションがあるかもしれません。

他にも、WebSocketのエンドポイントと通信する方法があるかもしれません。

---

ただし、この例では非常にシンプルなHTML文書といくつかのJavaScriptを、すべて長い文字列の中に入れて使用することにします。

もちろん、これは最適な方法ではありませんし、本番環境で使うことはないでしょう。

本番環境では、上記の方法のいずれかの選択肢を採用することになるでしょう。

しかし、これはWebSocketsのサーバーサイドに焦点を当て、動作する例を示す最も簡単な方法です。

{* ../../docs_src/websockets/tutorial001_py310.py hl[2,6:38,41:43] *}

## `websocket` を作成する { #create-a-websocket }

**FastAPI** アプリケーションで、`websocket` を作成します。

{* ../../docs_src/websockets/tutorial001_py310.py hl[1,46:47] *}

/// note | 技術詳細

`from starlette.websockets import WebSocket` を使用しても構いません.

**FastAPI** は開発者の利便性のために、同じ `WebSocket` を提供します。しかし、こちらはStarletteから直接提供されるものです。

///

## メッセージを待機して送信する { #await-for-messages-and-send-messages }

WebSocketルートでは、メッセージを待機して送信するために `await` を使用できます。

{* ../../docs_src/websockets/tutorial001_py310.py hl[48:52] *}

バイナリやテキストデータ、JSONデータを送受信できます。

## 試してみる { #try-it }

ファイル名が `main.py` である場合、以下でアプリケーションを実行します。

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

ブラウザで <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> を開きます。

次のようなシンプルなページが表示されます。

<img src="/img/tutorial/websockets/image01.png">

入力ボックスにメッセージを入力して送信できます。

<img src="/img/tutorial/websockets/image02.png">

そして、 WebSocketsを使用した**FastAPI**アプリケーションが応答します。

<img src="/img/tutorial/websockets/image03.png">

複数のメッセージを送信（および受信）できます。

<img src="/img/tutorial/websockets/image04.png">

そして、これらの通信はすべて同じWebSocket接続を使用します。

## `Depends` などの使用 { #using-depends-and-others }

WebSocketエンドポイントでは、`fastapi` から以下をインポートして使用できます。

* `Depends`
* `Security`
* `Cookie`
* `Header`
* `Path`
* `Query`

これらは、他のFastAPI エンドポイント/*path operations* の場合と同じように機能します。

{* ../../docs_src/websockets/tutorial002_an_py310.py hl[68:69,82] *}

/// info | 情報

これはWebSocketであるため、`HTTPException` を発生させることはあまり意味がありません。代わりに `WebSocketException` を発生させます。

クロージングコードは、<a href="https://tools.ietf.org/html/rfc6455#section-7.4.1" class="external-link" target="_blank">仕様で定義された有効なコード</a>の中から使用することができます。

///

### 依存関係を用いてWebSocketsを試してみる { #try-the-websockets-with-dependencies }

ファイル名が `main.py` である場合、以下でアプリケーションを実行します。

<div class="termy">

```console
$ fastapi dev main.py

<span style="color: green;">INFO</span>:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

</div>

ブラウザで <a href="http://127.0.0.1:8000" class="external-link" target="_blank">http://127.0.0.1:8000</a> を開きます。

そこで、以下を設定できます。

* パスで使用される「Item ID」
* クエリパラメータとして使用される「Token」

/// tip | 豆知識

クエリ `token` は依存関係によって処理されることに注意してください。

///

これにより、WebSocketに接続してメッセージを送受信できます。

<img src="/img/tutorial/websockets/image05.png">

## 切断や複数クライアントの処理 { #handling-disconnections-and-multiple-clients }

WebSocket接続が閉じられると、 `await websocket.receive_text()` は例外 `WebSocketDisconnect` を発生させ、この例のようにキャッチして処理することができます。

{* ../../docs_src/websockets/tutorial003_py310.py hl[79:81] *}

試してみるには、

* いくつかのブラウザタブでアプリを開きます。
* それらのタブでメッセージを記入してください。
* そして、タブのうち1つを閉じてください。

これにより例外 `WebSocketDisconnect` が発生し、他のすべてのクライアントは次のようなメッセージを受信します。

```
Client #1596980209979 left the chat
```

/// tip | 豆知識

上記のアプリは、複数の WebSocket 接続に対してメッセージを処理し、ブロードキャストする方法を示すための最小限のシンプルな例です。

しかし、すべてがメモリ内の単一のリストで処理されるため、プロセスの実行中にのみ機能し、単一のプロセスでのみ機能することに注意してください。

FastAPIと簡単に統合できて、RedisやPostgreSQLなどでサポートされている、より堅牢なものが必要なら、<a href="https://github.com/encode/broadcaster" class="external-link" target="_blank">encode/broadcaster</a> を確認してください。

///

## 詳細情報 { #more-info }

オプションの詳細については、Starletteのドキュメントを確認してください。

* <a href="https://www.starlette.dev/websockets/" class="external-link" target="_blank">`WebSocket` クラス</a>.
* <a href="https://www.starlette.dev/endpoints/#websocketendpoint" class="external-link" target="_blank">クラスベースのWebSocket処理</a>.
