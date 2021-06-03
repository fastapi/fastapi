# Python型ヒントについて

Pythonはバージョン3.6から型ヒントをサポートしました。

**型ヒント**は変数の<abbr title="例えば：str、int、float、bool">型</abbr>を宣言できる特殊な文法です。

変数を宣言することによって、エディターやツールからより良いサポートを受けることができます。

この文章はPython型ヒントについての**クイックチュートリアル / おさらい**です。**FastAPI**を使うための型ヒントについての必要最小限の知識しか含まれていません。

**FastAPI**はすべて型ヒントに基づいて構築されています。これによってたくさんのアドバンテージと利便性をもたらしました。

**FastAPI**を使わなくても，型ヒントを知ることはどこかで役に立つでしょう。

!!! note "備考"
    もしあなたがすでにPythonのエキスパートで、型ヒントについてよく知っているなら、次の章に移りましょう。

## 動機

簡単な例から始めましょう：

```Python
{!../../../docs_src/python_types/tutorial001.py!}
```

このプログラムを実行すると、以下のように出力されます：

```
John Doe
```

この関数は以下のことをしています：

* 引数`first_name`と`last_name`を受けます。
* メソッド`title()`でそれぞれの引数の最初のアルファベットを大文字に変換します。
* 真ん中にスペースを入れて二つの引数を<abbr title="順番で二つの引数を一つにします。">つなぎます</abbr>。

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial001.py!}
```

### プログラムを修正する

これはとてもシンプルなプログラムです。

でも、ゼロからこのプログラムを書くことを想像してください。

ある時に、関数を定義し、引数を用意した...。

次に、”最初のアルファベットを大文字に変換するメソッド”を呼び出そうとします。

あれ、待って、そのメソッドは何でしたっけ、`upper`でしょうか？それとも `uppercase`？`first_uppercase`？`capitalize`でしょうか？

そうなるとプログラマーの友ーーコード自動補完機能に助けを求めるでしょう。

関数の最初の引数`first_name`を入力し、後ろにドット（`.`）を入れて、`Ctrl+Space`を押して自動補完を呼び出そうとします。

しかし、残念ながら何も起こりません。

<img src="https://fastapi.tiangolo.com/img/python-types/image01.png">

### 型を入れる

上のプログラムを一行だけ変更しましょう。

関数の引数を次のような形から：

```Python
    first_name, last_name
```

このように変えます：

```Python
    first_name: str, last_name: str
```

これだけです。

これだけが型ヒントです。

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial002.py!}
```

これはデフォルト値の設定と違います。デフォルト値の設定はこう書きます：

```Python
    first_name="john", last_name="doe"
```

型ヒントとデフォルト値の設定は全く違うことです。

型ヒントが使ったのはコロン（`:`）であって、イコール記号（`=`）ではありません。

通常なら、型ヒントを入れるか否かで実行結果が変わることはありません。

では、もう一度この関数を作っているところを想像してみてください。今度は型ヒントを入れました。

同じところで`Ctrl+Space`を押して自動補完を呼び出そうとすると、このようになります：

<img src="https://fastapi.tiangolo.com/img/python-types/image02.png">

こうすると、スクロールしてオプションを探し、見覚えのあるものを見つけることができるでしょう。

<img src="https://fastapi.tiangolo.com/img/python-types/image03.png">

## さらなる動機

この、すでに型ヒントを入れた関数を見てください：

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial003.py!}
```

エディターはすでに変数の型を知っているため、コードの補完だけでなく、エラーをチェックすることもできます。

<img src="https://fastapi.tiangolo.com/img/python-types/image04.png">

これを修復しなければならないため、`str(age)`を使って`age`を文字列に変換します。

```Python hl_lines="2"
{!../../../docs_src/python_types/tutorial004.py!}
```

## 型を宣言する

ここまで紹介したのが、関数の引数として型ヒントを宣言する主な場面です。

これも**FastAPI**において、型ヒントを使う主な場面です。

### シンプルタイプ

`str`型だけではなく、すべてのPythonの標準な型を宣言することができます。

例えば以下の型：

* `int`
* `float`
* `bool`
* `bytes`

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial005.py!}
```

### タイプパラメータ付きのジェネリック型

他の値を収納できるデータ構造があります。例えば：`dict`型、`list`型、`set`型と`tuple`型。それの内部の値も自分の型を持っています。

Pythonの標準モジュール`typing`を使って、これらの型とその内部変数の型を宣言することができます。

このモジュールはこのような型をサポートするためだけにあります。

#### リスト

例えば、`str`型の要素によって構成される`list`型の変数を定義しましょう。

`typing`モジュールから`List`をインポート（`L`は大文字）：

```Python hl_lines="1"
{!../../../docs_src/python_types/tutorial006.py!}
```

同じくコロン（`:`）を使ってこの変数を宣言します。

型を`List`にします。

内部の型を含むリストであるため、内部の型を角括弧に入れます：

```Python hl_lines="4"
{!../../../docs_src/python_types/tutorial006.py!}
```

!!! tip "豆知識"
    角括弧の中にある内部タイプは”タイプパラメータ”と言います。

    この場合では、`str`は`List`に渡されるタイプパラメータです。

上のプログラムは”変数`items`は`list`型であり、かつその中身のすべての要素は`str`型である”という意味です。

こうすると、リストの中の要素を処理しているときも、エディターがサポートしてくれます。

<img src="https://fastapi.tiangolo.com/img/python-types/image05.png">

タイプを入れなければ、このようなことは実現できません。

ここで注意すべきことは、変数`item`はリスト`items`の一つの要素であるということです。

さらに、エディターは変数`item`は`str`型だということを知っており、それをサポートしました。

#### タプル型と集合型

`tuple`型と`set`型を宣言する方法も同じです。

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial007.py!}
```

このプログラムは以下のことを意味します：

* 変数`items_t`は`tuple`型であり、2つの`int`型と1つの`str`型の3つの要素から構成されています。
* 変数`items_s`は`set`型である、その中のすべての要素は`bytes`型です。

#### 辞書型

`dict`型を定義するときは2つの引数を渡します。コンマで区切ります。

最初の引数は`dict`型のキーの型を定義します。

2つ目の引数は`dict`型の値の型を定義します。

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial008.py!}
```

このプログラムは以下のことを意味します：

* 変数`prices`は`dict`であり：
    * この`dict`型変数のすべてのキーは`str`型です（それぞれの要素の名前と呼んでおきましょう）。
    * この`dict`型変数のすべての値は`float`型です（それぞれの要素の価格と呼んでおきましょう）。

#### `Optional`

`Optional`を使うと、とある変数には型があるということを宣言することができます。
しかし、それは”オプショナル”なことです。つまり、その変数の値は`None`であることも許されます。

```Python hl_lines="1  4"
{!../../../docs_src/python_types/tutorial009.py!}
```

常に`str`型ですが、実際は`None`である場合もある値を定義するとき、`str`ではなく`Optional[str]`を使ったら、エディターがエラーをチェックしてくれます。

#### ジェネリック型

角括弧に囲まれるタイプパラメータを要する型、例えば：

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...とその他。

これらは **ジェネリック型**あるいは**ジェネリック**と呼びます。

### クラスを型にする

クラスを変数の型として宣言することもできます。

`Person`というクラスがあると仮定しましょう。これは、nameというフィールドを持ちます。

```Python hl_lines="1-3"
{!../../../docs_src/python_types/tutorial010.py!}
```

次に、変数を`Person`型として宣言できます。

```Python hl_lines="6"
{!../../../docs_src/python_types/tutorial010.py!}
```

そうすると、またエディターからサポートを受けることができます。

<img src="https://fastapi.tiangolo.com/img/python-types/image06.png">

## Pydanticモジュール

<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">Pydantic</a>はデータの妥当性を検証するためのPyhtonライブラリです。

データの”構造”をフィールドを持つクラスとして宣言することができます。

それぞれのフィールドには型があります。

次に、いくつかの値をもってそのクラスのインスタンスを作ります。
このモジュールは値の妥当性を検証し、必要であれば適切な型に変換して、すべてのデータを含むオブジェクトを返します。

そうすると、このオブジェクトにおいてすべてのエディターサポートを受けることができます。

次の例はPydanticの公式ドキュメントのものです：

```Python
{!../../../docs_src/python_types/tutorial011.py!}
```

!!! info "情報"
    Pydanticについて詳しく知りたい場合は、<a href="https://pydantic-docs.helpmanual.io/" class="external-link" target="_blank">ドキュメントをチェックしてください</a>。

**FastAPI**はすべてPydanticに基づいて構築されます。

[チュートリアル - ユーザーガイド](tutorial/index.md){.internal-link target=_blank}の中で、これが実践される場面をたくさん見ることになります。

## **FastAPI**においての型ヒント

**FastAPI**は型ヒントのアドバンテージを取って、いくつかのことを行なっています。

**FastAPI**を使うとき、型ヒントを用いて引数を宣言すると、以下のことができます：

* **エディターサポート**。
* **型チェック**。

...さらに**FastAPI**はその宣言を用いて以下のことを行っています：

* **要件定義**：リクエストからのパスパラメータ、クエリパラメータ、ヘッダー、ボディ、依存性などの要件を定義する。
* **データ変換**：リクエストからのデータを望まれる形に変換する。
* **妥当性検証**： すべてのリクエストに対して：
    * 無効なデータであるときは自動的に**エラーメッセージ**を生成し返します。
* OpenAPIを用いてAPIを**記録**：
    * 自動対話ドキュメントのユーザインタフェースに使われます。

抽象的に聞こえますが、心配することはありません。[チュートリアル - ユーザーガイド](tutorial/index.md){.internal-link target=_blank}の中でそのすべての運用を見ることができます。

何より、Python標準型を用いてひとつのところにだけ定義すれば（たくさんのクラスとデコレーターを入れる代わりに）、**FastAPI**はたくさんの仕事をやってくれます。

!!! info "情報"
    すでにチュートリアルをすべて終えて、型についてもっと知りたいと思って戻ってきた人にとって、<a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`の”cheat sheet”</a>は良い資料になるでしょう。
