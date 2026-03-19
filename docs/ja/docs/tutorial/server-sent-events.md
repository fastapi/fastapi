# Server-Sent Events (SSE) { #server-sent-events-sse }

**Server-Sent Events** (SSE) を使うと、クライアントへデータをストリーミングできます。

これは[JSON Lines のストリーミング](stream-json-lines.md)に似ていますが、`text/event-stream` フォーマットを使用します。これはブラウザがネイティブに [`EventSource` API](https://developer.mozilla.org/en-US/docs/Web/API/EventSource) でサポートしています。

/// info | 情報

FastAPI 0.135.0 で追加されました。

///

## Server-Sent Events とは { #what-are-server-sent-events }

SSE は、HTTP 経由でサーバーからクライアントへデータをストリーミングするための標準です。

各イベントは、`data`、`event`、`id`、`retry` などの「フィールド」を含む小さなテキストブロックで、空行で区切られます。

次のようになります:

```
data: {"name": "Portal Gun", "price": 999.99}

data: {"name": "Plumbus", "price": 32.99}

```

SSE は、AI チャットのストリーミング、ライブ通知、ログやオブザビリティなど、サーバーがクライアントへ更新をプッシュする用途で一般的に使われます。

/// tip | 豆知識

バイナリデータ（例: 動画や音声）をストリーミングしたい場合は、上級ガイド [データのストリーミング](../advanced/stream-data.md) を参照してください。

///

## FastAPI で SSE をストリーミング { #stream-sse-with-fastapi }

FastAPI で SSE をストリーミングするには、*path operation 関数*で `yield` を使い、`response_class=EventSourceResponse` を設定します。

`EventSourceResponse` は `fastapi.sse` からインポートします:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[4,22] *}

yield された各アイテムは JSON にエンコードされ、SSE イベントの `data:` フィールドで送信されます。

戻り値の型を `AsyncIterable[Item]` と宣言すると、FastAPI は Pydantic を用いてデータを**検証**、**ドキュメント化**、**シリアライズ**します。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[1:25] hl[10:12,23] *}

/// tip | 豆知識

Pydantic が**Rust** 側でシリアライズを行うため、戻り値の型を宣言しない場合に比べて大幅に**高性能**になります。

///

### 非 async の *path operation 関数* { #non-async-path-operation-functions }

通常の `def` 関数（`async` なし）も使用でき、同様に `yield` を使えます。

イベントループをブロックしないよう、FastAPI が正しく実行されるように調整します。

この場合は関数が async ではないため、適切な戻り値の型は `Iterable[Item]` です:

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[28:31] hl[29] *}

### 戻り値の型なし { #no-return-type }

戻り値の型を省略することもできます。FastAPI は [`jsonable_encoder`](./encoder.md) を使ってデータを変換し、送信します。

{* ../../docs_src/server_sent_events/tutorial001_py310.py ln[34:37] hl[35] *}

## `ServerSentEvent` { #serversentevent }

`event`、`id`、`retry`、`comment` などの SSE フィールドを設定する必要がある場合は、生データの代わりに `ServerSentEvent` オブジェクトを `yield` できます。

`ServerSentEvent` は `fastapi.sse` からインポートします:

{* ../../docs_src/server_sent_events/tutorial002_py310.py hl[4,26] *}

`data` フィールドは常に JSON にエンコードされます。Pydantic モデルを含む、JSON にシリアライズ可能な任意の値を渡せます。

## 生データ { #raw-data }

JSON エンコードせずにデータを送る必要がある場合は、`data` の代わりに `raw_data` を使用します。

これは、整形済みテキスト、ログ行、または `[DONE]` のような特別な <dfn title="特別な条件や状態を示すために用いられる値">"センチネル"</dfn> 値を送るのに有用です。

{* ../../docs_src/server_sent_events/tutorial003_py310.py hl[17] *}

/// note | 備考

`data` と `raw_data` は相互排他的です。各 `ServerSentEvent` ではどちらか一方しか設定できません。

///

## `Last-Event-ID` での再開 { #resuming-with-last-event-id }

接続が途切れた後にブラウザが再接続すると、最後に受信した `id` を `Last-Event-ID` ヘッダーで送信します。

これをヘッダーパラメータとして受け取り、クライアントが離脱した位置からストリームを再開できます:

{* ../../docs_src/server_sent_events/tutorial004_py310.py hl[25,27,31] *}

## POST での SSE { #sse-with-post }

SSE は `GET` だけでなく、**任意の HTTP メソッド**で動作します。

これは、`POST` 上で SSE をストリーミングする [MCP](https://modelcontextprotocol.io) のようなプロトコルで有用です:

{* ../../docs_src/server_sent_events/tutorial005_py310.py hl[14] *}

## 技術詳細 { #technical-details }

FastAPI は SSE のいくつかのベストプラクティスを標準で実装しています。

- メッセージがない場合は 15 秒ごとに「キープアライブ」用の `ping` コメントを送信し、一部のプロキシが接続を閉じるのを防ぎます（[HTML 仕様: Server-Sent Events](https://html.spec.whatwg.org/multipage/server-sent-events.html#authoring-notes) の推奨に従います）。
- ストリームの**キャッシュを防止**するため、`Cache-Control: no-cache` ヘッダーを設定します。
- Nginx など一部のプロキシでの**バッファリングを防ぐ**ため、特別なヘッダー `X-Accel-Buffering: no` を設定します。

追加の設定は不要で、そのまま動作します。🤓
