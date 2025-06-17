# クッキーパラメータモデル

もし関連する**複数のクッキー**から成るグループがあるなら、それらを宣言するために、**Pydanticモデル**を作成できます。🍪

こうすることで、**複数の場所**で**そのPydanticモデルを再利用**でき、バリデーションやメタデータを、すべてのクッキーパラメータに対して一度に宣言できます。😎

/// note | 備考

この機能は、FastAPIのバージョン `0.115.0` からサポートされています。🤓

///

/// tip | 豆知識

これと同じテクニックは `Query` 、 `Cookie` 、 `Header` にも適用できます。 😎

///

## クッキーにPydanticモデルを使用する

必要な複数の**クッキー**パラメータを**Pydanticモデル**で宣言し、さらに、それを `Cookie` として宣言しましょう:

{* ../../docs_src/cookie_param_models/tutorial001_an_py310.py hl[9:12,16] *}

**FastAPI**は、リクエストの**クッキー**から**それぞれのフィールド**のデータを**抽出**し、定義された**Pydanticモデル**を提供します。

## ドキュメントの確認

対話的APIドキュメントUI `/docs` で、定義されているクッキーを確認できます:

<div class="screenshot">
<img src="/img/tutorial/cookie-param-models/image01.png">
</div>

/// info | 備考


**ブラウザがクッキーを処理し**ていますが、特別な方法で内部的に処理を行っているために、**JavaScript**からは簡単に操作**できない**ことに留意してください。

**対話的APIドキュメントUI** `/docs` にアクセスすれば、*パスオペレーション*に関するクッキーの**ドキュメンテーション**を確認できます。

しかし、たとえ**クッキーデータを入力して**「Execute」をクリックしても、対話的APIドキュメントUIは**JavaScript**で動作しているためクッキーは送信されず、まるで値を入力しなかったかのような**エラー**メッセージが表示されます。

///

## 余分なクッキーを禁止する

特定の（あまり一般的ではないかもしれない）ケースで、受け付けるクッキーを**制限**する必要があるかもしれません。

あなたのAPIは独自の <abbr title="念のためですが、これはジョークです。クッキー同意とは関係ありませんが、APIでさえ不適切なクッキーを拒否できるとは愉快ですね。クッキーでも食べてください。🍪 （原文: This is a joke, just in case. It has nothing to do with cookie consents, but it's funny that even the API can now reject the poor cookies. Have a cookie. 🍪）">クッキー同意</abbr> を管理する能力を持っています。 🤪🍪

Pydanticのモデルの Configuration を利用して、 `extra` フィールドを `forbid` とすることができます。

{* ../../docs_src/cookie_param_models/tutorial002_an_py39.py hl[10] *}

もしクライアントが**余分なクッキー**を送ろうとすると、**エラー**レスポンスが返されます。

<abbr title="これもジョークです。気にしないでください。クッキーのお供にコーヒーでも飲んでください。☕ （原文: This is another joke. Don't pay attention to me. Have some coffee for your cookie. ☕）">どうせAPIに拒否されるのに</abbr>あなたの同意を得ようと精一杯努力する可哀想なクッキーバナーたち... 🍪

例えば、クライアントがクッキー `santa_tracker` を `good-list-please` という値で送ろうとすると、`santa_tracker` という <abbr title="サンタはクッキー不足を良しとはしないでしょう。🎅 はい、クッキージョークはもう止めておきます。（原文: Santa disapproves the lack of cookies. 🎅 Okay, no more cookie jokes.）">クッキーが許可されていない</abbr> ことを通知する**エラー**レスポンスが返されます:

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

## まとめ

**FastAPI**では、<abbr title="帰ってしまう前に最後のクッキーをどうぞ。🍪 （原文: Have a last cookie before you go. 🍪）">**クッキー**</abbr>を宣言するために、**Pydanticモデル**を使用できます。😎
