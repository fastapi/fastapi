# パスパラメータと数値の検証

`Query`を使ってクエリパラメータのための検証とメタデータを定義できるように、パスパラメータのため`Path`を使って検証およびメタデータのクエリパラメータと同じ型を定義することができます。

## Pathのインポート

最初に、`fastapi`から`Path`をインポートします。:

```Python hl_lines="3"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

## メタデータの定義

`Query`と同様のパラメータを定義することができます。

例えば、`item_id`のパスパラメータのため、`title`のメタデータの値を定義するために次のようにタイプします。:

```Python hl_lines="10"
{!../../../docs_src/path_params_numeric_validations/tutorial001.py!}
```

!!! note "技術詳細"
    パスの一部である必要があるため、パスパラメータは常に必須です。
    
    そのため、`...`を使ってそのパラメータが必須であることを表さなければいけません。

    それでもなお、`None`またはデフォルト値を定義した場合でも、何も影響せず、常に必須となります。

## 並べたい順番でパラメータを並べる

例えば、必須の`str`としてクエリパラメータの`q`を定義したいとしましょう。

そのパラメータに関しては他に定義することはないので、`Query`を使う必要はありません。

しかし、 `item_id`のパスパラメータのため、`Path`を使う必要があります。

デフォルトを持たない引数の前にデフォルト引数を置くと、pythonは文句をいいます。

しかし、それらを並べ直し、デフォルトを持たない引数を最初に置きます。

それは**FastAPI**には関係ありません。パラメータの名前、型、デフォルトの定義(`Query`, `Path`, etc)により検知されるため、順番については気にしません。

そのため、あなたは以下のように関数を定義できます。:

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial002.py!}
```

## 並べたい順番でパラメータを並べる仕掛け

もし、`Query`またはデフォルト値なしの`q`のクエリパラメータおよび`Path`を使用した`item_id`のパスパラメータを定義し、それらを別の順番に並べたい場合、pythonはちょっとした特別な構文があります。

関数の最初の引数に`*`を渡します。

pythonはこの`*`に対して何もしませんが、それに続くすべてのパラメータが<abbr title="From: K-ey W-ord Arg-uments"><code>kwargs</code></abbr>と知られるキーワード引数（キーと値のペア）です。たとえそれらがデフォルト値を持たないとしてもです。

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial003.py!}
```

## 数値の検証: 〜以上

`Query`および`Path`(他のものはあとで見ます)を使って、文字列の制約が定義でき、また同様に数値の制約も定義することができます。


ここでは、`ge=1`を使って、`item_id`が`1`に対して"`g`reater than or `e`qual"の整数値である必要です。

```Python hl_lines="8"
{!../../../docs_src/path_params_numeric_validations/tutorial004.py!}
```

## 数値の検証: 〜より大きい、〜以下

以下も同様です:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

```Python hl_lines="9"
{!../../../docs_src/path_params_numeric_validations/tutorial005.py!}
```

## 数値の検証: 浮動小数での〜より大きい、〜未満

数値の検証は`float`の値でも動作します。

ここで重要になってくるのは、<abbr title="greater than or equal"><code>ge</code></abbr>だけではなく、<abbr title="greater than"><code>gt</code></abbr>を定義することができることです。例えば、0より大きく1未満でなければならない値を要求することができます。

そのため、`0.5`は正しい値です。しかし、`0.0`または`0`正しい値ではありません。

<abbr title="less than"><code>lt</code></abbr>も同様です。

```Python hl_lines="11"
{!../../../docs_src/path_params_numeric_validations/tutorial006.py!}
```

## 要約

`Query`および`Path`(他のものはあとで見ます)を使って、[Query Parameters and String Validations](query-params-str-validations.md){.internal-link target=_blank}と同じ方法で、メタデータおよび文字列の検証ができます。

そして、同様に数値の検証が可能です。

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

!!! info "情報"
    `Query`、`Path`および後ほど見るその他は共通の`Param`クラス(使う必要はありません)のサブクラスです。

    そして、それらの全てはあなたがすでに見た、追加の検証およびメタデータを共有しています。

!!! note "技術詳細"
    `fastapi`から`Query`、`Path`およびその他をインポートしたとき、それらは実は関数です。

    呼び出されたとき、同じ名前のクラスのインスタンスが返されます。

    そのため、`Query`という関数をインポートしています。そして、それを呼び出したとき、`Query`という名前のクラスのインスタンスが返されます。

    エディタがそれらの型についてエラーとつけないように、(直接クラスを使用する代わりに)これらの関数が存在します。

    この方法により、これらのエラーのカスタム設定を追加する必要がなく、通常のエディタとコーディングツールを使うことができます。
