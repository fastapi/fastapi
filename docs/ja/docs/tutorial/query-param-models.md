# クエリパラメータモデル { #query-parameter-models }

もし関連する**複数のクエリパラメータ**から成るグループがあるなら、それらを宣言するために、**Pydanticモデル**を作成できます。

こうすることで、**複数の場所**で**そのモデルを再利用**でき、バリデーションやメタデータを、すべてのパラメータに対して一度に宣言できます。😎

/// note | 備考

この機能は、FastAPIのバージョン `0.115.0` からサポートされています。🤓

///

## Pydanticモデルを使ったクエリパラメータ { #query-parameters-with-a-pydantic-model }

必要な**クエリパラメータ**を**Pydanticモデル**で宣言し、さらに、そのパラメータを `Query` として宣言しましょう:

{* ../../docs_src/query_param_models/tutorial001_an_py310.py hl[9:13,17] *}

**FastAPI**は、リクエストの**クエリパラメータ**からそれぞれの**フィールド**のデータを**抽出**し、定義したPydanticモデルを提供します。

## ドキュメントの確認 { #check-the-docs }

対話的APIドキュメント `/docs` でクエリパラメータを確認できます:

<div class="screenshot">
<img src="/img/tutorial/query-param-models/image01.png">
</div>

## 余分なクエリパラメータを禁止する { #forbid-extra-query-parameters }

特定の（あまり一般的ではないかもしれない）ユースケースで、受け取りたいクエリパラメータを**制限**したい場合があります。

Pydanticのモデル設定を使って、あらゆる `extra` フィールドを `forbid` にできます。

{* ../../docs_src/query_param_models/tutorial002_an_py310.py hl[10] *}

もしクライアントが**クエリパラメータ**として**余分な**データを送ろうとすると、**エラー**レスポンスが返されます。

例えば、クライアントがクエリパラメータ `tool` に、値 `plumbus` を設定して送ろうとすると:

```http
https://example.com/items/?limit=10&tool=plumbus
```

クエリパラメータ `tool` が許可されていないことを伝える**エラー**レスポンスが返されます。

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["query", "tool"],
            "msg": "Extra inputs are not permitted",
            "input": "plumbus"
        }
    ]
}
```

## パラメータモデルの組み合わせ { #combine-parameter-models }

複数のクエリパラメータモデルを宣言し、個別のクエリパラメータや依存関係と組み合わせることができます。

{* ../../docs_src/query_param_models/tutorial003_an_py310.py hl[9:15,20:22] *}

リクエストパラメータは同じ階層のままです。

```http
https://example.com/items/?limit=5&offset=10&tags=red&tags=blue&search=shirt
```

クエリ文字列に `pagination` や `filters` キーはありません。各モデルは、それぞれのデフォルト値、フィールドバリデータ、モデルバリデータを使って、クエリパラメータを独立して検証します。モデルや個別のパラメータを依存関係で宣言した場合も同様です。

複数のモデルがパラメータ名やエイリアスを共有している場合、各モデルはそのリクエストパラメータを独立して検証します。独立した値には、異なる名前やエイリアスを使用してください。OpenAPIでは、依存関係と共有するパラメータと同様に、共有パラメータは一度だけ記載されるため、共有する宣言では同じ型と制約を記述する必要があります。

各モデルの `extra` 設定は、他のモデルや依存関係で宣言されたものも含め、すべてのクエリパラメータに適用されます。`extra="forbid"` の場合、そのモデルに含まれないパラメータはすべて拒否されます。`extra="allow"` の場合、それらのパラメータはモデルの余分なフィールドとして含まれます。

これは `Header` モデルと `Cookie` モデルでも機能します。

## 任意のクエリパラメータモデル { #optional-query-parameter-models }

クエリパラメータモデルに `| None` とデフォルト値 `None` を指定して宣言すると、そのグループを任意にできます。

{* ../../docs_src/query_param_models/tutorial004_an_py310.py hl[18] *}

`start` も `end` も送信されない場合、`date_range` は `None` になります。どちらかが送信された場合、FastAPIはモデルを検証し、両方のフィールドを必須とします。

デフォルト値なしで `| None` を使用した場合、パラメータは引き続き必須です。

余分なパラメータはモデルの `extra` 設定に従います。無視される余分なパラメータがあっても、モデルが存在するとはみなされません。

OpenAPIでは、グループのフィールドが個別に記載され、任意としてマークされます。

任意の[ヘッダーパラメータモデル](header-param-models.md#optional-header-parameter-models)や[クッキーパラメータモデル](cookie-param-models.md#optional-cookie-parameter-models)も宣言できます。

## まとめ { #summary }

**FastAPI**では、**クエリパラメータ**を宣言するために、**Pydanticモデル**を使用できます。😎

/// tip | 豆知識

ネタバレ注意: Pydanticモデルはクッキーやヘッダーの宣言にも使用できますが、その内容については後のチュートリアルで学びます。🤫

///
