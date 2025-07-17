# 依存関係としてのクラス

**依存性注入** システムを深く掘り下げる前に、先ほどの例をアップグレードしてみましょう。

## 前の例の`dict`

前の例では、依存関係（"dependable"）から`dict`を返していました:

{* ../../docs_src/dependencies/tutorial001.py hl[9] *}

しかし、*path operation関数*のパラメータ`commons`に`dict`が含まれています。

また、エディタは`dict`のキーと値の型を知ることができないため、多くのサポート（補完のような）を提供することができません。

もっとうまくやれるはずです...。

## 依存関係を作るもの

これまでは、依存関係が関数として宣言されているのを見てきました。

しかし、依存関係を定義する方法はそれだけではありません（その方が一般的かもしれませんが）。

重要なのは、依存関係が「呼び出し可能」なものであることです。

Pythonにおける「**呼び出し可能**」とは、Pythonが関数のように「呼び出す」ことができるものを指します。

そのため、`something`オブジェクト（関数ではないかもしれませんが）を持っていて、それを次のように「呼び出す」（実行する）ことができるとします:

```Python
something()
```

または

```Python
something(some_argument, some_keyword_argument="foo")
```

これを「呼び出し可能」なものと呼びます。

## 依存関係としてのクラス

Pythonのクラスのインスタンスを作成する際に、同じ構文を使用していることに気づくかもしれません。

例えば:

```Python
class Cat:
    def __init__(self, name: str):
        self.name = name


fluffy = Cat(name="Mr Fluffy")
```

この場合、`fluffy`は`Cat`クラスのインスタンスです。

そして`fluffy`を作成するために、`Cat`を「呼び出している」ことになります。

そのため、Pythonのクラスもまた「呼び出し可能」です。

そして、**FastAPI** では、Pythonのクラスを依存関係として使用することができます。

FastAPIが実際にチェックしているのは、それが「呼び出し可能」（関数、クラス、その他なんでも）であり、パラメータが定義されているかどうかということです。

**FastAPI** の依存関係として「呼び出し可能なもの」を渡すと、その「呼び出し可能なもの」のパラメータを解析し、サブ依存関係も含めて、*path operation関数*のパラメータと同じように処理します。

それは、パラメータが全くない呼び出し可能なものにも適用されます。パラメータのない*path operation関数*と同じように。

そこで、上で紹介した依存関係の`common_parameters`を`CommonQueryParams`クラスに変更します:

{* ../../docs_src/dependencies/tutorial002.py hl[11,12,13,14,15] *}

クラスのインスタンスを作成するために使用される`__init__`メソッドに注目してください:

{* ../../docs_src/dependencies/tutorial002.py hl[12] *}

...以前の`common_parameters`と同じパラメータを持っています:

{* ../../docs_src/dependencies/tutorial001.py hl[8] *}

これらのパラメータは **FastAPI** が依存関係を「解決」するために使用するものです。

どちらの場合も以下を持っています:

* オプショナルの`q`クエリパラメータ。
* `skip`クエリパラメータ、デフォルトは`0`。
* `limit`クエリパラメータ、デフォルトは`100`。

どちらの場合も、データは変換され、検証され、OpenAPIスキーマなどで文書化されます。

## 使用

これで、このクラスを使用して依存関係を宣言することができます。

{* ../../docs_src/dependencies/tutorial002.py hl[19] *}

**FastAPI** は`CommonQueryParams`クラスを呼び出します。これにより、そのクラスの「インスタンス」が作成され、インスタンスはパラメータ`commons`として関数に渡されます。

## 型注釈と`Depends`

上のコードでは`CommonQueryParams`を２回書いていることに注目してください:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

以下にある最後の`CommonQueryParams`:

```Python
... = Depends(CommonQueryParams)
```

...は、**FastAPI** が依存関係を知るために実際に使用するものです。

そこからFastAPIが宣言されたパラメータを抽出し、それが実際にFastAPIが呼び出すものです。

---

この場合、以下にある最初の`CommonQueryParams`:

```Python
commons: CommonQueryParams ...
```

...は **FastAPI** に対して特別な意味をもちません。FastAPIはデータ変換や検証などには使用しません（それらのためには`= Depends(CommonQueryParams)`を使用しています）。

実際には以下のように書けばいいだけです:

```Python
commons = Depends(CommonQueryParams)
```

以下にあるように:

{* ../../docs_src/dependencies/tutorial003.py hl[19] *}

しかし、型を宣言することは推奨されています。そうすれば、エディタは`commons`のパラメータとして何が渡されるかを知ることができ、コードの補完や型チェックなどを行うのに役立ちます:

<img src="https://fastapi.tiangolo.com/img/tutorial/dependencies/image02.png">

## ショートカット

しかし、ここでは`CommonQueryParams`を２回書くというコードの繰り返しが発生していることがわかります:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

依存関係が、クラス自体のインスタンスを作成するために**FastAPI**が「呼び出す」*特定の*クラスである場合、**FastAPI** はこれらのケースのショートカットを提供しています。

それらの具体的なケースについては以下のようにします:

以下のように書く代わりに:

```Python
commons: CommonQueryParams = Depends(CommonQueryParams)
```

...以下のように書きます:

```Python
commons: CommonQueryParams = Depends()
```

パラメータの型として依存関係を宣言し、`Depends()`の中でパラメータを指定せず、`Depends()`をその関数のパラメータの「デフォルト」値（`=`のあとの値）として使用することで、`Depends(CommonQueryParams)`の中でクラス全体を*もう一度*書かなくてもよくなります。

同じ例では以下のようになります:

{* ../../docs_src/dependencies/tutorial004.py hl[19] *}

...そして **FastAPI** は何をすべきか知っています。

/// tip | 豆知識

役に立つというよりも、混乱するようであれば無視してください。それをする*必要*はありません。

それは単なるショートカットです。なぜなら **FastAPI** はコードの繰り返しを最小限に抑えることに気を使っているからです。

///
