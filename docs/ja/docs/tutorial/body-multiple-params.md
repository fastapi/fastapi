# ボディ - 複数のパラメータ

これまで`Path`と`Query`をどう使うかを見てきましたが、リクエストボディの宣言のより高度な使い方を見てみましょう。

## `Path`、`Query`とボディパラメータを混ぜる

まず、もちろん、`Path`と`Query`とリクエストボディのパラメータの宣言は自由に混ぜることができ、 **FastAPI** は何をするべきかを知っています。

また、デフォルトの`None`を設定することで、ボディパラメータをオプションとして宣言することもできます:

{* ../../docs_src/body_multiple_params/tutorial001.py hl[19,20,21] *}

/// note | 備考

この場合、ボディから取得する`item`はオプションであることに注意してください。デフォルト値は`None`です。

///

## 複数のボディパラメータ

上述の例では、*path operations*は`item`の属性を持つ以下のようなJSONボディを期待していました:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

しかし、`item`と`user`のように複数のボディパラメータを宣言することもできます:

{* ../../docs_src/body_multiple_params/tutorial002.py hl[22] *}

この場合、**FastAPI**は関数内に複数のボディパラメータ（Pydanticモデルである２つのパラメータ）があることに気付きます。

そのため、パラメータ名をボディのキー（フィールド名）として使用し、以下のようなボディを期待しています:

```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
```

/// note | 備考

以前と同じように`item`が宣言されていたにもかかわらず、`item`はキー`item`を持つボディの内部にあることが期待されていることに注意してください。

///

**FastAPI** はリクエストから自動で変換を行い、パラメータ`item`が特定の内容を受け取り、`user`も同じように特定の内容を受け取ります。

複合データの検証を行い、OpenAPIスキーマや自動ドキュメントのように文書化してくれます。

## ボディ内の単数値

クエリとパスパラメータの追加データを定義するための `Query` と `Path` があるのと同じように、 **FastAPI** は同等の `Body` を提供します。

例えば、前のモデルを拡張して、同じボディに `item` と `user` の他にもう一つのキー `importance` を入れたいと決めることができます。

単数値なのでそのまま宣言すると、**FastAPI** はそれがクエリパラメータであるとみなします。

しかし、`Body`を使用して、**FastAPI** に別のボディキーとして扱うように指示することができます:


{* ../../docs_src/body_multiple_params/tutorial003.py hl[23] *}

この場合、**FastAPI** は以下のようなボディを期待します:


```JSON
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
```

繰り返しになりますが、データ型の変換、検証、文書化などを行います。

## 複数のボディパラメータとクエリ

もちろん、ボディパラメータに加えて、必要に応じて追加のクエリパラメータを宣言することもできます。

デフォルトでは、単数値はクエリパラメータとして解釈されるので、明示的に `Query` を追加する必要はありません。

```Python
q: str = None
```

以下において:

{* ../../docs_src/body_multiple_params/tutorial004.py hl[27] *}

/// info | 情報

`Body`もまた、後述する `Query` や `Path` などと同様に、すべての検証パラメータとメタデータパラメータを持っています。

///

## 単一のボディパラメータの埋め込み

Pydanticモデル`Item`のボディパラメータ`item`を1つだけ持っているとしましょう。

デフォルトでは、**FastAPI**はそのボディを直接期待します。

しかし、追加のボディパラメータを宣言したときのように、キー `item` を持つ JSON とその中のモデルの内容を期待したい場合は、特別な `Body` パラメータ `embed` を使うことができます:

```Python
item: Item = Body(..., embed=True)
```

以下において:

{* ../../docs_src/body_multiple_params/tutorial005.py hl[17] *}

この場合、**FastAPI** は以下のようなボディを期待します:

```JSON hl_lines="2"
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
```

以下の代わりに:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## まとめ

リクエストが単一のボディしか持てない場合でも、*path operation関数*に複数のボディパラメータを追加することができます。

しかし、**FastAPI** はそれを処理し、関数内の正しいデータを与え、*path operation*内の正しいスキーマを検証し、文書化します。

また、ボディの一部として受け取る単数値を宣言することもできます。

また、単一のパラメータしか宣言されていない場合でも、ボディをキーに埋め込むように **FastAPI** に指示することができます。
