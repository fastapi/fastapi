# リクエストファイル { #request-files }

`File` を使って、クライアントがアップロードするファイルを定義できます。

/// info | 情報

アップロードされたファイルを受け取るには、まず <a href="https://github.com/Kludex/python-multipart" class="external-link" target="_blank">`python-multipart`</a> をインストールします。

[仮想環境](../virtual-environments.md){.internal-link target=_blank}を作成して有効化し、次のようにインストールしてください:

```console
$ pip install python-multipart
```

アップロードされたファイルは「form data」として送信されるためです。

///

## `File` をインポート { #import-file }

`fastapi` から `File` と `UploadFile` をインポートします:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[3] *}

## `File` パラメータの定義 { #define-file-parameters }

`Body` や `Form` と同様の方法でファイルのパラメータを作成します:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[9] *}

/// info | 情報

`File` は `Form` を直接継承したクラスです。

ただし、`fastapi` から `Query`、`Path`、`File` などをインポートするとき、それらは実際には特殊なクラスを返す関数であることに注意してください。

///

/// tip | 豆知識

ファイルのボディを宣言するには `File` を使う必要があります。そうしないと、パラメータはクエリパラメータやボディ（JSON）パラメータとして解釈されます。

///

ファイルは「form data」としてアップロードされます。

*path operation 関数* のパラメータの型を `bytes` として宣言すると、**FastAPI** がファイルを読み取り、内容を `bytes` として受け取ります。

これは内容全体がメモリに保持されることを意味します。小さなファイルには有効です。

しかし、多くの場合は `UploadFile` を使う方が有利です。

## `UploadFile` によるファイルパラメータ { #file-parameters-with-uploadfile }

型を `UploadFile` にしてファイルパラメータを定義します:

{* ../../docs_src/request_files/tutorial001_an_py310.py hl[14] *}

`UploadFile` を使うことには `bytes` に対する次の利点があります:

- パラメータのデフォルト値に `File()` を使う必要がありません。
- 「spooled」ファイルを使います:
    - 最大サイズまではメモリに保持し、それを超えるとディスクに格納されるファイルです。
- そのため、画像・動画・大きなバイナリなどの大きなファイルでも、メモリを使い果たすことなくうまく動作します。
- アップロードされたファイルからメタデータを取得できます。
- <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> な `async` インターフェースを持ちます。
- 実際の Python の <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> オブジェクトを公開しており、file-like オブジェクトを期待する他のライブラリにそのまま渡せます。

### `UploadFile` { #uploadfile }

`UploadFile` には次の属性があります:

- `filename`: アップロード時の元のファイル名を表す `str`（例: `myimage.jpg`）
- `content_type`: コンテントタイプ（MIME タイプ / メディアタイプ）を表す `str`（例: `image/jpeg`）
- `file`: <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>（<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a> なオブジェクト）。これは実際の Python のファイルオブジェクトで、「file-like」オブジェクトを期待する関数やライブラリに直接渡せます。

`UploadFile` には次の `async` メソッドがあります。いずれも内部で対応するファイルメソッド（内部の `SpooledTemporaryFile`）を呼び出します。

- `write(data)`: `data`（`str` または `bytes`）を書き込みます。
- `read(size)`: `size`（`int`）バイト/文字を読み込みます。
- `seek(offset)`: ファイル内のバイト位置 `offset`（`int`）に移動します。
    - 例: `await myfile.seek(0)` はファイルの先頭に移動します。
    - 一度 `await myfile.read()` を実行して、もう一度内容を読みたい場合に特に便利です。
- `close()`: ファイルを閉じます。

これらはすべて `async` メソッドなので、`await` する必要があります。

例えば、`async` の *path operation 関数* 内では次のように内容を取得できます:

```Python
contents = await myfile.read()
```

通常の `def` の *path operation 関数* 内にいる場合は、`UploadFile.file` に直接アクセスできます。例えば:

```Python
contents = myfile.file.read()
```

/// note | `async` の技術詳細

`async` メソッドを使うと、**FastAPI** はファイルメソッドをスレッドプールで実行し、その完了を待機します。

///

/// note | Starlette の技術詳細

**FastAPI** の `UploadFile` は **Starlette** の `UploadFile` を直接継承していますが、**Pydantic** や FastAPI の他の部分と互換にするために必要な要素を追加しています。

///

## 「Form Data」とは { #what-is-form-data }

HTML フォーム（`<form></form>`）がサーバーにデータを送る方法は、そのデータに対して通常「特別な」エンコーディングを用い、JSON とは異なります。

**FastAPI** は JSON ではなく、適切な場所からそのデータを読み取るようにします。

/// note | 技術詳細

ファイルを含まない場合、フォームからのデータは通常「メディアタイプ」`application/x-www-form-urlencoded` でエンコードされます。

ただしフォームにファイルが含まれる場合は、`multipart/form-data` としてエンコードされます。`File` を使うと、**FastAPI** はボディ内の正しい部分からファイルを取得すべきであると認識します。

これらのエンコーディングやフォームフィールドの詳細は、<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network - Mozilla 開発者ネットワーク">MDN</abbr> Web Docs の <code>POST</code></a> を参照してください。

///

/// warning | 注意

1 つの *path operation* に複数の `File` および `Form` パラメータを宣言できますが、同時に JSON として受け取ることを期待する `Body` フィールドを宣言することはできません。リクエストのボディは `application/json` ではなく `multipart/form-data` でエンコードされるためです。

これは **FastAPI** の制限ではなく、HTTP プロトコルの仕様です。

///

## 任意のファイルアップロード { #optional-file-upload }

標準の型アノテーションを使い、デフォルト値を `None` に設定することで、ファイルを任意にできます:

{* ../../docs_src/request_files/tutorial001_02_an_py310.py hl[9,17] *}

## 追加メタデータつきの `UploadFile` { #uploadfile-with-additional-metadata }

例えば追加のメタデータを設定するために、`UploadFile` と併せて `File()` を使うこともできます:

{* ../../docs_src/request_files/tutorial001_03_an_py310.py hl[9,15] *}

## 複数ファイルのアップロード { #multiple-file-uploads }

同時に複数のファイルをアップロードできます。

それらは「form data」で送信される同じ「フォームフィールド」に関連付けられます。

そのためには、`bytes` または `UploadFile` のリストを宣言します:

{* ../../docs_src/request_files/tutorial002_an_py310.py hl[10,15] *}

宣言どおり、`bytes` または `UploadFile` の `list` を受け取ります。

/// note | 技術詳細

`from starlette.responses import HTMLResponse` を使うこともできます。

**FastAPI** は利便性のため、`starlette.responses` と同じものを `fastapi.responses` として提供しています。ただし、利用可能なレスポンスの多くは Starlette から直接提供されています。

///

### 追加メタデータつきの複数ファイルアップロード { #multiple-file-uploads-with-additional-metadata }

先ほどと同様に、`UploadFile` に対しても `File()` を使って追加のパラメータを設定できます:

{* ../../docs_src/request_files/tutorial003_an_py310.py hl[11,18:20] *}

## まとめ { #recap }

リクエストでフォームデータとして送信されるアップロードファイルを宣言するには、`File`、`bytes`、`UploadFile` を使います。
