# エラーハンドリング { #handling-errors }

APIを使用しているクライアントにエラーを通知する必要がある状況はたくさんあります。

このクライアントは、フロントエンドを持つブラウザ、誰かのコード、IoTデバイスなどが考えられます。

クライアントに以下のようなことを伝える必要があるかもしれません:

* クライアントにはその操作のための十分な権限がありません。
* クライアントはそのリソースにアクセスできません。
* クライアントがアクセスしようとしていた項目が存在しません。
* など

これらの場合、通常は **400**（400から499）の範囲内の **HTTPステータスコード** を返すことになります。

これは200のHTTPステータスコード（200から299）に似ています。これらの「200」ステータスコードは、何らかの形でリクエスト「成功」であったことを意味します。

400の範囲にあるステータスコードは、クライアントからのエラーがあったことを意味します。

**"404 Not Found"** のエラー（およびジョーク）を覚えていますか？

## `HTTPException`の使用 { #use-httpexception }

HTTPレスポンスをエラーでクライアントに返すには、`HTTPException`を使用します。

### `HTTPException`のインポート { #import-httpexception }

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[1] *}

### コード内での`HTTPException`の発生 { #raise-an-httpexception-in-your-code }

`HTTPException`は通常のPythonの例外であり、APIに関連するデータを追加したものです。

Pythonの例外なので、`return`ではなく、`raise`です。

これはまた、*path operation関数*の内部で呼び出しているユーティリティ関数の内部から`HTTPException`を発生させた場合、*path operation関数*の残りのコードは実行されず、そのリクエストを直ちに終了させ、`HTTPException`からのHTTPエラーをクライアントに送信することを意味します。

値を返す`return`よりも例外を発生させることの利点は、「依存関係とセキュリティ」のセクションでより明確になります。

この例では、クライアントが存在しないIDでアイテムを要求した場合、`404`のステータスコードを持つ例外を発生させます:

{* ../../docs_src/handling_errors/tutorial001_py310.py hl[11] *}

### レスポンス結果 { #the-resulting-response }

クライアントが`http://example.com/items/foo`（`item_id` `"foo"`）をリクエストすると、HTTPステータスコードが200で、以下のJSONレスポンスが返されます:

```JSON
{
  "item": "The Foo Wrestlers"
}
```

しかし、クライアントが`http://example.com/items/bar`（存在しない`item_id` `"bar"`）をリクエストした場合、HTTPステータスコード404（"not found"エラー）と以下のJSONレスポンスが返されます:

```JSON
{
  "detail": "Item not found"
}
```

/// tip | 豆知識

`HTTPException`を発生させる際には、`str`だけでなく、JSONに変換できる任意の値を`detail`パラメータとして渡すことができます。

`dict`や`list`などを渡すことができます。

これらは **FastAPI** によって自動的に処理され、JSONに変換されます。

///

## カスタムヘッダーの追加 { #add-custom-headers }

例えば、いくつかのタイプのセキュリティのために、HTTPエラーにカスタムヘッダを追加できると便利な状況がいくつかあります。

おそらくコードの中で直接使用する必要はないでしょう。

しかし、高度なシナリオのために必要な場合には、カスタムヘッダーを追加することができます:

{* ../../docs_src/handling_errors/tutorial002_py310.py hl[14] *}

## カスタム例外ハンドラのインストール { #install-custom-exception-handlers }

カスタム例外ハンドラは<a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starletteと同じ例外ユーティリティ</a>を使用して追加することができます。

あなた（または使用しているライブラリ）が`raise`するかもしれないカスタム例外`UnicornException`があるとしましょう。

そして、この例外をFastAPIでグローバルに処理したいと思います。

カスタム例外ハンドラを`@app.exception_handler()`で追加することができます:

{* ../../docs_src/handling_errors/tutorial003_py310.py hl[5:7,13:18,24] *}

ここで、`/unicorns/yolo`をリクエストすると、*path operation*は`UnicornException`を`raise`します。

しかし、これは`unicorn_exception_handler`で処理されます。

そのため、HTTPステータスコードが`418`で、JSONの内容が以下のような明確なエラーを受け取ることになります:

```JSON
{"message": "Oops! yolo did something. There goes a rainbow..."}
```

/// note | 技術詳細

また、`from starlette.requests import Request`と`from starlette.responses import JSONResponse`を使用することもできます。

**FastAPI** は開発者の利便性を考慮して、`fastapi.responses`と同じ`starlette.responses`を提供しています。しかし、利用可能なレスポンスのほとんどはStarletteから直接提供されます。これは`Request`と同じです。

///

## デフォルトの例外ハンドラのオーバーライド { #override-the-default-exception-handlers }

**FastAPI** にはいくつかのデフォルトの例外ハンドラがあります。

これらのハンドラは、`HTTPException`を`raise`させた場合や、リクエストに無効なデータが含まれている場合にデフォルトのJSONレスポンスを返す役割を担っています。

これらの例外ハンドラを独自のものでオーバーライドすることができます。

### リクエスト検証の例外のオーバーライド { #override-request-validation-exceptions }

リクエストに無効なデータが含まれている場合、**FastAPI** は内部的に`RequestValidationError`を発生させます。

また、そのためのデフォルトの例外ハンドラも含まれています。

これをオーバーライドするには`RequestValidationError`をインポートして`@app.exception_handler(RequestValidationError)`と一緒に使用して例外ハンドラをデコレートします。

この例外ハンドラは`Request`と例外を受け取ります。

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[2,14:19] *}

これで、`/items/foo`にアクセスすると、以下のデフォルトのJSONエラーの代わりに:

```JSON
{
    "detail": [
        {
            "loc": [
                "path",
                "item_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ]
}
```

以下のテキスト版を取得します:

```
Validation errors:
Field: ('path', 'item_id'), Error: Input should be a valid integer, unable to parse string as an integer
```

### `HTTPException`エラーハンドラのオーバーライド { #override-the-httpexception-error-handler }

同様に、`HTTPException`ハンドラをオーバーライドすることもできます。

例えば、これらのエラーに対しては、JSONではなくプレーンテキストを返すようにすることができます:

{* ../../docs_src/handling_errors/tutorial004_py310.py hl[3:4,9:11,25] *}

/// note | 技術詳細

また、`from starlette.responses import PlainTextResponse`を使用することもできます。

**FastAPI** は開発者の利便性を考慮して、`fastapi.responses`と同じ`starlette.responses`を提供しています。しかし、利用可能なレスポンスのほとんどはStarletteから直接提供されます。

///

/// warning | 注意

`RequestValidationError`には、検証エラーが発生したファイル名と行番号の情報が含まれているため、必要であれば関連情報と一緒にログに表示できます。

しかし、そのまま文字列に変換して直接その情報を返すと、システムに関する情報が多少漏えいする可能性があります。そのため、ここではコードが各エラーを個別に抽出して表示します。

///

### `RequestValidationError`のボディの使用 { #use-the-requestvalidationerror-body }

`RequestValidationError`には無効なデータを含む`body`が含まれています。

アプリ開発中にボディのログを取ってデバッグしたり、ユーザーに返したりなどに使用することができます。

{* ../../docs_src/handling_errors/tutorial005_py310.py hl[14] *}

ここで、以下のような無効な項目を送信してみてください:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

受信したボディを含むデータが無効であることを示すレスポンスが表示されます:

```JSON hl_lines="12-15"
{
  "detail": [
    {
      "loc": [
        "body",
        "size"
      ],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ],
  "body": {
    "title": "towel",
    "size": "XL"
  }
}
```

#### FastAPIの`HTTPException`とStarletteの`HTTPException` { #fastapis-httpexception-vs-starlettes-httpexception }

**FastAPI**は独自の`HTTPException`を持っています。

また、 **FastAPI**の`HTTPException`エラークラスはStarletteの`HTTPException`エラークラスを継承しています。

唯一の違いは、**FastAPI** の`HTTPException`は`detail`フィールドにJSONに変換可能な任意のデータを受け付けるのに対し、Starletteの`HTTPException`は文字列のみを受け付けることです。

そのため、コード内では通常通り **FastAPI** の`HTTPException`を発生させ続けることができます。

しかし、例外ハンドラを登録する際には、Starletteの`HTTPException`に対して登録しておく必要があります。

これにより、Starletteの内部コードやStarletteの拡張機能やプラグインの一部がStarletteの`HTTPException`を発生させた場合、ハンドラがそれをキャッチして処理できるようになります。

この例では、同じコード内で両方の`HTTPException`を使用できるようにするために、Starletteの例外を`StarletteHTTPException`にリネームしています:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI** の例外ハンドラの再利用 { #reuse-fastapis-exception-handlers }

**FastAPI** から同じデフォルトの例外ハンドラと一緒に例外を使用したい場合は、`fastapi.exception_handlers`からデフォルトの例外ハンドラをインポートして再利用できます:

{* ../../docs_src/handling_errors/tutorial006_py310.py hl[2:5,15,21] *}

この例では、非常に表現力のあるメッセージでエラーを`print`しているだけですが、要点は理解できるはずです。例外を使用し、その後デフォルトの例外ハンドラを再利用できます。
