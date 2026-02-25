# パスパラメータと数値の検証 { #path-parameters-and-numeric-validations }

クエリパラメータに対して`Query`でより多くのバリデーションとメタデータを宣言できるのと同じように、パスパラメータに対しても`Path`で同じ種類のバリデーションとメタデータを宣言することができます。

## `Path`のインポート { #import-path }

まず初めに、`fastapi`から`Path`をインポートし、`Annotated`もインポートします:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[1,3] *}

/// info | 情報

FastAPI はバージョン 0.95.0 で`Annotated`のサポートを追加し（そして推奨し始めました）。

古いバージョンの場合、`Annotated`を使おうとするとエラーになります。

`Annotated`を使用する前に、FastAPI のバージョンを少なくとも 0.95.1 まで[アップグレードしてください](../deployment/versions.md#upgrading-the-fastapi-versions){.internal-link target=_blank}。

///

## メタデータの宣言 { #declare-metadata }

パラメータは`Query`と同じものを宣言することができます。

例えば、パスパラメータ`item_id`に対して`title`のメタデータを宣言するには以下のようにします:

{* ../../docs_src/path_params_numeric_validations/tutorial001_an_py310.py hl[10] *}

/// note | 備考

パスパラメータはパスの一部でなければならないので、常に必須です。`None`で宣言したりデフォルト値を設定したりしても何も影響せず、常に必須のままです。

///

## 必要に応じてパラメータを並び替える { #order-the-parameters-as-you-need }

/// tip | 豆知識

`Annotated`を使う場合、これはおそらくそれほど重要でも必要でもありません。

///

クエリパラメータ`q`を必須の`str`として宣言したいとしましょう。

また、このパラメータには何も宣言する必要がないので、`Query`を使う必要はありません。

しかし、パスパラメータ`item_id`のために`Path`を使用する必要があります。そして何らかの理由で`Annotated`を使いたくないとします。

Pythonは「デフォルト」を持つ値を「デフォルト」を持たない値の前に置くとエラーになります。

しかし、それらを並び替えることができ、デフォルト値を持たない値（クエリパラメータ`q`）を最初に持つことができます。

**FastAPI**では関係ありません。パラメータは名前、型、デフォルトの宣言（`Query`、`Path`など）で検出され、順番は気にしません。

そのため、以下のように関数を宣言することができます:

{* ../../docs_src/path_params_numeric_validations/tutorial002_py310.py hl[7] *}

ただし、`Annotated`を使う場合はこの問題は起きないことを覚えておいてください。`Query()`や`Path()`に関数パラメータのデフォルト値を使わないためです。

{* ../../docs_src/path_params_numeric_validations/tutorial002_an_py310.py *}

## 必要に応じてパラメータを並び替えるトリック { #order-the-parameters-as-you-need-tricks }

/// tip | 豆知識

`Annotated`を使う場合、これはおそらくそれほど重要でも必要でもありません。

///

これは**小さなトリック**で、便利な場合がありますが、頻繁に必要になることはありません。

次のことをしたい場合:

* `q`クエリパラメータを`Query`もデフォルト値もなしで宣言する
* パスパラメータ`item_id`を`Path`を使って宣言する
* それらを別の順番にする
* `Annotated`を使わない

...Pythonにはそのための少し特殊な構文があります。

関数の最初のパラメータとして`*`を渡します。

Pythonはその`*`で何かをすることはありませんが、それ以降のすべてのパラメータがキーワード引数（キーと値のペア）として呼ばれるべきものであると知っているでしょう。それは<abbr title="From: K-ey W-ord Arg-uments - キーワード引数"><code>kwargs</code></abbr>としても知られています。たとえデフォルト値がなくても。

{* ../../docs_src/path_params_numeric_validations/tutorial003_py310.py hl[7] *}

### `Annotated`のほうがよい { #better-with-annotated }

`Annotated`を使う場合は、関数パラメータのデフォルト値を使わないため、この問題は起きず、おそらく`*`を使う必要もありません。

{* ../../docs_src/path_params_numeric_validations/tutorial003_an_py310.py hl[10] *}

## 数値の検証: 以上 { #number-validations-greater-than-or-equal }

`Query`と`Path`（、そして後述する他のもの）を用いて、数値の制約を宣言できます。

ここで、`ge=1`の場合、`item_id`は`1`「より大きい`g`か、同じ`e`」整数でなければなりません。

{* ../../docs_src/path_params_numeric_validations/tutorial004_an_py310.py hl[10] *}

## 数値の検証: より大きいと小なりイコール { #number-validations-greater-than-and-less-than-or-equal }

以下も同様です:

* `gt`: `g`reater `t`han
* `le`: `l`ess than or `e`qual

{* ../../docs_src/path_params_numeric_validations/tutorial005_an_py310.py hl[10] *}

## 数値の検証: 浮動小数点、 大なり小なり { #number-validations-floats-greater-than-and-less-than }

数値のバリデーションは`float`の値に対しても有効です。

ここで重要になってくるのは<abbr title="greater than – より大きい"><code>gt</code></abbr>だけでなく<abbr title="greater than or equal – 以上"><code>ge</code></abbr>も宣言できることです。これと同様に、例えば、値が`1`より小さくても`0`より大きくなければならないことを要求することができます。

したがって、`0.5`は有効な値ですが、`0.0`や`0`はそうではありません。

これは<abbr title="less than – より小さい"><code>lt</code></abbr>も同じです。

{* ../../docs_src/path_params_numeric_validations/tutorial006_an_py310.py hl[13] *}

## まとめ { #recap }

`Query`と`Path`（そしてまだ見たことない他のもの）では、[クエリパラメータと文字列の検証](query-params-str-validations.md){.internal-link target=_blank}と同じようにメタデータと文字列の検証を宣言することができます。

また、数値のバリデーションを宣言することもできます:

* `gt`: `g`reater `t`han
* `ge`: `g`reater than or `e`qual
* `lt`: `l`ess `t`han
* `le`: `l`ess than or `e`qual

/// info | 情報

`Query`、`Path`、および後で見る他のクラスは、共通の`Param`クラスのサブクラスです。

それらはすべて、これまで見てきた追加のバリデーションとメタデータの同じパラメータを共有しています。

///

/// note | 技術詳細

`fastapi`から`Query`、`Path`などをインポートすると、これらは実際には関数です。

呼び出されると、同じ名前のクラスのインスタンスを返します。

そのため、関数である`Query`をインポートし、それを呼び出すと、`Query`という名前のクラスのインスタンスが返されます。

これらの関数は（クラスを直接使うのではなく）エディタが型についてエラーとしないようにするために存在します。

この方法によって、これらのエラーを無視するための設定を追加することなく、通常のエディタやコーディングツールを使用することができます。

///
