# ボディ - 複数のパラメータ

これまで、`Path` と `Query` を見てきたので、より高度なリクエストボディの宣言の利用法を見ていきましょう。

## `Path`、 `Query` とボディパラメータを組み合わせる

もちろんですが、`Path`, `Query` や リクエストボディのパラメータの宣言は、自由に組み合わせることができ、**FastAPI** はそれを理解することができます。

そして、デフォルトを`None`に設定することで、ボディパラメータの宣言をオプションにすることも可能です。

=== "Python 3.10+"

    ```Python hl_lines="18-20"
    {!> ../../../docs_src/body_multiple_params/tutorial001_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="18-20"
    {!> ../../../docs_src/body_multiple_params/tutorial001_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="19-21"
    {!> ../../../docs_src/body_multiple_params/tutorial001_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="17-19"
    {!> ../../../docs_src/body_multiple_params/tutorial001_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="19-21"
    {!> ../../../docs_src/body_multiple_params/tutorial001.py!}
    ```

!!! note "備考"
    このケースでは、`item` はデフォルト値が `None` なので、オプションでボディから取得されることに注意してください。

## 複数のパラメータ

上の例で、*パス操作* は、 `Item`の属性に、下記のような単一のJSONボディを期待していました。

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

しかし、 `item` や `user` など、複数のボディパラメータを宣言することができます。

=== "Python 3.10+"

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial002_py310.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial002.py!}
    ```

このケースでは、**FastAPI** は関数内に１つ以上のボディパラメータが存在することを認識します。（２つのパラメータはPydanticのモデルにより作成されます。）

なので、ボディ内でパラメータの名前をキー（フィールド名）として使用することができます。下のようなボディが想定されます。

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

!!! note "備考"
    `item`は以前と同じように宣言されていますが、今回はJSONボディ内部で、`item`キーを使って宣言されていることに注意してください。


**FastAPI** はリクエストから自動的に変換を行うので、`item` パラメータの内容と、`user`パラメータの内容を受け取ります。

それにより、複合データのバリデーションが行われ、OpenAPIスキーマおよび自動ドキュメントに複合データが記録されます。

## ボディ内の単一の値

`Query` と `Path` がクエリパラメータやパスパラメータに追加のデータを定義するのと同様に、 **FastAPI** は `Body` を提供しています。

例えば、上のモデルを拡張して、`item` や `user` と同じJSONボディに `importance` という別のキーを宣言したいとします。

そのように宣言すると、単一の値なので、**FastAPI** はそれをクエリパラメータと認識します。

しかし、 `Body` を使うことで、JSONボディの別のキーとして扱うよう、**FastAPI** に教える事ができます。

=== "Python 3.10+"

    ```Python hl_lines="23"
    {!> ../../../docs_src/body_multiple_params/tutorial003_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="23"
    {!> ../../../docs_src/body_multiple_params/tutorial003_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="24"
    {!> ../../../docs_src/body_multiple_params/tutorial003_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="20"
    {!> ../../../docs_src/body_multiple_params/tutorial003_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="22"
    {!> ../../../docs_src/body_multiple_params/tutorial003.py!}
    ```

この場合、 **FastAPI** は下のようなボディを期待します。:

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

そして再び、データの種類を変換し、バリデーション、ドキュメンテーション等を行います。

## 複数のボディパラメータとクエリ

もちろん、必要であればいつでも、リクエストボディのパラメータに加えて、追加のクエリパラメータもボディパラメータに宣言することができます。

デフォルトでは、単一のバリューはクエリパラメータとして解釈されるので、明示的に `Query` を追加する必要はなく、下のように宣言するだけです。:

```Python
q: Union[str, None] = None
```

Or in Python 3.10 and above:

```Python
q: str | None = None
```

例:

=== "Python 3.10+"

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="28"
    {!> ../../../docs_src/body_multiple_params/tutorial004_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="25"
    {!> ../../../docs_src/body_multiple_params/tutorial004_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="27"
    {!> ../../../docs_src/body_multiple_params/tutorial004.py!}
    ```

!!! info "情報"
    `Body`は`Query`,`Path`や、後にみるものと全く同じように、追加のバリデーションや、メタデータパラメータを持っています。

## 単一のリクエストボディパラメータを埋め込む。

仮にPydanticモデル `item` から単一の `item` ボディパラメーターしか持っていないとします。

デフォルトでは、 **FastAPI** はボディを直接期待します。

しかし、追加のリクエストボディパラメータを宣言する際のように、JSONの中に item というキーを持ち、その中にモデルの内容がある形式のリクエストボディを期待したい場合、特別な `Body` パラメータである `embed` を使うことができます。

```Python
item: Item = Body(embed=True)
```

as in:

=== "Python 3.10+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005_an_py310.py!}
    ```

=== "Python 3.9+"

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005_an_py39.py!}
    ```

=== "Python 3.6+"

    ```Python hl_lines="18"
    {!> ../../../docs_src/body_multiple_params/tutorial005_an.py!}
    ```

=== "Python 3.10+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="15"
    {!> ../../../docs_src/body_multiple_params/tutorial005_py310.py!}
    ```

=== "Python 3.6+ non-Annotated"

    !!! tip "豆知識"
        可能であれば`Annotated`バージョンを使って下さい。

    ```Python hl_lines="17"
    {!> ../../../docs_src/body_multiple_params/tutorial005.py!}
    ```

この場合、 **FastAPI** は下のようなボディを想定します。:

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

このようにしてはいけません。:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2
}
```

## まとめ

リクエストが単一のボディしか持たなくても、複数のボディパラメータを *パス操作関数* に追加することができます。

しかし、 **FastAPI** はそれに対応し、関数内部に正しいデータを与え、*パス操作* における正確なスキーマのバリデーションと、ドキュメンテーションを提供します。

単一の値をボディの一部として受け取るように宣言することもできます。

単一のパラメータの宣言しかなくとも、キーの内部に、ボディを埋め込むよう、**FastAPI** に指示することができます。