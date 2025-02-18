# Pythonの型の紹介

**Python 3.6以降** では「型ヒント」オプションがサポートされています。

これらの **"型ヒント"** は変数の<abbr title="例: str, int, float, bool">型</abbr>を宣言することができる新しい構文です。（Python 3.6以降）

変数に型を宣言することでエディターやツールがより良いサポートを提供することができます。

ここではPythonの型ヒントについての **クイックチュートリアル/リフレッシュ** で、**FastAPI**でそれらを使用するために必要な最低限のことだけをカバーしています。...実際には本当に少ないです。

**FastAPI** はすべてこれらの型ヒントに基づいており、多くの強みと利点を与えてくれます。

しかしたとえまったく **FastAPI** を使用しない場合でも、それらについて少し学ぶことで利点を得ることができるでしょう。

/// note | 備考

もしあなたがPythonの専門家で、すでに型ヒントについてすべて知っているのであれば、次の章まで読み飛ばしてください。

///

## 動機

簡単な例から始めてみましょう:

{* ../../docs_src/python_types/tutorial001.py *}


このプログラムを実行すると以下が出力されます:

```
John Doe
```

この関数は以下のようなことを行います:

* `first_name`と`last_name`を取得します。
* `title()`を用いて、それぞれの最初の文字を大文字に変換します。
* 真ん中にスペースを入れて<abbr title="次から次へと中身を入れて一つにまとめる">連結</abbr>します。

{* ../../docs_src/python_types/tutorial001.py hl[2] *}


### 編集

これはとても簡単なプログラムです。

しかし、今、あなたがそれを一から書いていたと想像してみてください。

パラメータの準備ができていたら、そのとき、関数の定義を始めていたことでしょう...

しかし、そうすると「最初の文字を大文字に変換するあのメソッド」を呼び出す必要があります。

それは`upper`でしたか？`uppercase`でしたか？それとも`first_uppercase`？または`capitalize`？

そして、古くからプログラマーの友人であるエディタで自動補完を試してみます。

関数の最初のパラメータ`first_name`を入力し、ドット(`.`)を入力してから、`Ctrl+Space`を押すと補完が実行されます。

しかし、悲しいことに、これはなんの役にも立ちません:

<img src="https://fastapi.tiangolo.com/img/python-types/image01.png">

### 型の追加

先ほどのコードから一行変更してみましょう。

以下の関数のパラメータ部分を:

```Python
    first_name, last_name
```

以下へ変更します:

```Python
    first_name: str, last_name: str
```

これだけです。

それが「型ヒント」です:

{* ../../docs_src/python_types/tutorial002.py hl[1] *}


これは、以下のようにデフォルト値を宣言するのと同じではありません:

```Python
    first_name="john", last_name="doe"
```

それとは別物です。

イコール（`=`）ではなく、コロン（`:`）を使用します。

そして、通常、型ヒントを追加しても、それらがない状態と起こることは何も変わりません。

しかし今、あなたが再びその関数を作成している最中に、型ヒントを使っていると想像してみて下さい。

同じタイミングで`Ctrl+Space`で自動補完を実行すると、以下のようになります:

<img src="https://fastapi.tiangolo.com/img/python-types/image02.png">

これであれば、あなたは「ベルを鳴らす」一つを見つけるまで、オプションを見て、スクロールすることができます:

<img src="https://fastapi.tiangolo.com/img/python-types/image03.png">

## より強い動機

この関数を見てください。すでに型ヒントを持っています:

{* ../../docs_src/python_types/tutorial003.py hl[1] *}


エディタは変数の型を知っているので、補完だけでなく、エラーチェックをすることもできます。

<img src="https://fastapi.tiangolo.com/img/python-types/image04.png">

これで`age`を`str(age)`で文字列に変換して修正する必要があることがわかります:

{* ../../docs_src/python_types/tutorial004.py hl[2] *}


## 型の宣言

関数のパラメータとして、型ヒントを宣言している主な場所を確認しました。

これは **FastAPI** で使用する主な場所でもあります。

### 単純な型

`str`だけでなく、Pythonの標準的な型すべてを宣言することができます。

例えば、以下を使用可能です:

* `int`
* `float`
* `bool`
* `bytes`

{* ../../docs_src/python_types/tutorial005.py hl[1] *}


### 型パラメータを持つジェネリック型

データ構造の中には、`dict`、`list`、`set`、そして`tuple`のように他の値を含むことができるものがあります。また内部の値も独自の型を持つことができます。

これらの型や内部の型を宣言するには、Pythonの標準モジュール`typing`を使用します。

これらの型ヒントをサポートするために特別に存在しています。

#### `List`

例えば、`str`の`list`の変数を定義してみましょう。

`typing`から`List`をインポートします（大文字の`L`を含む）:

{* ../../docs_src/python_types/tutorial006.py hl[1] *}


同じようにコロン（`:`）の構文で変数を宣言します。

型として、`List`を入力します。

リストはいくつかの内部の型を含む型なので、それらを角括弧で囲んでいます。

{* ../../docs_src/python_types/tutorial006.py hl[4] *}


/// tip | 豆知識

角括弧内の内部の型は「型パラメータ」と呼ばれています。

この場合、`str`は`List`に渡される型パラメータです。

///

つまり: 変数`items`は`list`であり、このリストの各項目は`str`です。

そうすることで、エディタはリストの項目を処理している間にもサポートを提供できます。

<img src="https://fastapi.tiangolo.com/img/python-types/image05.png">

タイプがなければ、それはほぼ不可能です。

変数`item`はリスト`items`の要素の一つであることに注意してください。

それでも、エディタはそれが`str`であることを知っていて、そのためのサポートを提供しています。

#### `Tuple` と `Set`

`tuple`と`set`の宣言も同様です:

{* ../../docs_src/python_types/tutorial007.py hl[1,4] *}


つまり:

* 変数`items_t`は`int`、`int`、`str`の3つの項目を持つ`tuple`です

* 変数`items_s`はそれぞれの項目が`bytes`型である`set`です。

#### `Dict`

`dict`を宣言するためには、カンマ区切りで2つの型パラメータを渡します。

最初の型パラメータは`dict`のキーです。

２番目の型パラメータは`dict`の値です。

{* ../../docs_src/python_types/tutorial008.py hl[1,4] *}


つまり:

* 変数`prices`は`dict`であり:
    * この`dict`のキーは`str`型です。（つまり、各項目の名前）
    * この`dict`の値は`float`型です。（つまり、各項目の価格）

#### `Optional`

また、`Optional`を使用して、変数が`str`のような型を持つことを宣言することもできますが、それは「オプション」であり、`None`にすることもできます。

```Python hl_lines="1 4"
{!../../docs_src/python_types/tutorial009.py!}
```

ただの`str`の代わりに`Optional[str]`を使用することで、エディタは値が常に`str`であると仮定している場合に実際には`None`である可能性があるエラーを検出するのに役立ちます。

#### ジェネリック型

以下のように角括弧で型パラメータを取る型を:

* `List`
* `Tuple`
* `Set`
* `Dict`
* `Optional`
* ...など

**ジェネリック型** または **ジェネリクス** と呼びます。

### 型としてのクラス

変数の型としてクラスを宣言することもできます。

例えば、`Person`クラスという名前のクラスがあるとしましょう:

{* ../../docs_src/python_types/tutorial010.py hl[1,2,3] *}


変数の型を`Person`として宣言することができます:

{* ../../docs_src/python_types/tutorial010.py hl[6] *}


そして、再び、すべてのエディタのサポートを得ることができます:

<img src="https://fastapi.tiangolo.com/img/python-types/image06.png">

## Pydanticのモデル

<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">Pydantic</a> はデータ検証を行うためのPythonライブラリです。

データの「形」を属性付きのクラスとして宣言します。

そして、それぞれの属性は型を持ちます。

さらに、いくつかの値を持つクラスのインスタンスを作成すると、その値を検証し、適切な型に変換して（もしそうであれば）全てのデータを持つオブジェクトを提供してくれます。

また、その結果のオブジェクトですべてのエディタのサポートを受けることができます。

Pydanticの公式ドキュメントから引用:

{* ../../docs_src/python_types/tutorial011.py *}


/// info | 情報

Pydanticについてより学びたい方は<a href="https://docs.pydantic.dev/" class="external-link" target="_blank">ドキュメントを参照してください</a>.

///

**FastAPI** はすべてPydanticをベースにしています。

すべてのことは[チュートリアル - ユーザーガイド](tutorial/index.md){.internal-link target=_blank}で実際に見ることができます。

## **FastAPI**での型ヒント

**FastAPI** はこれらの型ヒントを利用していくつかのことを行います。

**FastAPI** では型ヒントを使って型パラメータを宣言すると以下のものが得られます:

* **エディタサポート**.
* **型チェック**.

...そして **FastAPI** は同じように宣言をすると、以下のことを行います:

* **要件の定義**: リクエストパスパラメータ、クエリパラメータ、ヘッダー、ボディ、依存関係などから要件を定義します。
* **データの変換**: リクエストのデータを必要な型に変換します。
* **データの検証**: リクエストごとに:
    * データが無効な場合にクライアントに返される **自動エラー** を生成します。
* **ドキュメント** OpenAPIを使用したAPI:
    * 自動的に対話型ドキュメントのユーザーインターフェイスで使用されます。

すべてが抽象的に聞こえるかもしれません。心配しないでください。 この全ての動作は [チュートリアル - ユーザーガイド](tutorial/index.md){.internal-link target=_blank}で見ることができます。

重要なのは、Pythonの標準的な型を使うことで、（クラスやデコレータなどを追加するのではなく）１つの場所で **FastAPI** が多くの作業を代わりにやってくれているということです。

/// info | 情報

すでにすべてのチュートリアルを終えて、型についての詳細を見るためにこのページに戻ってきた場合は、<a href="https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html" class="external-link" target="_blank">`mypy`のチートシートを参照してください</a>

///
