# ボディ - ネストされたモデル { #body-nested-models }

**FastAPI** を使用すると、深くネストされた任意のモデルを定義、検証、文書化、使用することができます（Pydanticのおかげです）。

## リストのフィールド { #list-fields }

属性をサブタイプとして定義することができます。例えば、Pythonの`list`:

{* ../../docs_src/body_nested_models/tutorial001_py310.py hl[12] *}

これにより、各項目の型は宣言されていませんが、`tags`はリストになります。

## タイプパラメータを持つリストのフィールド { #list-fields-with-type-parameter }

しかし、Pythonには内部の型、または「タイプパラメータ」を使ってリストを宣言するための特定の方法があります:

### タイプパラメータを持つ`list`の宣言 { #declare-a-list-with-a-type-parameter }

`list`、`dict`、`tuple`のようにタイプパラメータ（内部の型）を持つ型を宣言するには、
角括弧（`[`と`]`）を使って内部の型を「タイプパラメータ」として渡します。

```Python
my_list: list[str]
```

型宣言の標準的なPythonの構文はこれだけです。

内部の型を持つモデルの属性にも同じ標準の構文を使用してください。

そのため、以下の例では`tags`を具体的な「文字列のリスト」にすることができます:

{* ../../docs_src/body_nested_models/tutorial002_py310.py hl[12] *}

## セット型 { #set-types }

しかし、よく考えてみると、タグは繰り返すべきではなく、おそらくユニークな文字列になるのではないかと気付いたとします。

そして、Pythonにはユニークな項目のセットのための特別なデータ型`set`があります。

そして、`tags`を文字列のセットとして宣言できます:

{* ../../docs_src/body_nested_models/tutorial003_py310.py hl[12] *}

これを使えば、データが重複しているリクエストを受けた場合でも、ユニークな項目のセットに変換されます。

そして、そのデータを出力すると、たとえソースに重複があったとしても、固有の項目のセットとして出力されます。

また、それに応じて注釈をつけたり、文書化したりします。

## ネストされたモデル { #nested-models }

Pydanticモデルの各属性には型があります。

しかし、その型はそれ自体が別のPydanticモデルである可能性があります。

そのため、特定の属性名、型、バリデーションを指定して、深くネストしたJSON「オブジェクト」を宣言することができます。

すべては、任意のネストにされています。

### サブモデルの定義 { #define-a-submodel }

例えば、`Image`モデルを定義することができます:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[7:9] *}

### サブモデルを型として使用 { #use-the-submodel-as-a-type }

そして、それを属性の型として使用することができます:

{* ../../docs_src/body_nested_models/tutorial004_py310.py hl[18] *}

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

## 特殊な型とバリデーション { #special-types-and-validation }

`str`や`int`、`float`などの通常の単数型の他にも、`str`を継承したより複雑な単数型を使うこともできます。

すべてのオプションをみるには、<a href="https://docs.pydantic.dev/latest/concepts/types/" class="external-link" target="_blank">Pydanticの型の概要</a>を確認してください。次の章でいくつかの例をみることができます。

例えば、`Image`モデルのように`url`フィールドがある場合、`str`の代わりにPydanticの`HttpUrl`のインスタンスとして宣言することができます:

{* ../../docs_src/body_nested_models/tutorial005_py310.py hl[2,8] *}

文字列は有効なURLであることが確認され、そのようにJSON Schema / OpenAPIで文書化されます。

## サブモデルのリストを持つ属性 { #attributes-with-lists-of-submodels }

Pydanticモデルを`list`や`set`などのサブタイプとして使用することもできます:

{* ../../docs_src/body_nested_models/tutorial006_py310.py hl[18] *}

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

## 深くネストされたモデル { #deeply-nested-models }

深くネストされた任意のモデルを定義することができます:

{* ../../docs_src/body_nested_models/tutorial007_py310.py hl[7,12,18,21,25] *}

/// info | 情報

`Offer`は`Item`のリストであり、それらがさらにオプションの`Image`のリストを持っていることに注目してください。

///

## 純粋なリストのボディ { #bodies-of-pure-lists }

期待するJSONボディのトップレベルの値がJSON`array`（Pythonの`list`）であれば、Pydanticモデルと同じように、関数のパラメータで型を宣言することができます:

```Python
images: list[Image]
```

以下のように:

{* ../../docs_src/body_nested_models/tutorial008_py310.py hl[13] *}

## あらゆる場所でのエディタサポート { #editor-support-everywhere }

そして、あらゆる場所でエディタサポートを得られます。

以下のようにリストの中の項目でも:

<img src="/img/tutorial/body-nested-models/image01.png">

Pydanticモデルではなく、`dict`を直接使用している場合はこのようなエディタのサポートは得られません。

しかし、それらについて心配する必要はありません。入力されたdictは自動的に変換され、出力も自動的にJSONに変換されます。

## 任意の`dict`のボディ { #bodies-of-arbitrary-dicts }

また、ある型のキーと別の型の値を持つ`dict`としてボディを宣言することもできます。

この方法で、有効なフィールド/属性名を事前に知る必要がありません（Pydanticモデルの場合のように）。

これは、まだ知らないキーを受け取りたいときに便利です。

---

もうひとつ便利なケースは、別の型（例: `int`）のキーを持ちたい場合です。

それをここで見ていきます。

この場合、`int`のキーと`float`の値を持つものであれば、どんな`dict`でも受け入れることができます:

{* ../../docs_src/body_nested_models/tutorial009_py310.py hl[7] *}

/// tip | 豆知識

JSONはキーとして`str`しかサポートしていないことに注意してください。

しかしPydanticには自動データ変換機能があります。

これは、APIクライアントがキーとして文字列しか送信できなくても、それらの文字列に純粋な整数が含まれている限り、Pydanticが変換して検証することを意味します。

そして、`weights`として受け取る`dict`は、実際には`int`のキーと`float`の値を持つことになります。

///

## まとめ { #recap }

**FastAPI** を使用すると、Pydanticモデルが提供する最大限の柔軟性を持ちながら、コードをシンプルに短く、エレガントに保つことができます。

しかし、以下のような利点があります:

* エディタのサポート（どこでも補完！）
* データ変換（別名：構文解析 / シリアライズ）
* データの検証
* スキーマ文書
* 自動ドキュメント
