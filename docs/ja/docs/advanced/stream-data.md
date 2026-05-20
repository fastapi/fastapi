# データのストリーミング { #stream-data }

JSON として構造化できるデータをストリームしたい場合は、[JSON Lines をストリームする](../tutorial/stream-json-lines.md) を参照してください。

しかし、純粋なバイナリデータや文字列をストリームしたい場合は、次のようにできます。

/// info | 情報

FastAPI 0.134.0 で追加されました。

///

## ユースケース { #use-cases }

例えば、AI LLM サービスの出力をそのまま、純粋な文字列としてストリームしたい場合に使えます。

メモリに一度に全て読み込むことなく、読み込みながらチャンクごとに送ることで、巨大なバイナリファイルをストリームすることにも使えます。

同様に、動画や音声をストリームすることもできます。処理しながら生成し、そのまま送信することも可能です。

## `yield` を使った `StreamingResponse` { #a-streamingresponse-with-yield }

path operation 関数で `response_class=StreamingResponse` を宣言すると、`yield` を使ってデータをチャンクごとに順次送信できます。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[1:23] hl[20,23] *}

FastAPI は各データチャンクをそのまま `StreamingResponse` に渡し、JSON などに変換しようとはしません。

### 非 async な path operation 関数 { #non-async-path-operation-functions }

`async` なしの通常の `def` 関数でも同様に `yield` を使えます。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[26:29] hl[27] *}

### アノテーションなし { #no-annotation }

バイナリデータをストリームする場合、戻り値の型アノテーションを宣言する必要は実際にはありません。

この場合、FastAPI はデータを Pydantic で JSON 化したり、何らかの方法でシリアライズしようとしないため、型アノテーションはエディタやツール向けの補助にすぎず、FastAPI 自体では使用されません。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[32:35] hl[33] *}

つまり、`StreamingResponse` では型アノテーションに依存せず、送信したい形式に合わせてバイト列を生成・エンコードする「自由」と「責任」があなたにあります。 🤓

### バイト列をストリームする { #stream-bytes }

主なユースケースの一つは、文字列ではなく `bytes` をストリームすることです。もちろん可能です。

{* ../../docs_src/stream_data/tutorial001_py310.py ln[44:47] hl[47] *}

## カスタム `PNGStreamingResponse` { #a-custom-pngstreamingresponse }

上記の例ではバイト列をストリームしましたが、レスポンスに `Content-Type` ヘッダがないため、クライアントは受け取るデータの種類を認識できませんでした。

`StreamingResponse` を継承したカスタムクラスを作成し、ストリームするデータに応じて `Content-Type` ヘッダを設定できます。

例えば、`media_type` 属性で `Content-Type` を `image/png` に設定する `PNGStreamingResponse` を作成できます:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[6,19:20] hl[20] *}

その後、path operation 関数で `response_class=PNGStreamingResponse` としてこの新しいクラスを使用できます:

{* ../../docs_src/stream_data/tutorial002_py310.py ln[23:27] hl[23] *}

### ファイルを模擬する { #simulate-a-file }

この例では `io.BytesIO` でファイルを模擬しています。これはメモリ上だけに存在するファイルライクオブジェクトですが、通常のファイルと同じインターフェースを提供します。

例えば、ファイルと同様にイテレートして内容を読み出せます。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[1:27] hl[3,12:13,25] *}

/// note | 技術詳細

他の2つの変数 `image_base64` と `binary_image` は、画像を Base64 でエンコードし、それを `bytes` に変換してから `io.BytesIO` に渡したものです。

この例では1つのファイル内に完結させ、コピーしてそのまま実行できるようにするためだけのものです。 🥚

///

`with` ブロックを使うことで、ジェネレータ関数（`yield` を持つ関数）が終了した後、つまりレスポンス送信が完了した後に、そのファイルライクオブジェクトが確実にクローズされます。

この例では `io.BytesIO` によるメモリ内の疑似ファイルなので重要度は高くありませんが、実ファイルの場合は処理後に確実にクローズすることが重要です。

### ファイルと非同期 { #files-and-async }

多くの場合、ファイルライクオブジェクトはデフォルトでは async/await と互換性がありません。

例えば、`await file.read()` や `async for chunk in file` のような操作は提供されていません。

また、多くの場合、ディスクやネットワークから読み出すため、読み取りはブロッキング（イベントループをブロックし得る）処理になります。

/// info | 情報

上記の例は例外で、`io.BytesIO` は既にメモリ上にあるため、読み取りが何かをブロックすることはありません。

しかし多くの場合、ファイルやファイルライクオブジェクトの読み取りはブロッキングになります。

///

イベントループのブロッキングを避けるには、path operation 関数を `async def` ではなく通常の `def` で宣言してください。そうすると FastAPI はその関数をスレッドプールワーカー上で実行し、メインループのブロッキングを避けます。

{* ../../docs_src/stream_data/tutorial002_py310.py ln[30:34] hl[31] *}

/// tip | 豆知識

async 関数内からブロッキングなコードを呼び出す必要がある場合、あるいはブロッキングな関数内から async 関数を呼び出す必要がある場合は、FastAPI の兄弟ライブラリである [Asyncer](https://asyncer.tiangolo.com) を利用できます。

///

### `yield from` { #yield-from }

ファイルライクオブジェクトのようなものをイテレートして各要素に対して `yield` している場合、`for` ループを省略して、`yield from` で各要素をそのまま送ることもできます。

これは FastAPI 固有ではなく単なる Python の機能ですが、知っておくと便利な小ワザです。 😎

{* ../../docs_src/stream_data/tutorial002_py310.py ln[37:40] hl[40] *}
