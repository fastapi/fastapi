# エラーハンドリング

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

## `HTTPException`の使用

HTTPレスポンスをエラーでクライアントに返すには、`HTTPException`を使用します。

### `HTTPException`のインポート

{* ../../docs_src/handling_errors/tutorial001.py hl[1] *}

### コード内での`HTTPException`の発生

`HTTPException`は通常のPythonの例外であり、APIに関連するデータを追加したものです。

Pythonの例外なので、`return`ではなく、`raise`です。

これはまた、*path operation関数*の内部で呼び出しているユーティリティ関数の内部から`HTTPException`を発生させた場合、*path operation関数*の残りのコードは実行されず、そのリクエストを直ちに終了させ、`HTTPException`からのHTTPエラーをクライアントに送信することを意味します。

値を返す`return`よりも例外を発生させることの利点は、「依存関係とセキュリティ」のセクションでより明確になります。

この例では、クライアントが存在しないIDでアイテムを要求した場合、`404`のステータスコードを持つ例外を発生させます:

{* ../../docs_src/handling_errors/tutorial001.py hl[11] *}

### レスポンス結果

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

## カスタムヘッダーの追加

例えば、いくつかのタイプのセキュリティのために、HTTPエラーにカスタムヘッダを追加できると便利な状況がいくつかあります。

おそらくコードの中で直接使用する必要はないでしょう。

しかし、高度なシナリオのために必要な場合には、カスタムヘッダーを追加することができます:

{* ../../docs_src/handling_errors/tutorial002.py hl[14] *}

## カスタム例外ハンドラのインストール

カスタム例外ハンドラは<a href="https://www.starlette.dev/exceptions/" class="external-link" target="_blank">Starletteと同じ例外ユーティリティ</a>を使用して追加することができます。

あなた（または使用しているライブラリ）が`raise`するかもしれないカスタム例外`UnicornException`があるとしましょう。

そして、この例外をFastAPIでグローバルに処理したいと思います。

カスタム例外ハンドラを`@app.exception_handler()`で追加することができます:

{* ../../docs_src/handling_errors/tutorial003.py hl[5,6,7,13,14,15,16,17,18,24] *}

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

## デフォルトの例外ハンドラのオーバーライド

**FastAPI** にはいくつかのデフォルトの例外ハンドラがあります。

これらのハンドラは、`HTTPException`を`raise`させた場合や、リクエストに無効なデータが含まれている場合にデフォルトのJSONレスポンスを返す役割を担っています。

これらの例外ハンドラを独自のものでオーバーライドすることができます。

### リクエスト検証の例外のオーバーライド

リクエストに無効なデータが含まれている場合、**FastAPI** は内部的に`RequestValidationError`を発生させます。

また、そのためのデフォルトの例外ハンドラも含まれています。

これをオーバーライドするには`RequestValidationError`をインポートして`@app.exception_handler(RequestValidationError)`と一緒に使用して例外ハンドラをデコレートします。

この例外ハンドラは`Requset`と例外を受け取ります。

{* ../../docs_src/handling_errors/tutorial004.py hl[2,14,15,16] *}

これで、`/items/foo`にアクセスすると、デフォルトのJSONエラーの代わりに以下が返されます:

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

以下のようなテキスト版を取得します:

```
1 validation error
path -> item_id
  value is not a valid integer (type=type_error.integer)
```

#### `RequestValidationError`と`ValidationError`

/// warning | 注意

これらは今のあなたにとって重要でない場合は省略しても良い技術的な詳細です。

///

`RequestValidationError`はPydanticの<a href="https://docs.pydantic.dev/latest/concepts/models/#error-handling" class="external-link" target="_blank">`ValidationError`</a>のサブクラスです。

**FastAPI** は`response_model`でPydanticモデルを使用していて、データにエラーがあった場合、ログにエラーが表示されるようにこれを使用しています。

しかし、クライアントやユーザーはそれを見ることはありません。その代わりに、クライアントはHTTPステータスコード`500`の「Internal Server Error」を受け取ります。

*レスポンス*やコードのどこか（クライアントの*リクエスト*ではなく）にPydanticの`ValidationError`がある場合、それは実際にはコードのバグなのでこのようにすべきです。

また、あなたがそれを修正している間は、セキュリティの脆弱性が露呈する場合があるため、クライアントやユーザーがエラーに関する内部情報にアクセスできないようにしてください。

### エラーハンドラ`HTTPException`のオーバーライド

同様に、`HTTPException`ハンドラをオーバーライドすることもできます。

例えば、これらのエラーに対しては、JSONではなくプレーンテキストを返すようにすることができます:

{* ../../docs_src/handling_errors/tutorial004.py hl[3,4,9,10,11,22] *}

/// note | 技術詳細

また、`from starlette.responses import PlainTextResponse`を使用することもできます。

**FastAPI** は開発者の利便性を考慮して、`fastapi.responses`と同じ`starlette.responses`を提供しています。しかし、利用可能なレスポンスのほとんどはStarletteから直接提供されます。

///

### `RequestValidationError`のボディの使用

`RequestValidationError`には無効なデータを含む`body`が含まれています。

アプリ開発中に本体のログを取ってデバッグしたり、ユーザーに返したりなどに使用することができます。

{* ../../docs_src/handling_errors/tutorial005.py hl[14] *}

ここで、以下のような無効な項目を送信してみてください:

```JSON
{
  "title": "towel",
  "size": "XL"
}
```

受信したボディを含むデータが無効であることを示すレスポンスが表示されます:

```JSON hl_lines="12 13 14 15"
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

#### FastAPIの`HTTPException`とStarletteの`HTTPException`

**FastAPI**は独自の`HTTPException`を持っています。

また、 **FastAPI**のエラークラス`HTTPException`はStarletteのエラークラス`HTTPException`を継承しています。

唯一の違いは、**FastAPI** の`HTTPException`はレスポンスに含まれるヘッダを追加できることです。

これはOAuth 2.0といくつかのセキュリティユーティリティのために内部的に必要とされ、使用されています。

そのため、コード内では通常通り **FastAPI** の`HTTPException`を発生させ続けることができます。

しかし、例外ハンドラを登録する際には、Starletteの`HTTPException`を登録しておく必要があります。

これにより、Starletteの内部コードやStarletteの拡張機能やプラグインの一部が`HTTPException`を発生させた場合、ハンドラがそれをキャッチして処理することができるようになります。

以下の例では、同じコード内で両方の`HTTPException`を使用できるようにするために、Starletteの例外の名前を`StarletteHTTPException`に変更しています:

```Python
from starlette.exceptions import HTTPException as StarletteHTTPException
```

### **FastAPI** の例外ハンドラの再利用

また、何らかの方法で例外を使用することもできますが、**FastAPI** から同じデフォルトの例外ハンドラを使用することもできます。

デフォルトの例外ハンドラを`fastapi.exception_handlers`からインポートして再利用することができます:

{* ../../docs_src/handling_errors/tutorial006.py hl[2,3,4,5,15,21] *}

この例では、非常に表現力のあるメッセージでエラーを`print`しています。

しかし、例外を使用して、デフォルトの例外ハンドラを再利用することができるということが理解できます。
