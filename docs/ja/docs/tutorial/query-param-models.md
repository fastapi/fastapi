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

## まとめ { #summary }

**FastAPI**では、**クエリパラメータ**を宣言するために、**Pydanticモデル**を使用できます。😎

/// tip | 豆知識

ネタバレ注意: Pydanticモデルはクッキーやヘッダーの宣言にも使用できますが、その内容については後のチュートリアルで学びます。🤫

///
