# リクエストファイル

クライアントがアップロードするファイルは`File`を用いて定義することができます。

!!! info "情報"
    アップロードされたファイルを受信するには、まず<a href="https://andrew-d.github.io/python-multipart/" class="external-link" target="_blank">`python-multipart`</a>をインポートします。

    例えば`pip install python-multipart`のように。

    これはアップロードされたファイルが「フォームデータ」として送信されるためです。

## `File`のインポート

`fastapi`から`File`と`UploadFile`をインポートします:

```Python hl_lines="1"
{!../../../docs_src/request_files/tutorial001.py!}
```

## `File`パラメータを定義

ファイルパラメータは`Body`や`Form`と同じように作成します:

```Python hl_lines="7"
{!../../../docs_src/request_files/tutorial001.py!}
```

!!! info "情報"
    `File`は`Form`を直接継承するクラスです。

    しかし、`fastapi`から`Query`や`Path`、`File`などをインポートする場合、それらは実際には特殊なクラスを返す関数であることを覚えておいてください。

!!! tip "豆知識"
    ファイルのボディを宣言するには、`File`を使用する必要があります。なぜなら、パラメータがクエリパラメータやボディ（JSON）パラメータとして解釈されてしますからです。

ファイルは「フォームデータ」としてアップロードされます。

*path operation関数*のパラメータの型を`bytes`と宣言すると、**FastAPI** がファイルを読み込んで、`bytes`として内容を受け取ることになります。

これは、全体の内容がメモリに保存されることを意味することを覚えておいてください。これは小さなファイルの場合にはうまくいくでしょう。

`UploadFile`を使用することで恩恵を受けることができるケースがいくつかあります。

## `UploadFile`を持つ`File`パラメータ

`File`パラメータを`UploadFile`型で定義します:

```Python hl_lines="12"
{!../../../docs_src/request_files/tutorial001.py!}
```

`UploadFile`を使うことは`bytes`よりもいくつかの利点があります:

* それは「spooled」ファイルを使用しています:
    * サイズの上限までメモリに保存されたファイルで、上限を超えるとディスクに保存されます。
* 画像や動画、大きなバイナリなどの大きなファイルに対して、メモリを消費することなく動作することを意味します。
* アップロードされたファイルからメタデータを取得することができます。
* <a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">file-like</a>`async`インターフェースを持っています。
* これは実際のPythonの<a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a>オブジェクトを公開しており、ファイルライクなオブジェクトを期待する他のライブラリに直接渡すことができます。

### `UploadFile`

`UploadFile`は以下の属性を持っています:

* `filename`: アップロードされた元のファイル名を持つ`str`（例：`myimage.jpg`）。
* `content_type`: コンテンツタイプ（MIMEタイプ・メディアタイプ）を持つ`str`（例：`image/jpeg`）。
* `file`: <a href="https://docs.python.org/3/library/tempfile.html#tempfile.SpooledTemporaryFile" class="external-link" target="_blank">`SpooledTemporaryFile`</a> (<a href="https://docs.python.org/3/glossary.html#term-file-like-object" class="external-link" target="_blank">ファイルライク</a>オブジェクト)。これが実際のPythonファイルで、「ファイルライク」オブジェクトを期待する他の関数やライブラリに直接渡すことができます。

`UploadFile`は以下の`async`メソッドを持っています。これらはすべて（内部の`SpooledTemporaryFile`を使用して）その下にある対応するファイルメソッドを呼び出します。

* `write(data)`: ファイルに`data`（`str`または`bytes`）を書き込む。
* `read(size)`: ファイルの`size`（`int`）バイト・文字を読み込む。
* `seek(offset)`: ファイルのバイト位置`offset`（`int`）に移動します。
    * 例えば、`await myfile.seek(0)`はファイルの先頭に移動します。
    * これは、`await myfile.read()`を一度実行した後、再度内容を読み込む必要がある場合に特に有用です。
* `close()`: ファイルを閉じます。

これらのメソッドはすべて`async`メソッドなので、それらを「待機（await）」する必要があります。

例えば、`async`*path operation関数*の内部では、以下のようにして内容を取得することができます:

```Python
contents = await myfile.read()
```

通常の`def`*path operation関数*の内部にある場合、例えば、以下のように`UploadFile.file`に直接アクセスすることができます:

```Python
contents = myfile.file.read()
```

!!! note "`async` 技術詳細"
    `async`メソッドを使用すると、**FastAPI** はファイルメソッドをスレッドプールで実行し、それらを待機（`await`）します。

!!! note "Starlette 技術詳細"
    **FastAPI** の`UploadFile`は **Starlette** の`UploadFile`を直接継承していますが、**Pydantic** やFastAPIの他の部分と互換性を持たせるために必要な部分を追加しています。

## 「フォームデータ」とは

HTMLフォーム（`<form></form>`）がサーバにデータを送信する方法は、通常、そのデータに「特別な」エンコーディングを使用していますが、これはJSONとは異なります。

**FastAPI** は、JSONの代わりにそのデータを適切な場所から読み込むようにします。

!!! note "技術詳細"
    フォームからのデータは通常、`application/x-www-form-urlencoded`の「media type」を使用してエンコードされます。

    しかし、フォームがファイルを含む場合は、`multipart/form-data`としてエンコードされます。ファイルの扱いについては次の章で説明します。

    これらのエンコーディングやフォームフィールドの詳細については、<a href="https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST" class="external-link" target="_blank"><abbr title="Mozilla Developer Network">MDN</abbr>の<code>POST</code></a>のウェブドキュメントを参照してください。

!!! warning "注意"
    *path operation*で複数の`Form`パラメータを宣言することができますが、JSONとして受け取ることを期待している`Body`フィールドを宣言することはできません。なぜなら、リクエストは`application/json`の代わりに`application/x-www-form-urlencoded`を使ってボディをエンコードするからです。

    これは **FastAPI**の制限ではなく、HTTPプロトコルの制限の一部です。

## 複数ファイルのアップロード

複数のファイルを同時にアップロードすることも可能です。

これらは「フォームデータ」使用して送信された同じ「フォームフィールド」に関連づけられます。

これを利用するには、`bytes`の`List`または`UploadFile`を宣言します:

```Python hl_lines="10 15"
{!../../../docs_src/request_files/tutorial002.py!}
```

宣言された通り、`bytes`または`UploadFile`の`list`を受け取ります

!!! note "備考"
    2019-04-14現在、Swagger UIは同一フォームフィールド内での複数ファイルのアップロードに対応していないことに注意してください。詳しくは<a href="https://github.com/swagger-api/swagger-ui/issues/4276" class="external-link" target="_blank">#4276</a>と<a href="https://github.com/swagger-api/swagger-ui/issues/3641" class="external-link" target="_blank">#3641</a>を参照してください。

    それにもかかわらず、**FastAPI** は標準のOpenAPIを使用して、すでに互換性があります。

    そのため、Swagger UIが複数ファイルのアップロードサポートしていたり、OpenAPIをサポートしているツールがあれば、それらは **FastAPI** と互換性があります。

!!! note "技術詳細"
    また、`from starlette.responses import HTMLResponse`を使用することもできます。

    **FastAPI** は開発者の利便性を考慮して、`fastapi.responses`と同じ`starlette.responses`を提供しています。しかし、利用可能なレスポンスのほとんどはStarletteから直接提供されます。

## まとめ

入力パラメータとして（フォームデータとして）アップロードするファイルを宣言するには`File`を使用します。
