# Pythonの型の紹介 { #python-types-intro }

Pythonではオプションの「型ヒント」（「型アノテーション」とも呼ばれます）がサポートされています。

これらの **「型ヒント」** またはアノテーションは、変数の<abbr title="for example: str, int, float, bool">型</abbr>を宣言できる特別な構文です。

変数に型を宣言することで、エディターやツールがより良いサポートを提供できます。

これはPythonの型ヒントについての **クイックチュートリアル/リフレッシュ** にすぎません。**FastAPI** で使用するために必要な最低限のことだけをカバーしています。...実際には本当に少ないです。

**FastAPI** はすべてこれらの型ヒントに基づいており、多くの強みと利点を与えてくれます。

しかし、たとえ **FastAPI** をまったく使用しない場合でも、それらについて少し学ぶことで利点を得られます。

/// note | 備考

もしあなたがPythonの専門家で、すでに型ヒントについてすべて知っているのであれば、次の章まで読み飛ばしてください。

///

## 動機 { #motivation }

簡単な例から始めてみましょう:

{* ../../docs_src/python_types/tutorial001_py39.py *}

このプログラムを呼び出すと、以下が出力されます:

```
John Doe
```

この関数は以下のようなことを行います:

* `first_name`と`last_name`を取得します。
* `title()`を用いて、それぞれの最初の文字を大文字に変換します。
* 真ん中にスペースを入れて<abbr title="Puts them together, as one. With the contents of one after the other.">連結</abbr>します。

{* ../../docs_src/python_types/tutorial001_py39.py hl[2] *}

### 編集 { #edit-it }

これはとても簡単なプログラムです。

しかし、今、あなたがそれを一から書いていたと想像してみてください。

パラメータの準備ができていたら、そのとき、関数の定義を始めていたことでしょう...

しかし、そうすると「最初の文字を大文字に変換するあのメソッド」を呼び出す必要があります。

それは`upper`でしたか？`uppercase`でしたか？`first_uppercase`？`capitalize`？

そして、古くからプログラマーの友人であるエディタで自動補完を試してみます。

関数の最初のパラメータ`first_name`を入力し、ドット(`.`)を入力してから、`Ctrl+Space`を押すと補完が実行されます。

しかし、悲しいことに、これはなんの役にも立ちません:

<img src="/img/python-types/image01.png">

### 型の追加 { #add-types }

先ほどのコードから一行変更してみましょう。

関数のパラメータである次の断片を、以下から:

```Python
    first_name, last_name
```

以下へ変更します:

```Python
    first_name: str, last_name: str
```

これだけです。

それが「型ヒント」です:

{* ../../docs_src/python_types/tutorial002_py39.py hl[1] *}

これは、以下のようにデフォルト値を宣言するのと同じではありません:

```Python
    first_name="john", last_name="doe"
```

それとは別物です。

イコール（`=`）ではなく、コロン（`:`）を使用します。

そして、通常、型ヒントを追加しても、それらがない状態と起こることは何も変わりません。

しかし今、あなたが再びその関数を作成している最中に、型ヒントを使っていると想像してみてください。

同じタイミングで`Ctrl+Space`で自動補完を実行すると、以下のようになります:

<img src="/img/python-types/image02.png">

これであれば、あなたは「ベルを鳴らす」ものを見つけるまで、オプションを見てスクロールできます:

<img src="/img/python-types/image03.png">

## より強い動機 { #more-motivation }

この関数を見てください。すでに型ヒントを持っています:

{* ../../docs_src/python_types/tutorial003_py39.py hl[1] *}

エディタは変数の型を知っているので、補完だけでなく、エラーチェックをすることもできます:

<img src="/img/python-types/image04.png">

これで`age`を`str(age)`で文字列に変換して修正する必要があることがわかります:

{* ../../docs_src/python_types/tutorial004_py39.py hl[2] *}

## 型の宣言 { #declaring-types }

型ヒントを宣言する主な場所を見てきました。関数のパラメータです。

これは **FastAPI** で使用する主な場所でもあります。

### 単純な型 { #simple-types }

`str`だけでなく、Pythonの標準的な型すべてを宣言できます。

例えば、以下を使用可能です:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005_py39.py hl[1] *}

### 型パラメータを持つジェネリック型 { #generic-types-with-type-parameters }

データ構造の中には、`dict`、`list`、`set`、`tuple`のように他の値を含むことができるものがあります。また内部の値も独自の型を持つことができます。

内部の型を持つこれらの型は「**generic**」型と呼ばれます。そして、内部の型も含めて宣言することが可能です。

これらの型や内部の型を宣言するには、Pythonの標準モジュール`typing`を使用できます。これらの型ヒントをサポートするために特別に存在しています。

#### 新しいPythonバージョン { #newer-versions-of-python }

`typing`を使う構文は、Python 3.6から最新バージョンまで（Python 3.9、Python 3.10などを含む）すべてのバージョンと **互換性** があります。

Pythonが進化するにつれ、**新しいバージョン** ではこれらの型アノテーションへのサポートが改善され、多くの場合、型アノテーションを宣言するために`typing`モジュールをインポートして使う必要すらなくなります。

プロジェクトでより新しいPythonバージョンを選べるなら、その追加のシンプルさを活用できます。

ドキュメント全体で、Pythonの各バージョンと互換性のある例（差分がある場合）を示しています。

例えば「**Python 3.6+**」はPython 3.6以上（3.7、3.8、3.9、3.10などを含む）と互換性があることを意味します。また「**Python 3.9+**」はPython 3.9以上（3.10などを含む）と互換性があることを意味します。

**最新のPythonバージョン** を使えるなら、最新バージョン向けの例を使ってください。例えば「**Python 3.10+**」のように、それらは **最良かつ最もシンプルな構文** になります。

#### List { #list }

例えば、`str`の`list`の変数を定義してみましょう。

同じコロン（`:`）の構文で変数を宣言します。

型として、`list`を指定します。

リストはいくつかの内部の型を含む型なので、それらを角括弧で囲みます:

{* ../../docs_src/python_types/tutorial006_py39.py hl[1] *}

/// info | 情報

角括弧内の内部の型は「型パラメータ」と呼ばれています。

この場合、`str`は`list`に渡される型パラメータです。

///

つまり: 変数`items`は`list`であり、このリストの各項目は`str`です。

そうすることで、エディタはリストの項目を処理している間にもサポートを提供できます。

<img src="/img/python-types/image05.png">

型がなければ、それはほぼ不可能です。

変数`item`はリスト`items`の要素の一つであることに注意してください。

それでも、エディタはそれが`str`であることを知っていて、そのためのサポートを提供しています。

#### Tuple と Set { #tuple-and-set }

`tuple`と`set`の宣言も同様です:

{* ../../docs_src/python_types/tutorial007_py39.py hl[1] *}

つまり:

* 変数`items_t`は`int`、別の`int`、`str`の3つの項目を持つ`tuple`です。
* 変数`items_s`は`set`であり、その各項目は`bytes`型です。

#### Dict { #dict }

`dict`を定義するには、カンマ区切りで2つの型パラメータを渡します。

最初の型パラメータは`dict`のキーです。

2番目の型パラメータは`dict`の値です:

{* ../../docs_src/python_types/tutorial008_py39.py hl[1] *}

つまり:

* 変数`prices`は`dict`です:
    * この`dict`のキーは`str`型です（例えば、各項目の名前）。
    * この`dict`の値は`float`型です（例えば、各項目の価格）。

#### Union { #union }

変数が**複数の型のいずれか**になり得ることを宣言できます。例えば、`int`または`str`です。

Python 3.6以上（Python 3.10を含む）では、`typing`の`Union`型を使い、角括弧の中に受け付ける可能性のある型を入れられます。

Python 3.10では、受け付ける可能性のある型を<abbr title='also called "bitwise or operator", but that meaning is not relevant here'>縦棒（`|`）</abbr>で区切って書ける **新しい構文** もあります。

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial008b_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial008b_py39.py!}
```

////

どちらの場合も、`item`は`int`または`str`になり得ることを意味します。

#### `None`の可能性 { #possibly-none }

値が`str`のような型を持つ可能性がある一方で、`None`にもなり得ることを宣言できます。

Python 3.6以上（Python 3.10を含む）では、`typing`モジュールから`Optional`をインポートして使うことで宣言できます。

```Python hl_lines="1  4"
{!../../docs_src/python_types/tutorial009_py39.py!}
```

ただの`str`の代わりに`Optional[str]`を使用することで、値が常に`str`であると仮定しているときに、実際には`None`である可能性もあるというエラーをエディタが検出するのに役立ちます。

`Optional[Something]`は実際には`Union[Something, None]`のショートカットで、両者は等価です。

これは、Python 3.10では`Something | None`も使えることを意味します:

//// tab | Python 3.10+

```Python hl_lines="1"
{!> ../../docs_src/python_types/tutorial009_py310.py!}
```

////

//// tab | Python 3.9+

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009_py39.py!}
```

////

//// tab | Python 3.9+ alternative

```Python hl_lines="1  4"
{!> ../../docs_src/python_types/tutorial009b_py39.py!}
```

////

#### `Union`または`Optional`の使用 { #using-union-or-optional }

Python 3.10未満のバージョンを使っている場合、これは私のとても **主観的** な観点からのヒントです:

* 🚨 `Optional[SomeType]`は避けてください
* 代わりに ✨ **`Union[SomeType, None]`を使ってください** ✨

どちらも等価で、内部的には同じですが、`Optional`より`Union`をおすすめします。というのも「**optional**」という単語は値がオプションであることを示唆するように見えますが、実際には「`None`になり得る」という意味であり、オプションではなく必須である場合でもそうだからです。

`Union[SomeType, None]`のほうが意味がより明示的だと思います。

これは言葉や名前の話にすぎません。しかし、その言葉はあなたやチームメイトがコードをどう考えるかに影響し得ます。

例として、この関数を見てみましょう:

{* ../../docs_src/python_types/tutorial009c_py39.py hl[1,4] *}

パラメータ`name`は`Optional[str]`として定義されていますが、**オプションではありません**。そのパラメータなしで関数を呼び出せません:

```Python
say_hi()  # Oh, no, this throws an error! 😱
```

`name`パラメータはデフォルト値がないため、**依然として必須**（*optional*ではない）です。それでも、`name`は値として`None`を受け付けます:

```Python
say_hi(name=None)  # This works, None is valid 🎉
```

良い知らせとして、Python 3.10になればその心配は不要です。型のユニオンを定義するために`|`を単純に使えるからです:

{* ../../docs_src/python_types/tutorial009c_py310.py hl[1,4] *}

そして、`Optional`や`Union`のような名前について心配する必要もなくなります。😎

#### ジェネリック型 { #generic-types }

角括弧で型パラメータを取るこれらの型は、例えば次のように **Generic types** または **Generics** と呼ばれます:

//// tab | Python 3.10+

同じ組み込み型をジェネリクスとして（角括弧と内部の型で）使えます:

* `list`
* `tuple`
* `set`
* `dict`

また、これまでのPythonバージョンと同様に、`typing`モジュールから:

* `Union`
* `Optional`
* ...and others.

Python 3.10では、ジェネリクスの`Union`や`Optional`を使う代替として、型のユニオンを宣言するために<abbr title='also called "bitwise or operator", but that meaning is not relevant here'>縦棒（`|`）</abbr>を使えます。これはずっと良く、よりシンプルです。

////

//// tab | Python 3.9+

同じ組み込み型をジェネリクスとして（角括弧と内部の型で）使えます:

* `list`
* `tuple`
* `set`
* `dict`

そして`typing`モジュールのジェネリクス:

* `Union`
* `Optional`
* ...and others.

////

### 型としてのクラス { #classes-as-types }

変数の型としてクラスを宣言することもできます。

名前を持つ`Person`クラスがあるとしましょう:

{* ../../docs_src/python_types/tutorial010_py39.py hl[1:3] *}

変数を`Person`型として宣言できます:

{* ../../docs_src/python_types/tutorial010_py39.py hl[6] *}

そして、再び、すべてのエディタのサポートを得ることができます:

<img src="/img/python-types/image06.png">

これは「`one_person`はクラス`Person`の**インスタンス**である」ことを意味します。

「`one_person`は`Person`という名前の**クラス**である」という意味ではありません。

## Pydanticのモデル { #pydantic-models }

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> はデータ検証を行うためのPythonライブラリです。

データの「形」を属性付きのクラスとして宣言します。

そして、それぞれの属性は型を持ちます。

さらに、いくつかの値を持つクラスのインスタンスを作成すると、その値を検証し、適切な型に変換して（もしそうであれば）すべてのデータを持つオブジェクトを提供してくれます。

また、その結果のオブジェクトですべてのエディタのサポートを受けることができます。

Pydanticの公式ドキュメントからの例:

{* ../../docs_src/python_types/tutorial011_py310.py *}

/// info | 情報

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydanticの詳細はドキュメントを参照してください</a>。

///

**FastAPI** はすべてPydanticをベースにしています。

すべてのことは[チュートリアル - ユーザーガイド](tutorial/index.md){.internal-link target=_blank}で実際に見ることができます。

/// tip | 豆知識

Pydanticには、デフォルト値なしで`Optional`または`Union[Something, None]`を使った場合の特別な挙動があります。詳細はPydanticドキュメントの<a href="https://docs.pydantic.dev/2.3/usage/models/#required-fields" class="external-link" target="_blank">Required Optional fields</a>を参照してください。

///

## メタデータアノテーション付き型ヒント { #type-hints-with-metadata-annotations }

Pythonには、`Annotated`を使って型ヒントに**追加の<abbr title="Data about the data, in this case, information about the type, e.g. a description.">メタデータ</abbr>**を付与できる機能もあります。

Python 3.9以降、`Annotated`は標準ライブラリの一部なので、`typing`からインポートできます。

{* ../../docs_src/python_types/tutorial013_py39.py hl[1,4] *}

Python自体は、この`Annotated`で何かをするわけではありません。また、エディタや他のツールにとっても、型は依然として`str`です。

しかし、`Annotated`内のこのスペースを使って、アプリケーションをどのように動作させたいかについての追加メタデータを **FastAPI** に提供できます。

覚えておくべき重要な点は、`Annotated`に渡す**最初の*型パラメータ***が**実際の型**であることです。残りは、他のツール向けのメタデータにすぎません。

今のところは、`Annotated`が存在し、それが標準のPythonであることを知っておけば十分です。😎

後で、これがどれほど**強力**になり得るかを見ることになります。

/// tip | 豆知識

これが **標準のPython** であるという事実は、エディタで、使用しているツール（コードの解析やリファクタリングなど）とともに、**可能な限り最高の開発体験**が得られることを意味します。 ✨

また、あなたのコードが他の多くのPythonツールやライブラリとも非常に互換性が高いことも意味します。 🚀

///

## **FastAPI**での型ヒント { #type-hints-in-fastapi }

**FastAPI** はこれらの型ヒントを利用していくつかのことを行います。

**FastAPI** では型ヒントを使ってパラメータを宣言すると以下のものが得られます:

* **エディタサポート**。
* **型チェック**。

...そして **FastAPI** は同じ宣言を使って、以下のことを行います:

* **要件の定義**: リクエストのパスパラメータ、クエリパラメータ、ヘッダー、ボディ、依存関係などから要件を定義します。
* **データの変換**: リクエストから必要な型にデータを変換します。
* **データの検証**: 各リクエストから来るデータについて:
    * データが無効な場合にクライアントに返される **自動エラー** を生成します。
* OpenAPIを使用してAPIを**ドキュメント化**します:
    * これは自動の対話型ドキュメントのユーザーインターフェイスで使われます。

すべてが抽象的に聞こえるかもしれません。心配しないでください。 この全ての動作は [チュートリアル - ユーザーガイド](tutorial/index.md){.internal-link target=_blank}で見ることができます。

重要なのは、Pythonの標準的な型を使うことで、（クラスやデコレータなどを追加するのではなく）1つの場所で **FastAPI** が多くの作業を代わりにやってくれているということです。

/// info | 情報

すでにすべてのチュートリアルを終えて、型についての詳細を見るためにこのページに戻ってきた場合は、良いリソースとして<a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`の「チートシート」</a>があります。

///
