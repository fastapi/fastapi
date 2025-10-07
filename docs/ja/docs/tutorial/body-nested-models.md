# ボディ - ネストされたモデル

**FastAPI** を使用すると、深くネストされた任意のモデルを定義、検証、文書化、使用することができます（Pydanticのおかげです）。

## リストのフィールド

属性をサブタイプとして定義することができます。例えば、Pythonの`list`は以下のように定義できます:

{* ../../docs_src/body_nested_models/tutorial001.py hl[12] *}

これにより、各項目の型は宣言されていませんが、`tags`はある項目のリストになります。

## タイプパラメータを持つリストのフィールド

しかし、Pythonには型や「タイプパラメータ」を使ってリストを宣言する方法があります:

### typingの`List`をインポート

まず、Pythonの標準の`typing`モジュールから`List`をインポートします:

{* ../../docs_src/body_nested_models/tutorial002.py hl[1] *}

### タイプパラメータを持つ`List`の宣言

`list`や`dict`、`tuple`のようなタイプパラメータ（内部の型）を持つ型を宣言するには:

* `typing`モジュールからそれらをインストールします。
* 角括弧（`[`と`]`）を使って「タイプパラメータ」として内部の型を渡します:

```Python
from typing import List

my_list: List[str]
```

型宣言の標準的なPythonの構文はこれだけです。

内部の型を持つモデルの属性にも同じ標準の構文を使用してください。

そのため、以下の例では`tags`を具体的な「文字列のリスト」にすることができます:

{* ../../docs_src/body_nested_models/tutorial002.py hl[14] *}

## セット型

しかし、よく考えてみると、タグは繰り返すべきではなく、おそらくユニークな文字列になるのではないかと気付いたとします。

そして、Pythonにはユニークな項目のセットのための特別なデータ型`set`があります。

そのため、以下のように、`Set`をインポートして`str`の`set`として`tags`を宣言することができます:

{* ../../docs_src/body_nested_models/tutorial003.py hl[1,14] *}

これを使えば、データが重複しているリクエストを受けた場合でも、ユニークな項目のセットに変換されます。

そして、そのデータを出力すると、たとえソースに重複があったとしても、固有の項目のセットとして出力されます。

また、それに応じて注釈をつけたり、文書化したりします。

## ネストされたモデル

Pydanticモデルの各属性には型があります。

しかし、その型はそれ自体が別のPydanticモデルである可能性があります。

そのため、特定の属性名、型、バリデーションを指定して、深くネストしたJSON`object`を宣言することができます。

すべては、任意のネストにされています。

### サブモデルの定義

例えば、`Image`モデルを定義することができます:

{* ../../docs_src/body_nested_models/tutorial004.py hl[9,10,11] *}

### サブモデルを型として使用

そして、それを属性の型として使用することができます:

{* ../../docs_src/body_nested_models/tutorial004.py hl[20] *}

これは **FastAPI** が以下のようなボディを期待することを意味します:

```JSON
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": ["rock", "metal", "bar"],
    "image": {
        "url": "http://example.com/baz.jpg",
        "name": "The Foo live"
    }
}
```

繰り返しになりますが、**FastAPI** を使用して、その宣言を行うだけで以下のような恩恵を受けられます:

* ネストされたモデルでも対応可能なエディタのサポート（補完など）
* データ変換
* データの検証
* 自動文書化

## 特殊な型とバリデーション

`str`や`int`、`float`のような通常の単数型の他にも、`str`を継承したより複雑な単数型を使うこともできます。

すべてのオプションをみるには、<a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydanticのエキゾチック な型</a>のドキュメントを確認してください。次の章でいくつかの例をみることができます。

例えば、`Image`モデルのように`url`フィールドがある場合、`str`の代わりにPydanticの`HttpUrl`を指定することができます:

{* ../../docs_src/body_nested_models/tutorial005.py hl[4,10] *}

文字列は有効なURLであることが確認され、そのようにJSONスキーマ・OpenAPIで文書化されます。

## サブモデルのリストを持つ属性

Pydanticモデルを`list`や`set`などのサブタイプとして使用することもできます:

{* ../../docs_src/body_nested_models/tutorial006.py hl[20] *}

これは、次のようなJSONボディを期待します（変換、検証、ドキュメントなど）:

```JSON hl_lines="11"
{
    "name": "Foo",
    "description": "The pretender",
    "price": 42.0,
    "tax": 3.2,
    "tags": [
        "rock",
        "metal",
        "bar"
    ],
    "images": [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
}
```

/// info | 情報

`images`キーが画像オブジェクトのリストを持つようになったことに注目してください。

///

## 深くネストされたモデル

深くネストされた任意のモデルを定義することができます:

{* ../../docs_src/body_nested_models/tutorial007.py hl[9,14,20,23,27] *}

/// info | 情報

`Offer`は`Item`のリストであり、オプションの`Image`のリストを持っていることに注目してください。

///

## 純粋なリストのボディ

期待するJSONボディのトップレベルの値がJSON`array`（Pythonの`list`）であれば、Pydanticモデルと同じように、関数のパラメータで型を宣言することができます:

```Python
images: List[Image]
```

以下のように:

{* ../../docs_src/body_nested_models/tutorial008.py hl[15] *}

## あらゆる場所でのエディタサポート

エディタのサポートもどこでも受けることができます。

以下のようにリストの中の項目でも:

<img src="https://fastapi.tiangolo.com/img/tutorial/body-nested-models/image01.png">

Pydanticモデルではなく、`dict`を直接使用している場合はこのようなエディタのサポートは得られません。

しかし、それらについて心配する必要はありません。入力された辞書は自動的に変換され、出力も自動的にJSONに変換されます。

## 任意の`dict`のボディ

また、ある型のキーと別の型の値を持つ`dict`としてボディを宣言することもできます。

有効なフィールド・属性名を事前に知る必要がありません（Pydanticモデルの場合のように）。

これは、まだ知らないキーを受け取りたいときに便利だと思います。

---

他にも、`int`のように他の型のキーを持ちたい場合などに便利です。

それをここで見ていきましょう。

この場合、`int`のキーと`float`の値を持つものであれば、どんな`dict`でも受け入れることができます:

{* ../../docs_src/body_nested_models/tutorial009.py hl[15] *}

/// tip | 豆知識

JSONはキーとして`str`しかサポートしていないことに注意してください。

しかしPydanticには自動データ変換機能があります。

これは、APIクライアントがキーとして文字列しか送信できなくても、それらの文字列に純粋な整数が含まれている限り、Pydanticが変換して検証することを意味します。

そして、`weights`として受け取る`dict`は、実際には`int`のキーと`float`の値を持つことになります。

///

## まとめ

**FastAPI** を使用すると、Pydanticモデルが提供する最大限の柔軟性を持ちながら、コードをシンプルに短く、エレガントに保つことができます。

以下のような利点があります:

* エディタのサポート（どこでも補完！）
* データ変換（別名：構文解析・シリアライズ）
* データの検証
* スキーマ文書
* 自動文書化
