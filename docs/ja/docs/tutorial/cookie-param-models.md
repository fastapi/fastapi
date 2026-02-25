# クッキーパラメータモデル { #cookie-parameter-models }

もし関連する**複数のクッキー**から成るグループがあるなら、それらを宣言するために、**Pydanticモデル**を作成できます。🍪

こうすることで、**複数の場所**で**そのPydanticモデルを再利用**でき、バリデーションやメタデータを、すべてのパラメータに対して一度に宣言できます。😎

/// note | 備考

この機能は、FastAPIのバージョン `0.115.0` からサポートされています。🤓

///

/// tip | 豆知識

これと同じテクニックは `Query` 、 `Cookie` 、 `Header` にも適用できます。 😎

///

## Pydanticモデルを使用したクッキー { #cookies-with-a-pydantic-model }

必要な複数の**クッキー**パラメータを**Pydanticモデル**で宣言し、さらに、パラメータを `Cookie` として宣言しましょう:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI**は、リクエストで受け取った**クッキー**から**それぞれのフィールド**のデータを**抽出**し、定義したPydanticモデルを提供します。

## ドキュメントの確認 { #check-the-docs }

対話的APIドキュメントUI `/docs` で、定義されているクッキーを確認できます:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | 情報

**ブラウザがクッキーを処理し**ていますが、特別な方法で内部的に処理を行っているために、**JavaScript**からは簡単に操作**できない**ことに留意してください。

**APIドキュメントUI** `/docs` にアクセスすれば、*path operation*に関するクッキーの**ドキュメンテーション**を確認できます。

しかし、たとえ**データを入力して**「Execute」をクリックしても、ドキュメントUIは**JavaScript**で動作しているためクッキーは送信されず、まるで値を入力しなかったかのような**エラー**メッセージが表示されます。

///

## 余分なクッキーを禁止する { #forbid-extra-cookies }

特定の（あまり一般的ではないかもしれない）ケースで、受け付けるクッキーを**制限**する必要があるかもしれません。

あなたのAPIは独自の <dfn title="念のためですが、これはジョークです。クッキー同意とは関係ありませんが、APIでさえ今やかわいそうなクッキーを拒否できるのは面白いですね。クッキーでもどうぞ。🍪">クッキー同意</dfn> を管理する能力を持っています。 🤪🍪

Pydanticのモデルの Configuration を利用して、 `extra` フィールドを `forbid` とすることができます。

{* ../../docs_src/cookie_param_models/tutorial002_an_py310.py hl[10] *}

もしクライアントが**余分なクッキー**を送ろうとすると、**エラー**レスポンスが返されます。

<dfn title="これもジョークです。気にしないでください。クッキーのお供にコーヒーでもどうぞ。☕">どうせAPIに拒否されるのに</dfn>あなたの同意を得ようと精一杯努力する可哀想なクッキーバナーたち... 🍪

例えば、クライアントがクッキー `santa_tracker` を `good-list-please` という値で送ろうとすると、`santa_tracker` という <dfn title="サンタはクッキー不足を良しとしません。🎅 はい、クッキージョークはこれでおしまい。">クッキーが許可されていない</dfn> ことを通知する**エラー**レスポンスが返されます:

```json
{
    "detail": [
        {
            "type": "extra_forbidden",
            "loc": ["cookie", "santa_tracker"],
            "msg": "Extra inputs are not permitted",
            "input": "good-list-please",
        }
    ]
}
```

## まとめ { #summary }

**FastAPI**では、<dfn title="帰る前に最後のクッキーをどうぞ。🍪">**クッキー**</dfn>を宣言するために、**Pydanticモデル**を使用できます。😎
